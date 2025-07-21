import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run the program from, relative to the working directory. If not provided, will run from working directory itself",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Any extra arguments to pass to the program. If not provided, the program will run without any extra arguments",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    working_directory_path = os.path.abspath(working_directory) + os.sep
    directory_path = os.path.abspath(path) + os.sep

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'

    if not path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", file_path] + args, cwd=working_directory, capture_output=True, timeout=30, text=True)
        if completed_process.stdout == "":
            return "No output produced."
        if completed_process.returncode != 0:
            return f'STDOUT:{completed_process.stdout}, STDERR:{completed_process.stderr}, Process exited with code {completed_process.returncode}.'
        else:
            return f'STDOUT:{completed_process.stdout}, STDERR:{completed_process.stderr}'

    except Exception as e:
        return f"Error: executing Python file: {e}"

    pass
