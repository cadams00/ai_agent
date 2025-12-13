import os
import subprocess

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
            return f"STDOUT: {result.stdout} STDERR: {result.stderr} Process exited with code {result.returncode}"
        if not result.stdout:
            return f"No output produced" 
        return f"STDOUT: {result.stdout}STDERR: {result.stderr}"
    except Exception as e:
        return (f"Error: executing Python file: {e}")