import os

working_directory = "/home/chris/programming/bootdotdev/ai_agent"

def get_files_info(working_directory=working_directory, directory="."):
    if not os.path.abspath(directory).startswith(working_directory):
        # print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        # print(os.path.isdir(directory))
        return f'Error: "{directory}" is not a directory'
    try:
        def get_data_for_files(files: list) -> list:
            concat_ret_list = []
            for file in files:
                size = os.path.getsize(file)
                dir = os.path.isdir(file)
                concat_ret_list.append(f"- {file}: file_size={size}, is_dir={dir}")
            joined = "\n".join(concat_ret_list)
            # print(joined)
            return joined
        # print(working_directory, os.path.abspath(directory))
        # print(get_data_for_files(os.listdir(directory)))
        return get_data_for_files(os.listdir(directory))
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    print(get_files_info())

if __name__ == "__main__":
    main()



# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False