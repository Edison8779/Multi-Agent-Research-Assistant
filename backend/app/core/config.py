from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core settings
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str | None = None
    LLM_MODEL: str = ""
    DATABASE_URL: str = ""
    REDIS_URL: str = ""
    SEARCH_API_KEY: str = "" 

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
