import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    contents = []
    working_directory_path = os.path.abspath(working_directory) + os.sep
    directory_path = os.path.abspath(path) + os.sep

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    try:

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            is_Dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            contents.append(
                f"- {filename}: file_size={file_size}, is_dir={is_Dir}")
    except Exception as e:
        return f"Error: {e}"

    return f"\n".join(contents)
