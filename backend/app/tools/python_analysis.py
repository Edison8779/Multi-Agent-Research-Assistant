import contextlib
import io
from typing import Any


def run_python(code: str) -> str:
    """
    Execute python code securely (as much as possible) and return stdout.
    In a real production environment, this should run in a sandbox like E2B,
    Firecracker, or a Docker container.
    """
    stdout = io.StringIO()

    # We create an empty local dictionary to avoid polluting the global state
    # and provide some degree of isolation
    local_env: dict[str, Any] = {}

    try:
        with contextlib.redirect_stdout(stdout):
            # Using exec to run arbitrary code.
            # Note: This is highly insecure if exposed to arbitrary user input directly.
            exec(code, {"__builtins__": __builtins__}, local_env)

        output = stdout.getvalue()
        return output.strip() if output else "Execution successful with no output."

    except Exception as e:
        return f"Error executing code: {type(e).__name__}: {str(e)}"
