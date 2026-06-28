import importlib
import os
import sys

def reload_project(project_root):
    project_root = os.path.abspath(project_root)

    for name, module in list(sys.modules.items()):
        # print(f"{name}, {module}")
        path = getattr(module, "__file__", None)
        # print(path)
        if os.path.commonpath([path, project_root]) == project_root:
            try:
                importlib.reload(module)
                print(f"Reloaded {name}")
                print(path)
            except Exception as e:
                print(f"Failed {name}: {e}")

reload_project(r"D:\PipelineTD\Maya_utility_Tool")