import os

def FindCompilerPath(cmake_cache_path):
    c_compiler = "cl.exe"
    cxx_compiler = "cl.exe"
    if os.path.exists(cmake_cache_path) == False:
        print("file not exists: %s" % cmake_cache_path)
        return c_compiler, cxx_compiler

    if (cmake_cache_path.endswith("CMakeCache.txt") == True):
        lines = []
        for line in open(cmake_cache_path, 'r', encoding='utf-8'):
            lines.append(line)

        for line in lines:
            if line.startswith("CMAKE_C_COMPILER:FILEPATH="):
                c_compiler = line.split("=")[-1].strip()
            elif line.startswith("CMAKE_CXX_COMPILER:FILEPATH="):
                cxx_compiler = line.split("=")[-1].strip()
    elif cmake_cache_path.endswith("CMakeConfigureLog.yaml"):
        lines = []
        for line in open(cmake_cache_path, 'r', encoding='utf-8'):
            lines.append(line.rstrip())

        for line in lines:
            if "CMAKE_C_COMPILER=" in line and line.endswith(".exe"):
                c_compiler = line.split("=")[-1].strip()

            if "CMAKE_CXX_COMPILER=" in line and line.endswith(".exe"):
                cxx_compiler = line.split("=")[-1].strip()

    c_compiler = c_compiler.replace("\\\\", "\\").replace("\\", "/")
    cxx_compiler = cxx_compiler.replace("\\\\", "\\").replace("\\", "/")
    return c_compiler, cxx_compiler