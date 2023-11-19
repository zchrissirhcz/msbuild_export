import xml.etree.ElementTree as ET
import os
import pathlib
import re
import json


class Project:
    def __init__(self):
        self.ProjectDir = ""
        self.ProjectPath = ""
        self.XMlName = ""
        self.ItemGroup = []
        self.ItemDefinitionGroup = []

    def FindSourceFiles(self):
        fileList = []
        for v in self.ItemGroup:
            for inc in v.ClCompileSrc:
                fileList.append(inc.Include)
        return fileList

    def FindConfig(self, conf):
        cfgList = []
        for v in self.ItemGroup:
            if len(v.ProjectConfigurationList) > 0:
                cfgList = v.ProjectConfigurationList
                break
        print(cfgList)
        if len(cfgList) == 0:
            raise CustomError(self.ProjectPath + ":not found " + conf)
        found = False
        for v in cfgList:
            if v.Include == conf:
                found = True
                break
        if not found:
            raise CustomError(self.ProjectPath + ":not found " + conf)
        for v in self.ItemDefinitionGroup:
            if conf in v.Condition:
                cl = v.ClCompile
                vlist = conf.split("|")
                configuration = vlist[0]
                platform = vlist[1]
                willReplaceEnv = {
                    "$(ProjectDir)": self.ProjectDir,
                    "$(Configuration)": configuration,
                    "$(ConfigurationName)": configuration,
                    "$(Platform)": platform,
                }
                for env in os.environ:
                    kv = env.split("=")
                    if kv[0] in willReplaceEnv:
                        willReplaceEnv["$(%s)" % kv[0]] = kv[1]
                include = cl.AdditionalIncludeDirectories
                def_ = cl.PreprocessorDefinitions
                for k, v in willReplaceEnv.items():
                    if k in include:
                        include = include.replace(k, v)
                badEnv = re.findall(r'\$\(.+\)', include)
                if len(badEnv) > 0:
                    pass
                    # print("%s:bad env[%s]" % (self.ProjectPath, badEnv), file=os.stderr)
                    # for v in badEnv:
                    #     include = include.replace(v, "")
                return include, def_, None
        return "", "", CustomError("not found " + conf)

    def FindCompilerPath(self, conf):
        return "cl.exe" # TODO: fix me


class ItemGroup:
    def __init__(self):
        self.XMLName = ""
        self.Label = ""
        self.ProjectConfigurationList = []
        self.ClCompileSrc = []


class ProjectConfiguration:
    def __init__(self):
        self.XMLName = ""
        self.Include = ""
        self.Configuration = ""
        self.Platform = ""


class ItemDefinitionGroup:
    def __init__(self):
        self.XMLName = ""
        self.Condition = ""
        self.ClCompile = ClCompile()


class ClCompile:
    def __init__(self):
        self.XMLName = ""
        self.AdditionalIncludeDirectories = ""
        self.PreprocessorDefinitions = ""


class ClCompileSrc:
    def __init__(self):
        self.XMLName = ""
        self.Include = ""


class CompileCommand:
    def __init__(self, directory="", command="", file=""):
        self.Dir = directory
        self.Cmd = command
        self.File = file


badInclude = [
    ";%(AdditionalIncludeDirectories)",
    "%(AdditionalIncludeDirectories);"
]

badDef = [
    ";%(PreprocessorDefinitions)",
    "%(PreprocessorDefinitions);"
]


def NewProject(path):
    pro = Project()
    pro.ProjectPath = os.path.abspath(path)
    pro.ProjectDir = os.path.dirname(pro.ProjectPath)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
            root = ET.fromstring(data)
            xml_data = ET.tostring(root, encoding='utf-8').decode('utf-8')
            pro = xml_to_project(xml_data, pro)
            return pro, None
    except Exception as e:
        return pro, e


def xml_to_project(xml_data, pro):
    root = ET.fromstring(xml_data)
    pro.XMlName = root.tag
    for child in root:
        tagname = child.tag.split('}')[-1]
        print("[DEBUG] child.tag = %s" % tagname)
        if(tagname == "ItemDefinitionGroup"):
            print("wait")
        if tagname == 'ItemGroup':
            item_group = ItemGroup()
            item_group.Label = child.attrib.get('Label', "")
            for item in child:
                if item.tag.endswith('ProjectConfiguration'):
                    project_config = ProjectConfiguration()
                    project_config.Include = item.attrib.get('Include', "")

                    for subitem in item:
                        if subitem.tag.endswith('Configuration'):
                            project_config.Configuration = subitem.text
                        elif subitem.tag.endswith('Platform'):
                            project_config.Platform = subitem.text
                    # project_config.Configuration = item.find('Configuration').text
                    # project_config.Platform = item.find('Platform').text

                    item_group.ProjectConfigurationList.append(project_config)
                elif item.tag.endswith('ClCompile'):
                    cl_compile_src = ClCompileSrc()
                    cl_compile_src.Include = item.attrib.get('Include', "")
                    item_group.ClCompileSrc.append(cl_compile_src)
            pro.ItemGroup.append(item_group)
        elif tagname == 'ItemDefinitionGroup':
            item_def_group = ItemDefinitionGroup()
            item_def_group.Condition = child.attrib.get('Condition', "")
            for item in child:
                if item.tag.endswith('ClCompile'):
                    cl_compile = ClCompile()
                    for subitem in item:
                        if subitem.tag.endswith('AdditionalIncludeDirectories'):
                            cl_compile.AdditionalIncludeDirectories = subitem.text
                        elif subitem.tag.endswith('PreprocessorDefinitions'):
                            cl_compile.PreprocessorDefinitions = subitem.text
                    item_def_group.ClCompile = cl_compile
                    pro.ItemDefinitionGroup.append(item_def_group)
    return pro


import os
import re

class CustomError(Exception):
    pass

def RemoveBadInclude(include):
    badInclude = ["bad1", "bad2"]  # 请替换为实际的坏包含目录列表
    for bad in badInclude:
        include = include.replace(bad, ";.")
    return include

def RemoveBadDefinition(def_):
    badDef = ["baddef1", "baddef2"]  # 请替换为实际的坏定义列表
    for bad in badDef:
        def_ = def_.replace(bad, "")
    return def_
