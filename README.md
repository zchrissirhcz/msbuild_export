# msbuild_export

Extract `compile_commands.json` from `.sln` file (required) and CMakeCache.txt (optional), without compilation.

Inspired by [vs_export](https://github.com/paopaol/vs_export) but re-write in Python.

```cmd
python msbuild_export.py -s <path> -c <configuration>

Where:
            -s   path                        sln filename
            -f   configuration               project configuration,eg Debug|Win32.
                                             default Release|x64
            -c   cmake_cache                 path to CMakeCache.txt
```

Example:

```bash
python msbuild_export.py  -s  opengv.sln  -c "Release|x64"
python msbuild_export.py  -s  D:/github/ncnn/build/vs2022-x64/ncnn.sln  -f "Release|x64" -c "D:/github/ncnn/build/vs2022-x64/CMakeCache.txt"
python msbuild_export.py  -s  D:/github/ncnn/build/vs2022-x64/ncnn.sln  -f "Release|x64" -c "D:/github/ncnn/build/vs2022-x64/CMakeFiles/CMakeConfigureLog.yaml"
```
