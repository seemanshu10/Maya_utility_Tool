from src.ui import main_window

from PySide2.QtWidgets import QWidget
from maya import OpenMayaUI as omui
import shiboken2

import importlib
import os
import sys

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QWidget)


def reload_project(project_root):
    project_root = os.path.abspath(project_root)

    for name, module in list(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if path and os.path.abspath(path).startswith(project_root): 
            try:
                importlib.reload(module)
                print(f"Reloaded {name}")
            except Exception as e:
                print(f"Failed {name}: {e}")
    
def show_window():
    global my_window
    # check if already window open close
    try:
        my_window.close()
        my_window.deleteLater()

    except:
        pass

    maya_main_window = get_maya_main_window()
    my_window = main_window.RiggingUtilityTool(parent=maya_main_window)
    print("I ran again ")
    my_window.show()

