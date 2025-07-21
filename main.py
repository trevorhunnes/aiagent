import os
import sys
from google.genai import types
from dotenv import load_dotenv
from google import genai
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
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
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    function_call_part = response.function_calls
    if function_call_part is None:
        print(response.text)
    else:
        for f in function_call_part:
            print(f"Calling function: {f.name}({f.args})")
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
