from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout, 
                               QLabel, QListWidget, QHBoxLayout, QVBoxLayout, 
                               QRadioButton, QTabWidget, QComboBox, QStatusBar, QGroupBox,
                               QCheckBox, QFormLayout)
from PySide2.QtCore import Qt

class RiggingUtilityTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rigging Utility Tool")
        self.setGeometry(100, 200, 500, 500)
        self.initUI()

    def main_ui(self):

        # Add Labels to the Grid Layout 
        self.objects_grid_layout = QGridLayout()

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
        self.objects_grid_layout.addLayout(source_column_layout, 0, 0)
        self.objects_grid_layout.addLayout(target_column_layout, 0, 1)

        # creating Relationship by order 
        self.relationship_layout = QHBoxLayout()
        relationship_label = QLabel("Relationship Label: ")
        radio_button_order = QRadioButton("Order")
        radio_button_name = QRadioButton("Name")

        radio_button_order.setChecked(True)
        
        self.relationship_layout.addWidget(relationship_label, alignment=Qt.AlignRight)
        self.relationship_layout.addWidget(radio_button_order, alignment=Qt.AlignLeft)
        self.relationship_layout.addWidget(radio_button_name, alignment=Qt.AlignLeft)

        # creating TabWidget 
        self.main_tab_widget = QTabWidget()
        self.first_tab = QWidget()
        self.second_tab = QWidget()
        self.third_tab = QWidget()

        self.main_tab_widget.addTab(self.first_tab, "Constraint")
        self.main_tab_widget.addTab(self.second_tab, "Connnection")
        self.main_tab_widget.addTab(self.third_tab, "Copy Skin")

        # self.constraint_tab_ui()

    def constraint_tab_ui(self):
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
        offset_radio_off.setChecked(True)

        maintain_offset_layout.addWidget(maintain_offset, alignment=Qt.AlignRight)
        maintain_offset_layout.addWidget(offset_radio_on, alignment=Qt.AlignLeft)
        maintain_offset_layout.addWidget(offset_radio_off, alignment=Qt.AlignLeft)

        # constraint adding everything to main Tab widget 
        constraint_main_layout.addLayout(constraint_type_layout) 
        constraint_main_layout.addLayout(maintain_offset_layout)

        self.first_tab.setLayout(constraint_main_layout)  

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

        # addLAyouts in main_layout
        self.main_layout.addLayout(self.objects_grid_layout)    
        self.main_layout.addLayout(self.relationship_layout)  
        self.main_layout.addWidget(self.main_tab_widget)
        
        self.central_widget.setLayout(self.main_layout)

        # Status bar  
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)

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

    def copyskin_tab_ui(self):
        # create The copy skin llayout 
        copyskin_tab_layout = QVBoxLayout()
        copy_skin_group = QGroupBox("Skin Options ")

        self.copyskin_form_layout = QFormLayout()

        self.association_label = QLabel("Surface Association: ")
        self.closest_point_radio_btn = QRadioButton("Closest Point Surface")
        self.ray_cast_radio_btn = QRadioButton("Ray Cast")
        self.closest_component_radio_btn = QRadioButton("Closest Component")
        self.uv_space_radio_btn = QRadioButton("UV Space")

        self.influence_label_1 = QLabel("Influence Association 1: ")
        self.influence_label_2 = QLabel("Influence Association 2: ")
        self.influence_label_3 = QLabel("Influence Association 3: ")
        
        items = ["None", "Closest Bone", "Closest Joint", "One To One", "Label", "Name" ]

        self.influence_combo_box_1 = QComboBox()
        self.influence_combo_box_1.addItems(items)

        self.influence_combo_box_2 = QComboBox()
        self.influence_combo_box_2.addItems(items)

        self.influence_combo_box_3 = QComboBox()
        self.influence_combo_box_3.addItems(items)

        self.copyskin_form_layout.addRow(self.association_label ,self.closest_point_radio_btn)
        self.copyskin_form_layout.addRow("" ,self.ray_cast_radio_btn)
        self.copyskin_form_layout.addRow("" ,self.closest_component_radio_btn)
        self.copyskin_form_layout.addRow("" ,self.uv_space_radio_btn)

        self.copyskin_form_layout.addRow(self.influence_label_1, self.influence_combo_box_1)
        self.copyskin_form_layout.addRow(self.influence_label_2, self.influence_combo_box_2)
        self.copyskin_form_layout.addRow(self.influence_label_3, self.influence_combo_box_3)

        self.copy_skin_btn = QPushButton("Copy Skin")

        copy_skin_group.setLayout(self.copyskin_form_layout)
        copyskin_tab_layout.addWidget(copy_skin_group)
        copyskin_tab_layout.addWidget(self.copy_skin_btn)
        self.third_tab.setLayout(copyskin_tab_layout)

    def initUI(self):
        # Create a basic central widget
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_ui()
        self.constraint_tab_ui()
        self.connection_tab_ui()
        self.copyskin_tab_ui()
        # self.central_widget.setLayout(self.main_layout)
