import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a new file or overwrite and existing file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file being writen or overwriten, constrained to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    working_directory_path = os.path.abspath(working_directory) + os.sep
    directory_path = os.path.abspath(path) + os.sep

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{file_path} as it is outside the permitted working directory'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
