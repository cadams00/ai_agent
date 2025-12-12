import os

working_directory = "/home/chris/programming/bootdotdev/ai_agent/"
def get_files_info(working_directory, directory="."):
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.join(abs_working_directory,abs_directory)):
        return f'Error: "{directory}" is not a directory'
    try:
        def get_data_for_files(files: list) -> list:
            concat_ret_list = []
            for file in files:
                size = os.path.getsize(abs_directory + "/" + file)
                dir = os.path.isdir(abs_directory + "/" + file)
                concat_ret_list.append(f"- {file}: file_size={size}, is_dir={dir}")
            joined = "\n".join(concat_ret_list)
            return joined
        return get_data_for_files(os.listdir(os.path.join(abs_working_directory,directory)))
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    print(get_files_info())

if __name__ == "__main__":
    main()