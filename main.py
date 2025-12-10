import os
import argparse
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
from google.genai import types


ENV_VAR_NAME = "GEMINI_API_KEY"
DEFAULT_MODEL = "gemini-2.5-flash"


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
    return parser.parse_args()


def generate_reply(client: genai.Client, model: str, prompt: str) -> tuple[str, int | None, int | None]:
    """Send a prompt to the model and return (text, prompt_tokens, response_tokens)."""
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response = client.models.generate_content(
        model=model,
        contents=messages,
    )

    text = response.text or ""

    usage = response.usage_metadata
    prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
    response_tokens = getattr(usage, "candidates_token_count", None) if usage else None

    return text, prompt_tokens, response_tokens


def main() -> None:
    args = parse_args()
    settings = load_settings()
    client = build_client(settings)

    reply, prompt_tokens, response_tokens = generate_reply(
        client=client,
        model=settings.model,
        prompt=args.prompt,
    )

    # Metrics (if we got them)
    if prompt_tokens is not None:
        print(f"Prompt tokens:   {prompt_tokens}")
    if response_tokens is not None:
        print(f"Response tokens: {response_tokens}")

    print("Response:")
    print(reply)


if __name__ == "__main__":
    main()
