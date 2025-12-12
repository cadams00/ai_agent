import os

working_directory = "/home/chris/programming/bootdotdev/ai_agent/"
# "calculator", "."
def get_files_info(working_directory, directory="."):
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_directory = os.path.abspath(working_directory)
    # print(directory, abs_directory, working_directory, abs_working_directory)
    # print(os.path.join(working_directory, directory))
    # if not abs_directory.startswith(abs_working_directory):
    if not abs_directory.startswith(abs_working_directory):
        # print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.join(abs_working_directory,abs_directory)):
        # print(os.path.isdir(directory))
        return f'Error: "{directory}" is not a directory'
    try:
        def get_data_for_files(files: list) -> list:
            concat_ret_list = []
            for file in files:
                size = os.path.getsize(abs_directory + "/" + file)
                dir = os.path.isdir(abs_directory + "/" + file)
                concat_ret_list.append(f"- {file}: file_size={size}, is_dir={dir}")
            joined = "\n".join(concat_ret_list)
            # print(joined)
            return joined
        # print(os.path.join(abs_working_directory,directory))
        # print(working_directory, directory)
        # print(get_data_for_files(os.listdir(directory)))
        return get_data_for_files(os.listdir(os.path.join(abs_working_directory,directory)))
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    print(get_files_info())

if __name__ == "__main__":
    main()