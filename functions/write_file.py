import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run files from, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that you want to write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        head, tail = os.path.split(abs_file_path)
        if not os.path.exists(head):
            os.makedirs(head)
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"ERROR: {e}")