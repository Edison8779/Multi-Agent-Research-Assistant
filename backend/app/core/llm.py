import json
from typing import AsyncGenerator, Type, TypeVar, Any, Dict, List, Optional, Tuple
from groq import Groq
from groq import AsyncGroq
from pydantic import BaseModel

from app.core.config import settings

T = TypeVar("T", bound=BaseModel)

# We use the AsyncGroq client as requested
if not settings.LLM_API_KEY:
    raise ValueError(
        "LLM_API_KEY is not set. Please add it to your .env file. "
        "Get a key from https://console.groq.com/keys"
    )

client = AsyncGroq(api_key=settings.LLM_API_KEY)


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class LLMResponse(BaseModel):
    content: str
    usage: TokenUsage


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculate approximate cost based on provider pricing.
    Includes OpenAI and some popular Open Source model providers (e.g. Groq, Together).
    """
    pricing = {
        "openai/gpt-oss-20b": {"input": 0.10 / 1_000_000, "output": 0.10 / 1_000_000},  # Groq pricing
    }
    rates = pricing.get(model, {"input": 0.0, "output": 0.0})
    return (prompt_tokens * rates["input"]) + (completion_tokens * rates["output"])


async def generate_text(
    prompt: str,
    system_message: Optional[str] = None,
    model: str | None = None,
    temperature: float = 0.7,
) -> LLMResponse:
    """
    Generate a simple text response from the LLM, demonstrating system messages,
    temperature control, and token counting.
    """
    if model is None:
        model = settings.LLM_MODEL
        
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    
    content = response.choices[0].message.content or ""
    usage = response.usage
    
    prompt_tokens = usage.prompt_tokens if usage else 0
    completion_tokens = usage.completion_tokens if usage else 0
    
    cost = calculate_cost(model, prompt_tokens, completion_tokens)
    
    return LLMResponse(
        content=content,
        usage=TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost_usd=cost,
        )
    )


async def generate_structured(
    prompt: str, 
    response_model: Type[T], 
    system_message: Optional[str] = None,
    model: str | None = None,
    temperature: float = 0.0,
    max_retries: int = 2,
) -> Tuple[T, TokenUsage]:
    """
    Generate a structured Pydantic output using JSON mode.
    This works across OpenAI and open-source models without relying on the restricted `beta.parse` endpoint.
    Includes retry logic for models that occasionally fail JSON validation.
    """
    if model is None:
        model = settings.LLM_MODEL
        
    schema = response_model.model_json_schema()
    schema_str = json.dumps(schema)
    
    # Build a concrete example from the schema to guide the model
    example = _build_json_example(schema)
    example_str = json.dumps(example, indent=2)
    
    instruction = (
        f"\n\nYou must output a valid JSON object exactly matching this schema: {schema_str}"
        f"\n\nHere is an example of the expected output format:\n{example_str}"
        f"\n\nIMPORTANT: Output ONLY the JSON object. No extra text, no markdown fences."
    )
    
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message + instruction})
    else:
        messages.append({"role": "system", "content": instruction})
        
    messages.append({"role": "user", "content": prompt})

    last_error = None
    total_prompt_tokens = 0
    total_completion_tokens = 0
    
    for attempt in range(max_retries + 1):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=temperature + (0.1 * attempt),  # slightly increase temp on retries
            )

            content = response.choices[0].message.content
            usage = response.usage
            total_prompt_tokens += usage.prompt_tokens if usage else 0
            total_completion_tokens += usage.completion_tokens if usage else 0
            
            if not content or not content.strip():
                raise ValueError("Received empty content from the LLM.")

            # Validate JSON with Pydantic
            parsed = response_model.model_validate_json(content)

            cost = calculate_cost(model, total_prompt_tokens, total_completion_tokens)
            
            token_usage = TokenUsage(
                prompt_tokens=total_prompt_tokens,
                completion_tokens=total_completion_tokens,
                total_tokens=total_prompt_tokens + total_completion_tokens,
                estimated_cost_usd=cost,
            )

            return parsed, token_usage
            
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                continue
    
    if last_error is not None:
        raise last_error
    raise RuntimeError("Structured generation failed after maximum retries.")


def _build_json_example(schema: dict) -> dict:
    """Build a minimal example JSON object from a JSON schema to guide the model."""
    return _example_from_schema(schema, schema.get("$defs", {}))


def _example_from_schema(schema: dict, defs: dict) -> Any:
    """Recursively build an example value from a JSON schema node."""
    if "$ref" in schema:
        ref_name = schema["$ref"].split("/")[-1]
        if ref_name in defs:
            return _example_from_schema(defs[ref_name], defs)
        return {}
    
    schema_type = schema.get("type", "string")
    
    if schema_type == "object":
        result = {}
        for prop_name, prop_schema in schema.get("properties", {}).items():
            result[prop_name] = _example_from_schema(prop_schema, defs)
        return result
    elif schema_type == "array":
        items_schema = schema.get("items", {})
        return [_example_from_schema(items_schema, defs)]
    elif schema_type == "string":
        desc = schema.get("description", "")
        return f"example {desc[:30]}" if desc else "example"
    elif schema_type == "number" or schema_type == "integer":
        return 0.5 if schema_type == "number" else 1
    elif schema_type == "boolean":
        return True
    else:
        return "example"


async def generate_stream(
    prompt: str,
    system_message: Optional[str] = None,
    model: str | None = None,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """
    Stream the response from the LLM back to the caller.
    """
    if model is None:
        model = settings.LLM_MODEL
        
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True,
    )
    
    async for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


async def generate_with_tools(
    prompt: str,
    tools: List[Dict[str, Any]],
    system_message: Optional[str] = None,
    model: str | None = None,
    temperature: float = 0.0,
) -> Any:
    """
    Demonstrate tool calling capabilities.
    """
    if model is None:
        model = settings.LLM_MODEL
        
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=temperature,
    )
    
    return response.choices[0].message
