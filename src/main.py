from PySide2.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout, QLabel, QListWidget, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import Qt

from maya import OpenMayaUI as omui
import shiboken2

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QWidget)

class RiggingUtilityTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rigging Utility Tool")

        # Create a basic central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Add Labels to the Grid Layout 
        objects_grid_layout = QGridLayout()

        source_obj_label = QLabel("Source Objects")
        target_obj_label = QLabel("Target Objects")

        source_obj_list = QListWidget()
        target_obj_list = QListWidget()

        # Source Objects Side 
        load_select_obj_source_button = QPushButton("Load Selected Object")
        clear_list_source_button = QPushButton("Clear")

        source_buttons_layout = QHBoxLayout()
        source_buttons_layout.addWidget(load_select_obj_source_button)
        source_buttons_layout.addWidget(clear_list_source_button)

        source_column_layout = QVBoxLayout()
        source_column_layout.addWidget(source_obj_label, alignment=Qt.AlignCenter)
        source_column_layout.addWidget(source_obj_list)
        source_column_layout.addLayout(source_buttons_layout)

        # target objects Side
        load_target_obj_button = QPushButton("Load Selected Object")
        clear_list_target_button = QPushButton("Clear")

        target_buttons_layout = QHBoxLayout()
        target_buttons_layout.addWidget(load_target_obj_button)
        target_buttons_layout.addWidget(clear_list_target_button)

        target_column_layout = QVBoxLayout()
        target_column_layout.addWidget(target_obj_label, alignment=Qt.AlignCenter)
        target_column_layout.addWidget(target_obj_list)
        target_column_layout.addLayout(target_buttons_layout)

        # Adding Both Source and target layout in Grid Layout  
        objects_grid_layout.addLayout(source_column_layout, 0, 0)
        objects_grid_layout.addLayout(target_column_layout, 0, 1)
        
        central_widget.setLayout(objects_grid_layout)

def show_window():
    global my_window

    # check if already window open close
    try:
        my_window.close()
        my_window.deleteLater()
    except:
        pass

    maya_main_window = get_maya_main_window()
    my_window = RiggingUtilityTool(parent=maya_main_window)
    
    my_window.show()

show_window()


