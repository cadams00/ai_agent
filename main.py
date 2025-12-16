import os
import argparse
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def generate_reply(client: genai.Client, model: str, messages: list[types.Content], verbose: bool):

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
    candidates = response.candidates
    usage = response.usage_metadata
    prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
    response_tokens = getattr(usage, "candidates_token_count", None) if usage else None

    if not calls:
        if verbose:
            user_prompt = messages[0].parts[0].text if messages and messages[0].parts else ""
            print(f"User prompt: {user_prompt}")
            if prompt_tokens is not None:
                print(f"Prompt tokens:   {prompt_tokens}")
            if response_tokens is not None:
                print(f"Response tokens: {response_tokens}")
            print(text)
        else:
            print("Response:")
            print(text)
        return

    function_responses = []
    for call in calls:
        function_call_result = call_function(call, verbose)

        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("empty function call result")

        part = function_call_result.parts[0]
        function_responses.append(part)

        if verbose:
            if part.function_response and part.function_response.response is not None:
                print(f"-> {part.function_response.response}")

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    

def main() -> None:
    args = parse_args()
    settings = load_settings()
    client = build_client(settings)
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    generate_reply(client=client, model=settings.model, messages=messages, verbose=args.verbose)
    
if __name__ == "__main__":
    main()