from functions.run_python_file import run_python_file 

command_input = [["calculator", "main.py"],
                 ["calculator", "main.py", ["3 + 5"]],
                 ["calculator", "tests.py"],
                 ["calculator", "../main.py"],
                 ["calculator", "nonexistent.py"],
                 ["calculator", "lorem.txt"]]

def test_get_files(commands: list) -> None:
    for command in commands:
        if len(command) == 3:
            ret_of_command = run_python_file(command[0], command[1], command[2])
        else:
            ret_of_command = run_python_file(command[0], command[1])
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