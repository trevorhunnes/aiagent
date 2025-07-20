import os
import sys
from google.genai import types
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    try:
        prompt = sys.argv[1]
    except Exception:
        print("Please enter a promt")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    print(response.text)
    try:
        if (sys.argv[2] == "--verbose"):

            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {
                  response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {
                  response.usage_metadata.candidates_token_count}")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
