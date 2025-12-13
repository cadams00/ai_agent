from functions.write_file import write_file

command_input = [["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
                 ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
                 ["calculator", "/tmp/temp.txt", "this should not be allowed"]]

def test_get_files(commands: list) -> None:
    for command in commands:
        ret_of_command = write_file(command[0], command[1], command[2])
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