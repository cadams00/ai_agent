import os
import argparse
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


ENV_VAR_NAME = "GEMINI_API_KEY"
DEFAULT_MODEL = "gemini-2.5-flash"

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content,
                           schema_run_python_file, schema_write_file],
)

@dataclass
class Settings:
    api_key: str
    model: str = DEFAULT_MODEL


def load_settings() -> Settings:
    """Load configuration from environment / .env."""
    load_dotenv()

    api_key = os.getenv(ENV_VAR_NAME)
    if not api_key:
        raise RuntimeError(
            f"{ENV_VAR_NAME} is not set. "
            "Set it in your environment or .env file."
        )

    return Settings(api_key=api_key)


def build_client(settings: Settings) -> genai.Client:
    """Create and return a configured Gemini client."""
    return genai.Client(api_key=settings.api_key)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Simple Gemini chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def generate_reply(client: genai.Client, model: str, prompt: str) -> tuple[str, int | None, int | None, list | None]:
    """Send a prompt to the model and return (text, prompt_tokens, response_tokens)."""
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    calls = response.function_calls

    if calls:
        text = ""
    else:
        text = response.text or ""

    usage = response.usage_metadata
    prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
    response_tokens = getattr(usage, "candidates_token_count", None) if usage else None

    return text, prompt_tokens, response_tokens, calls


def main() -> None:
    args = parse_args()
    settings = load_settings()
    client = build_client(settings)

    reply, prompt_tokens, response_tokens, calls= generate_reply(
        client=client,
        model=settings.model,
        prompt=args.prompt,
    )

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        if prompt_tokens is not None:
            print(f"Prompt tokens:   {prompt_tokens}")
        if response_tokens is not None:
            print(f"Response tokens: {response_tokens}")
        print(reply)
    else:
        if calls:
            for call in calls:
                print(f"Calling function: {call.name}({call.args})")
        else:
            print("Response:")
            print(reply)

if __name__ == "__main__":
    main()
