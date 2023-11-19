import json
import argparse
import os
import sln
import shutil

def main():
    parser = argparse.ArgumentParser(description='Generate compile_commands.json from a Visual Studio solution')
    parser.add_argument('-s', '--path', type=str, help='sln file path', required=True)
    parser.add_argument('-c', '--configuration', type=str, default='Debug|Win32', help='Configuration, [configuration|platform], default Debug|Win32')
    args = parser.parse_args()

    solution, err = sln.NewSln(args.path)
    if err:
        print(err)
        exit(1)
    cmdList, err = solution.CompileCommandsJson(args.configuration)
    if err:
        print(err)
        exit(1)
    js = json.dumps([cmd.__dict__ for cmd in cmdList], indent=4)
    print(js)
    with open("compile_commands.json", "w") as file:
        file.write(js)

if __name__ == "__main__":
    main()
