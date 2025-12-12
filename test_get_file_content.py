from functions.get_file_content import get_file_content

command_input = [["calculator", "lorem.txt"], 
                 ["calculator", "main.py"], 
                 ["calculator", "pkg/calculator.py"],
                 ["calculator", "/bin/cat"], 
                 ["calculator", "pkg/does_not_exist.py"]]

def test_get_files(commands: list) -> None:
    for command in commands:
        ret_of_command = get_file_content(command[0], command[1])
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
