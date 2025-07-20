import os
import sys
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

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt
    )

    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
