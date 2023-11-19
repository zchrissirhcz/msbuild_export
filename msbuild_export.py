import json
import argparse
import sln
import cmake_cache

def main():
    parser = argparse.ArgumentParser(description='Generate compile_commands.json from a Visual Studio solution')
    parser.add_argument('-s', '--path', type=str, help='sln file path', required=True)
    parser.add_argument('-f', '--configuration', type=str, default='Release|x64', help='Configuration, [configuration|platform], default Release|x64')
    parser.add_argument('-c', '--cmake_cache_path', type=str, default='', help='path to CMakeCache.txt or CMakeConfigureLog.yaml', required=False)
    args = parser.parse_args()

    solution, err = sln.NewSln(args.path)
    if err:
        print(err)
        exit(1)
    
    if args.cmake_cache_path == '':
        print("warning: CMakeCache.txt not specified, use default compiler")
        c_compiler = "cl.exe"
        cxx_compiler = "cl.exe"
    else:
        c_compiler, cxx_compiler = cmake_cache.FindCompilerPath(args.cmake_cache_path)
    cmdList, err = solution.CompileCommandsJson(args.configuration, c_compiler, cxx_compiler)
    if err:
        print(err)
        exit(1)
    js = json.dumps([cmd.__dict__ for cmd in cmdList], indent=2)
    #print(js)
    with open("compile_commands.json", "w") as file:
        file.write(js)

if __name__ == "__main__":
    main()
