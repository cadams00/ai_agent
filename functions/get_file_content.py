import os
from .config import MAX_CHARS 

def get_file_content(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                trnc = f'[...File "{file_path}" truncated at 10000 characters]'
                return file_content_string + trnc
            return file_content_string
    except Exception as e:
        print(f"ERROR: {e}")    




# def get_files_info(working_directory, directory="."):
#     abs_directory = os.path.abspath(os.path.join(working_directory, directory))
#     abs_working_directory = os.path.abspath(working_directory)
#     if not abs_directory.startswith(abs_working_directory):
#         return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
#     if not os.path.isdir(abs_directory):
#         return f'Error: "{directory}" is not a directory'
#     try:
#         def get_data_for_files(files: list) -> str:
#             concat_ret_list = []
#             for file in files:
#                 size = os.path.getsize(os.path.join(abs_directory, file))
#                 dir = os.path.isdir(os.path.join(abs_directory, file))
#                 concat_ret_list.append(f"- {file}: file_size={size}, is_dir={dir}")
#             joined = "\n".join(concat_ret_list)
#             return joined
#         return get_data_for_files(os.listdir(abs_directory))
#     except Exception as e:
#         print(f"ERROR: {e}")