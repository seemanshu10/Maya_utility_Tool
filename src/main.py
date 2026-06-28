from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout, 
                               QLabel, QListWidget, QHBoxLayout, QVBoxLayout, 
                               QRadioButton, QTabWidget, QComboBox, QStatusBar, QGroupBox,
                               QCheckBox)
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
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Add Labels to the Grid Layout 
        objects_grid_layout = QGridLayout()

        source_obj_label = QLabel("Source Objects")
        target_obj_label = QLabel("Target Objects")

        source_obj_list = QListWidget()
        target_obj_list = QListWidget()

        # Source Objects Side 
        self.load_select_obj_source_button = QPushButton("Load Selected Object")
        self.clear_list_source_button = QPushButton("Clear")

        source_buttons_layout = QHBoxLayout()
        source_buttons_layout.addWidget(self.load_select_obj_source_button)
        source_buttons_layout.addWidget(self.clear_list_source_button)

        source_column_layout = QVBoxLayout()
        source_column_layout.addWidget(source_obj_label, alignment=Qt.AlignCenter)
        source_column_layout.addWidget(source_obj_list)
        source_column_layout.addLayout(source_buttons_layout)

        # target objects Side
        self.load_target_obj_button = QPushButton("Load Selected Object")
        self.clear_list_target_button = QPushButton("Clear")

        target_buttons_layout = QHBoxLayout()
        target_buttons_layout.addWidget(self.load_target_obj_button)
        target_buttons_layout.addWidget(self.clear_list_target_button)

        target_column_layout = QVBoxLayout()
        target_column_layout.addWidget(target_obj_label, alignment=Qt.AlignCenter)
        target_column_layout.addWidget(target_obj_list)
        target_column_layout.addLayout(target_buttons_layout)

        # Adding Both Source and target layout in Grid Layout  
        objects_grid_layout.addLayout(source_column_layout, 0, 0)
        objects_grid_layout.addLayout(target_column_layout, 0, 1)

        # creating Relationship by order 
        relationship_layout = QHBoxLayout()
        relationship_label = QLabel("Relationship Label: ")
        radio_button_order = QRadioButton("Order")
        radio_button_name = QRadioButton("Name")

        relationship_layout.addWidget(relationship_label, alignment=Qt.AlignRight)
        relationship_layout.addWidget(radio_button_order, alignment=Qt.AlignLeft)
        relationship_layout.addWidget(radio_button_name, alignment=Qt.AlignLeft)

        # creating TabWidget 
        main_tab_widget = QTabWidget()
        first_tab = QWidget()
        second_tab = QWidget()
        third_tab = QWidget()

        # Creating Constraint tab 
        constraint_main_layout = QVBoxLayout()

        # Constraint Type 
        constraint_type_layout = QHBoxLayout()
        constraint_type_label = QLabel("Constraint Type: ")
        constraint_type_combobox = QComboBox()
        constraint_type_combobox.addItem("Parent Constraint")
        constraint_type_combobox.addItem("Point Constraint")
        constraint_type_combobox.addItem("Orient Constraint")
        constraint_type_combobox.addItem("Scale Constraint")

        constraint_type_layout.addWidget(constraint_type_label, alignment=Qt.AlignRight)
        constraint_type_layout.addWidget(constraint_type_combobox, alignment=Qt.AlignLeft)

        # maintain offset Options Creation 
        maintain_offset_layout = QHBoxLayout()
        maintain_offset = QLabel("Maintain Offset:")
        offset_radio_on = QRadioButton("On")
        offset_radio_off = QRadioButton("Off")

        maintain_offset_layout.addWidget(maintain_offset, alignment=Qt.AlignRight)
        maintain_offset_layout.addWidget(offset_radio_on, alignment=Qt.AlignLeft)
        maintain_offset_layout.addWidget(offset_radio_off, alignment=Qt.AlignLeft)

        # constraint adding everything to main Tab widget 
        constraint_main_layout.addLayout(constraint_type_layout) 
        constraint_main_layout.addLayout(maintain_offset_layout)

        first_tab.setLayout(constraint_main_layout)  

        main_tab_widget.addTab(first_tab, "Constraint")
        main_tab_widget.addTab(second_tab, "Connnection")
        main_tab_widget.addTab(third_tab, "Copy Skin")

        # creation constraint Axes Group 
        constraint_axes_group = QGroupBox("Constraint Axes ")
        constraint_options_layout = QGridLayout()
        translate_label = QLabel("Translate ")
        translate_all_checkbox = QCheckBox("All")
        translate_x_checkbox = QCheckBox("X")
        translate_y_checkbox = QCheckBox("Y")
        translate_z_checkbox = QCheckBox("Z")

        rotate_label = QLabel("Rotate ")
        rotate_all_checkbox = QCheckBox("All")
        rotate_x_checkbox = QCheckBox("X")
        rotate_y_checkbox = QCheckBox("Y")
        rotate_z_checkbox = QCheckBox("Z")

        constraint_options_layout.addWidget(translate_label, 0, 0, alignment=Qt.AlignRight)
        constraint_options_layout.addWidget(translate_all_checkbox, 0, 1)
        constraint_options_layout.addWidget(translate_x_checkbox, 0, 2)
        constraint_options_layout.addWidget(translate_y_checkbox, 0, 3)
        constraint_options_layout.addWidget(translate_z_checkbox, 0, 4)

        constraint_options_layout.addWidget(rotate_label, 1, 0, alignment=Qt.AlignRight)
        constraint_options_layout.addWidget(rotate_all_checkbox, 1, 1)
        constraint_options_layout.addWidget(rotate_x_checkbox, 1, 2)
        constraint_options_layout.addWidget(rotate_y_checkbox, 1, 3)
        constraint_options_layout.addWidget(rotate_z_checkbox, 1, 4)
        
        constraint_axes_group.setLayout(constraint_options_layout)
        constraint_main_layout.addWidget(constraint_axes_group)

        # Constraint Button creation 
        create_constraint_btn = QPushButton("Create Constraint") 
        constraint_main_layout.addWidget(create_constraint_btn)

        # addLAyouts in main_layout
        main_layout.addLayout(objects_grid_layout)    
        main_layout.addLayout(relationship_layout)  
        main_layout.addWidget(main_tab_widget)
        
        central_widget.setLayout(main_layout)

        # Status bar  
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)

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
