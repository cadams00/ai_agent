import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run files from, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file that you want to run",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The command line arguments that are passed to the file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(
            ["python3", abs_file_path, *args],
            timeout=30,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return (
                f"STDOUT: {result.stdout} "
                f"STDERR: {result.stderr} "
                f"Process exited with code {result.returncode}"
            )

        output = ""
        if result.stdout:
            output += f"STDOUT: {result.stdout}"
        if result.stderr:
            output += f"STDERR: {result.stderr}"

        if not output:
            return "No output produced"

        return output

    except Exception as e:
        return (f"Error: executing Python file: {e}")