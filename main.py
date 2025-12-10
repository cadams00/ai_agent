import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def load_settings():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Please find my keys!")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
)
if response.usage_metadata == None:
    raise RuntimeError("OMG WE GOT NO RESPONSE SOMETHING IS WRONG IN THE MATRIX")
print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
print("Response tokens: " + str(response.usage_metadata.candidates_token_count))
print("Response:")
print(response.text)

def main():
    print("Hello from ai-agent!")
    # print(args.prompt)

if __name__ == "__main__":
    main()
