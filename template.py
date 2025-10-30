# Code from clint project
import os
import json


class Template:
    def __init__(self, path):
        self.path = path

        with open(self.path, "r") as f:
            self.template = json.load(f)

        # Modified keywords to match new template
        self.keyWords = {
            "files": ["file_names"],
            "dir": ["dir_name", "dir_contents"],
        }

        self.file_dict = {}

    def printTemplate(self):
        print(self.template)

    def templateGet(self, name: str):

        return self.template.get(name)

    def visulizeTemplate(self):
        def printNested(item, level=0):
            indent = "  " * level
            if isinstance(item, dict):
                for key, value in item.items():
                    print(f"{indent}{key}:")
                    printNested(value, level + 1)
            elif isinstance(item, list):
                for value in item:
                    printNested(value, level + 1)
            else:
                print(f"{indent}{item}")

        printNested(self.template)

    def makeFromTemplate(self):
        data = self.template

        def makeStruct(data, parentPath=""):
            if isinstance(data, dict):
                currentPath = parentPath
                for key, value in data.items():
                    if key == "dir":
                        for item in value:
                            if "dir_name" in item:
                                print(f"Making Dir: {item["dir_name"]}")
                                dirPath = os.path.join(
                                    currentPath, item["dir_name"])
                                os.makedirs(dirPath, exist_ok=True)
                                makeStruct(item, dirPath)
                            elif "dir_contents" in item:
                                makeStruct(item["dir_contents"], dirPath)
                    elif key == "files":
                        prevFile = None
                        for item in value:
                            if "file_names" in item:
                                print(f"Making Files in: {currentPath}")
                                # Modified to correctly get file names
                                files = value["file_names"]
                                for file in files:
                                    filePath = os.path.join(currentPath, file)
                                    self.file_dict[file] = filePath
                                    prevFile = filePath
                                    with open(filePath, "w") as f:
                                        pass
                    else:
                        makeStruct(value, currentPath)

            elif isinstance(data, list):
                for item in data:
                    makeStruct(item, parentPath)

        makeStruct(data)
        print("Created Directory with following structure")

        self.visulizeTemplate()


if __name__ == "__main__":
    template = Template(path="templates/test.json")
    template.makeFromTemplate()
    file_names = template.file_dict.keys()

    for file in file_names:
        print(f"File : {file}, file path : {template.file_dict.get(file)}")
