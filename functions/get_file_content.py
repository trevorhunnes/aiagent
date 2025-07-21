import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Print contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be printed, constrained to the working directory",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    working_directory_path = os.path.abspath(working_directory) + os.sep
    directory_path = os.path.abspath(path) + os.sep

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{file_path} as it is outside the permitted working directory'

    if not os.path.isfile(path):
        return f'Error: "{file_path}" is not a file'

    try:

        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) > 999:
                file_content_string = file_content_string + \
                    f'[...File "{path}" truncated at 10000 characters]'

    except Exception as e:
        return (f"Error: {e}")

    return file_content_string
