import os
import re
import shutil
import prj

class Solution:
    def __init__(self):
        self.SolutionDir = ""
        self.ProjectList = []
        self.vs_version = ""

    def CompileCommandsJson(self, conf, c_compiler, cxx_compiler):
        cmdList = []

        for pro in self.ProjectList:
            src_files = pro.FindSourceFiles()
            for f in src_files:
                item = prj.CompileCommand()
                item.directory = pro.ProjectDir
                item.file = f

                inc, definition, err = pro.FindConfig(conf)
                if err:
                    return cmdList, err
                will_replace_env = {
                    "$(SolutionDir)": self.SolutionDir,
                }
                for k, v in will_replace_env.items():
                    if k in inc:
                        inc = inc.replace(k, v)
                definition = prj.RemoveBadDefinition(definition)
                definition = preappend(definition, "-D")

                inc = prj.RemoveBadInclude(inc)
                inc = preappend(inc, "-I")

                if f.endswith(".c"):
                    compiler = c_compiler
                elif f.endswith(".cpp") or f.endswith(".cc") or f.endswith(".cxx"):
                    compiler = cxx_compiler
                cmd = compiler + " " + definition + " " + inc + " -c " + f
                item.command = cmd

                cmdList.append(item)

        return cmdList, None

def NewSln(path):
    sln = Solution()
    err = None

    sln.SolutionDir = os.path.dirname(os.path.abspath(path))
    sln.vs_version = find_vs_version(path)
    projectFiles, err = find_all_project(path)
    if err:
        print(err)
        return sln, err
    if len(projectFiles) == 0:
        return sln, "not found project file"

    for projectPath in projectFiles:
        if projectPath in ["ALL_BUILD.vcxproj", "ZERO_CHECK.vcxproj", "INSTALL.vcxproj", "arcpkg.vcxproj"]:
            continue
        elif projectPath in ["arcpkg.vcxproj", "arcpkg-clean.vcxproj", "arcpkg-export.vcxproj", "arcpkg-pack", "arcpkg-update.vcxproj", "arcpkg-upload.vcxproj"]:
            continue
        elif projectPath.startswith("arcpkg-") and projectPath.endswith(".vcxproj"):
            continue
        fullpath = os.path.join(sln.SolutionDir, projectPath)
        if os.path.exists(fullpath) == False:
            continue
        pro, err = prj.NewProject(os.path.join(sln.SolutionDir, projectPath))
        if err:
            return sln, err
        sln.ProjectList.append(pro)
    return sln, None

def find_vs_version(sln_path):
    # Visual Studio Version 17
    lines = []
    for line in open(sln_path, 'r', encoding='utf-8'):
        lines.append(line)
    vs_version = ""
    for line in lines:
        if line.startswith("# Visual Studio Version 17"):
            vs_version = "vs2022"
            break
        elif line.startswith("# Visual Studio Version 16"):
            vs_version = "vs2019"
            break
        elif line.startswith("# Visual Studio Version 15"):
            vs_version = "vs2017"
            break
        elif line.startswith("# Visual Studio Version 14"):
            vs_version = "vs2015"
            break
    return vs_version

def find_all_project(path):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            data = file.read()
            #files = re.findall(r'[^\"]\"[^\"]+\\.vcxproj\"', data)
            files = re.findall(r'\b[\w\\-]+\.vcxproj\b', data)
            fileList = [file.replace('"', '').strip() for file in files]
            return fileList, None
    except Exception as e:
        return [], e


def preappend(seped_string, append):
    def_list = seped_string.split(";")
    output = ""
    for v in def_list:
        v = append + v + " "
        output += v
    return output
