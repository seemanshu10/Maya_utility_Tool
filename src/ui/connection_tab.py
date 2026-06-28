from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout, 
                               QLabel, QListWidget, QHBoxLayout, QVBoxLayout, 
                               QRadioButton, QTabWidget, QComboBox, QStatusBar, QGroupBox,
                               QCheckBox, QFormLayout)
from PySide2.QtCore import Qt

def connection_tab_ui(self):
        # create The connection tab
        connection_tab_layout = QVBoxLayout()

        # creation constraint Axes Group 
        self.connection_axes_group = QGroupBox("Constraint Axes ")
        self.connection_options_layout = QGridLayout()
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

        scale_label = QLabel("Scale ")
        scale_all_checkbox = QCheckBox("All")
        scale_x_checkbox = QCheckBox("X")
        scale_y_checkbox = QCheckBox("Y")
        scale_z_checkbox = QCheckBox("Z")

        self.connection_options_layout.addWidget(translate_label, 0, 0, alignment=Qt.AlignRight)
        self.connection_options_layout.addWidget(translate_all_checkbox, 0, 1)
        self.connection_options_layout.addWidget(translate_x_checkbox, 0, 2)
        self.connection_options_layout.addWidget(translate_y_checkbox, 0, 3)
        self.connection_options_layout.addWidget(translate_z_checkbox, 0, 4)

        self.connection_options_layout.addWidget(rotate_label, 1, 0, alignment=Qt.AlignRight)
        self.connection_options_layout.addWidget(rotate_all_checkbox, 1, 1)
        self.connection_options_layout.addWidget(rotate_x_checkbox, 1, 2)
        self.connection_options_layout.addWidget(rotate_y_checkbox, 1, 3)
        self.connection_options_layout.addWidget(rotate_z_checkbox, 1, 4)

        self.connection_options_layout.addWidget(scale_label, 2, 0, alignment=Qt.AlignRight)
        self.connection_options_layout.addWidget(scale_all_checkbox, 2, 1)
        self.connection_options_layout.addWidget(scale_x_checkbox, 2, 2)
        self.connection_options_layout.addWidget(scale_y_checkbox, 2, 3)
        self.connection_options_layout.addWidget(scale_z_checkbox, 2, 4)

        # All connection Atrributes List 
        self.grid_attributes_layout = QGridLayout()
        self.all_connection_label = QLabel("All Connections Attributes")
        self.all_connection_listwidget = QListWidget()
        self.selected_attributes_label = QLabel("Selected Attributes")
        self.selected_attributes_listwidget = QListWidget()

        self.add_attributes_button = QPushButton("ADD")
        self.remove_item_button = QPushButton("Remove Item")
        self.clear_attributes_button = QPushButton("Clear")

        self.grid_attributes_layout.addWidget(self.all_connection_label, 0, 0)
        self.grid_attributes_layout.addWidget(self.selected_attributes_label, 0, 1)
        self.grid_attributes_layout.addWidget(self.all_connection_listwidget, 1, 0)
        self.grid_attributes_layout.addWidget(self.selected_attributes_listwidget, 1, 1, 1, 2)
        self.grid_attributes_layout.addWidget(self.add_attributes_button, 2, 0, 1, 1)
        self.grid_attributes_layout.addWidget(self.remove_item_button, 2, 1)
        self.grid_attributes_layout.addWidget(self.clear_attributes_button, 2, 2)

        # Create connection buttons 
        self.create_connection_button = QPushButton("Create Connections")

        connection_tab_layout.addWidget(self.connection_axes_group)
        connection_tab_layout.addLayout(self.grid_attributes_layout)
        connection_tab_layout.addWidget(self.create_connection_button)

        self.connection_axes_group.setLayout(self.connection_options_layout)
        self.second_tab.setLayout(connection_tab_layout)