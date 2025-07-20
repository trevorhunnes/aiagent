import os


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
