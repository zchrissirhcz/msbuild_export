# msbuild_export

Extract `compile_commands.json` from `.sln` files, without compilation.

Inspired by [vs_export](https://github.com/paopaol/vs_export) but re-write in Python.

```cmd
msbuild_export -s <path> -c <configuration>

Where:
            -s   path                        sln filename
            -c   configuration               project configuration,eg Debug|Win32.
                                             default Debug|x64
```

Example:

```
msbuild_export  -s  opengv.sln  -c "Release|x64"
```
