from functions.get_files_info import get_files_info

command_input = [["calculator", "."], ["calculator", "pkg"], ["calculator", "/bin"], ["calculator", "../"]]
# command_input = [["calculator", "."]]

def test_get_files(commands: list) -> str:
    for command in commands:
        ret_of_command = get_files_info(command[0], command[1])
        if command[1] == ".":
            print(f"Results for current directory:")
        else:
            print(f"Results for '{command[1]}' directory:")
        print(ret_of_command)
        print("")
        print("")

def main():
    test_get_files(command_input)

if __name__ == "__main__":
    main()

# Result for current directory:
#   - main.py: file_size=719 bytes, is_dir=False
#   - tests.py: file_size=1331 bytes, is_dir=False
#   - pkg: file_size=44 bytes, is_dir=True