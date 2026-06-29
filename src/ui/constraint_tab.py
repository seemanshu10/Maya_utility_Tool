from PySide2.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QRadioButton, QGroupBox,
    QGridLayout, QCheckBox, QPushButton
)
from PySide2.QtCore import Qt


class ConstraintUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.constraint_tab_ui()

    def constraint_tab_ui(self):
        constraint_main_layout = QVBoxLayout(self)

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
        offset_radio_off.setChecked(True)

        maintain_offset_layout.addWidget(maintain_offset, alignment=Qt.AlignRight)
        maintain_offset_layout.addWidget(offset_radio_on, alignment=Qt.AlignLeft)
        maintain_offset_layout.addWidget(offset_radio_off, alignment=Qt.AlignLeft)

        # constraint adding everything to main Tab widget 
        constraint_main_layout.addLayout(constraint_type_layout) 
        constraint_main_layout.addLayout(maintain_offset_layout)

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

        scale_label = QLabel("Scale ")
        scale_all_checkbox = QCheckBox("All")
        scale_x_checkbox = QCheckBox("X")
        scale_y_checkbox = QCheckBox("Y")
        scale_z_checkbox = QCheckBox("Z")

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

        constraint_options_layout.addWidget(scale_label, 2, 0, alignment=Qt.AlignRight)
        constraint_options_layout.addWidget(scale_all_checkbox, 2, 1)
        constraint_options_layout.addWidget(scale_x_checkbox, 2, 2)
        constraint_options_layout.addWidget(scale_y_checkbox, 2, 3)
        constraint_options_layout.addWidget(scale_z_checkbox, 2, 4)
        
        constraint_axes_group.setLayout(constraint_options_layout)
        constraint_main_layout.addWidget(constraint_axes_group)

        # Constraint Button creation 
        create_constraint_btn = QPushButton("Create Constraint") 
        constraint_main_layout.addWidget(create_constraint_btn)