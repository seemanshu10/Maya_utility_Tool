from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout, 
                               QLabel, QListWidget, QHBoxLayout, QVBoxLayout, 
                               QRadioButton, QTabWidget, QComboBox, QStatusBar, QGroupBox,
                               QCheckBox, QFormLayout, QStyle)
from PySide2.QtCore import Qt, Slot

# maya Python API 
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import shiboken2

ITEMS = ["None", "Closest Bone", "Closest Joint", "One To One", "Label", "Name" ]

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QWidget)

class RiggingUtilityTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rigging Utility Tool")
        self.setGeometry(100, 200, 500, 600)
        self.initUI()

    def initUI(self):
        # Create a basic central widget
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_ui()
        self.constraint_tab_ui()
        self.connection_tab_ui()
        self.copyskin_tab_ui()

    def main_ui(self):

        # Add Labels to the Grid Layout 
        self.objects_grid_layout = QGridLayout()

        source_obj_label = QLabel("Source Objects")
        target_obj_label = QLabel("Target Objects")

        self.source_obj_list = QListWidget()
        self.source_obj_list.setMinimumHeight(200)
        self.target_obj_list = QListWidget()
        self.target_obj_list.setMinimumHeight(200)

        self.source_move_up_btn = QPushButton()
        self.source_move_up_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.source_move_up_btn.setToolTip("Move up")
        self.source_move_down_btn = QPushButton()
        self.source_move_down_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.source_move_down_btn.setToolTip("Move down")

        self.target_move_up_btn = QPushButton()
        self.target_move_up_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.target_move_up_btn.setToolTip("Move up")
        self.target_move_down_btn = QPushButton()
        self.target_move_down_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.target_move_down_btn.setToolTip("Move down")

        # Source Objects Side 
        self.load_select_obj_source_button = QPushButton("Load Selected Objects")
        self.clear_list_source_button = QPushButton("Clear")

        source_buttons_layout = QHBoxLayout()
        source_buttons_layout.addWidget(self.load_select_obj_source_button)
        source_buttons_layout.addWidget(self.clear_list_source_button)

        source_list_row_layout = QHBoxLayout()
        source_list_row_layout.addWidget(self.source_obj_list)

        source_button_column_layout = QVBoxLayout()
        source_button_column_layout.addWidget(self.source_move_up_btn)
        source_button_column_layout.addWidget(self.source_move_down_btn)
        source_list_row_layout.addLayout(source_button_column_layout)

        source_column_layout = QVBoxLayout()
        source_column_layout.addWidget(source_obj_label, alignment=Qt.AlignCenter)
        source_column_layout.addLayout(source_list_row_layout)
        source_column_layout.addLayout(source_buttons_layout)

        # connection Source List buttons
        self.load_select_obj_source_button.clicked.connect(lambda: self.load_selected_objects(self.source_obj_list))
        self.clear_list_source_button.clicked.connect(lambda: self.clear_list(self.source_obj_list))
        self.source_move_up_btn.clicked.connect(lambda: self.move_selected_item_up(self.source_obj_list))
        self.source_move_down_btn.clicked.connect(lambda: self.move_selected_item_down(self.source_obj_list))

        # target objects Side
        self.load_target_obj_button = QPushButton("Load Selected Objects")
        self.clear_list_target_button = QPushButton("Clear")

        # connections Target list buttons 
        self.load_target_obj_button.clicked.connect(lambda: self.load_selected_objects(self.target_obj_list))
        self.clear_list_target_button.clicked.connect(lambda: self.clear_list(self.target_obj_list))
        self.target_move_up_btn.clicked.connect(lambda: self.move_selected_item_up(self.target_obj_list))
        self.target_move_down_btn.clicked.connect(lambda: self.move_selected_item_down(self.target_obj_list))

        target_buttons_layout = QHBoxLayout()
        target_buttons_layout.addWidget(self.load_target_obj_button)
        target_buttons_layout.addWidget(self.clear_list_target_button)

        target_list_row_layout = QHBoxLayout()
        target_list_row_layout.addWidget(self.target_obj_list)

        target_button_column_layout = QVBoxLayout()
        target_button_column_layout.addWidget(self.target_move_up_btn)
        target_button_column_layout.addWidget(self.target_move_down_btn)
        target_list_row_layout.addLayout(target_button_column_layout)

        target_column_layout = QVBoxLayout()
        target_column_layout.addWidget(target_obj_label, alignment=Qt.AlignCenter)
        target_column_layout.addLayout(target_list_row_layout)
        target_column_layout.addLayout(target_buttons_layout)

        # Adding Both Source and target layout in Grid Layout  
        self.objects_grid_layout.addLayout(source_column_layout, 0, 0)
        self.objects_grid_layout.addLayout(target_column_layout, 0, 1)

        # creating Relationship by order 
        self.match_group = QHBoxLayout()

        # Reduce the space around the layout
        self.match_group.setContentsMargins(150, 0, 0, 0)

        # Reduce the space between widgets
        self.match_group.setSpacing(10)     

        relationship_label = QLabel("Match by:")

        self.radio_button_order = QRadioButton("Order")
        self.radio_button_name = QRadioButton("Name")
        self.radio_button_order.setChecked(True)

        self.match_group.addWidget(relationship_label)
        self.match_group.addWidget(self.radio_button_order)
        self.match_group.addWidget(self.radio_button_name)

        # Push everything to the left instead of spreading out
        self.match_group.addStretch()

        # creating TabWidget 
        self.main_tab_widget = QTabWidget()
        self.first_tab = QWidget()
        self.second_tab = QWidget()
        self.third_tab = QWidget()

        self.main_tab_widget.addTab(self.first_tab, "Constraint")
        self.main_tab_widget.addTab(self.second_tab, "Connnection")
        self.main_tab_widget.addTab(self.third_tab, "Copy Skin")

        # self.constraint_tab_ui()
        # Status bar  
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)

    def constraint_tab_ui(self):
        # Creating Constraint tab 
        constraint_main_layout = QVBoxLayout()

        # Constraint Type 
        constraint_type_layout = QHBoxLayout()
        constraint_type_label = QLabel("Constraint Type: ")
        self.constraint_type_combobox = QComboBox()
        self.constraint_type_combobox.addItem("Parent Constraint")
        self.constraint_type_combobox.addItem("Point Constraint")
        self.constraint_type_combobox.addItem("Orient Constraint")
        self.constraint_type_combobox.addItem("Scale Constraint")

        constraint_type_layout.addWidget(constraint_type_label, alignment=Qt.AlignRight)
        constraint_type_layout.addWidget(self.constraint_type_combobox, alignment=Qt.AlignLeft)

        # maintain offset Options Creation 
        maintain_offset_layout = QHBoxLayout()
        maintain_offset = QLabel("Maintain Offset:")
        self.offset_radio_on = QRadioButton("On")
        self.offset_radio_off = QRadioButton("Off")
        self.offset_radio_off.setChecked(True)

        maintain_offset_layout.addWidget(maintain_offset, alignment=Qt.AlignRight)
        maintain_offset_layout.addWidget(self.offset_radio_on, alignment=Qt.AlignLeft)
        maintain_offset_layout.addWidget(self.offset_radio_off, alignment=Qt.AlignLeft)

        # constraint adding everything to main Tab widget 
        constraint_main_layout.addLayout(constraint_type_layout) 
        constraint_main_layout.addLayout(maintain_offset_layout)

        self.first_tab.setLayout(constraint_main_layout)  

        # creation constraint Axes Group 
        constraint_axes_group = QGroupBox("Constraint Axes ")
        constraint_options_layout = QGridLayout()
        translate_label = QLabel("Translate ")
        self.translate_all_checkbox_constraint = QCheckBox("All")
        self.translate_x_checkbox_constraint = QCheckBox("X")
        self.translate_y_checkbox_constraint = QCheckBox("Y")
        self.translate_z_checkbox_constraint = QCheckBox("Z")

        rotate_label = QLabel("Rotate ")
        self.rotate_all_checkbox_constraint = QCheckBox("All")
        self.rotate_x_checkbox_constraint = QCheckBox("X")
        self.rotate_y_checkbox_constraint = QCheckBox("Y")
        self.rotate_z_checkbox_constraint = QCheckBox("Z")

        scale_label = QLabel("Scale ")
        self.scale_all_checkbox_constraint = QCheckBox("All")
        self.scale_x_checkbox_constraint = QCheckBox("X")
        self.scale_y_checkbox_constraint = QCheckBox("Y")
        self.scale_z_checkbox_constraint = QCheckBox("Z")

        constraint_options_layout.addWidget(translate_label, 0, 0, alignment=Qt.AlignRight)
        constraint_options_layout.addWidget(self.translate_all_checkbox_constraint, 0, 1)
        constraint_options_layout.addWidget(self.translate_x_checkbox_constraint, 0, 2)
        constraint_options_layout.addWidget(self.translate_y_checkbox_constraint, 0, 3)
        constraint_options_layout.addWidget(self.translate_z_checkbox_constraint, 0, 4)

        constraint_options_layout.addWidget(rotate_label, 1, 0, alignment=Qt.AlignRight)
        constraint_options_layout.addWidget(self.rotate_all_checkbox_constraint, 1, 1)
        constraint_options_layout.addWidget(self.rotate_x_checkbox_constraint, 1, 2)
        constraint_options_layout.addWidget(self.rotate_y_checkbox_constraint, 1, 3)
        constraint_options_layout.addWidget(self.rotate_z_checkbox_constraint, 1, 4)

        constraint_options_layout.addWidget(scale_label, 2, 0, alignment=Qt.AlignRight)
        constraint_options_layout.addWidget(self.scale_all_checkbox_constraint, 2, 1)
        constraint_options_layout.addWidget(self.scale_x_checkbox_constraint, 2, 2)
        constraint_options_layout.addWidget(self.scale_y_checkbox_constraint, 2, 3)
        constraint_options_layout.addWidget(self.scale_z_checkbox_constraint, 2, 4)
        
        constraint_axes_group.setLayout(constraint_options_layout)
        constraint_main_layout.addWidget(constraint_axes_group)

        # Constraint Button creation 
        self.create_constraint_btn = QPushButton("Create Constraint")
        self.create_constraint_btn.setFixedSize(160, 40)
        self.create_constraint_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #2563EB;
            }

            QPushButton:pressed {
                background-color: #1D4ED8;
            }

            QPushButton:disabled {
                background-color: #9CA3AF;
                color: #E5E7EB;
            }
        """)

        constraint_main_layout.addWidget(self.create_constraint_btn, alignment=Qt.AlignCenter)

        # added all enable disbale 
        if self.translate_all_checkbox_constraint.isChecked():
            self.translate_x_checkbox_constraint.setEnabled(False)
            self.translate_y_checkbox_constraint.setEnabled(False)
            self.translate_z_checkbox_constraint.setEnabled(False)

        # addLAyouts in main_layout
        self.main_layout.addLayout(self.objects_grid_layout)    
        self.main_layout.addLayout(self.match_group)  
        self.main_layout.addWidget(self.main_tab_widget)
        
        self.central_widget.setLayout(self.main_layout)
        self.create_constraint_btn.clicked.connect(self.create_constraints)
        self.translate_all_checkbox_constraint.toggled.connect(self.update_translate_checkboxes)
        self.rotate_all_checkbox_constraint.toggled.connect(self.update_rotate_checkboxes)
        self.scale_all_checkbox_constraint.toggled.connect(self.update_scale_checkboxes)
   
    def connection_tab_ui(self):
        # create The connection tab
        connection_tab_layout = QVBoxLayout()

        # creation constraint Axes Group 
        self.connection_axes_group = QGroupBox("Constraint Axes ")
        self.connection_options_layout = QGridLayout()
        translate_label = QLabel("Translate ")
        self.translate_all_checkbox_connection = QCheckBox("All")
        self.translate_x_checkbox_connection = QCheckBox("X")
        self.translate_y_checkbox_connection = QCheckBox("Y")
        self.translate_z_checkbox_connection = QCheckBox("Z")

        rotate_label = QLabel("Rotate ")
        self.rotate_all_checkbox_connection = QCheckBox("All")
        self.rotate_x_checkbox_connection = QCheckBox("X")
        self.rotate_y_checkbox_connection = QCheckBox("Y")
        self.rotate_z_checkbox_connection = QCheckBox("Z")

        scale_label = QLabel("Scale ")
        self.scale_all_checkbox_connection = QCheckBox("All")
        self.scale_x_checkbox_connection = QCheckBox("X")
        self.scale_y_checkbox_connection = QCheckBox("Y")
        self.scale_z_checkbox_connection = QCheckBox("Z")

        self.connection_options_layout.addWidget(translate_label, 0, 0, alignment=Qt.AlignRight)
        self.connection_options_layout.addWidget(self.translate_all_checkbox_connection, 0, 1)
        self.connection_options_layout.addWidget(self.translate_x_checkbox_connection, 0, 2)
        self.connection_options_layout.addWidget(self.translate_y_checkbox_connection, 0, 3)
        self.connection_options_layout.addWidget(self.translate_z_checkbox_connection, 0, 4)

        self.connection_options_layout.addWidget(rotate_label, 1, 0, alignment=Qt.AlignRight)
        self.connection_options_layout.addWidget(self.rotate_all_checkbox_connection, 1, 1)
        self.connection_options_layout.addWidget(self.rotate_x_checkbox_connection, 1, 2)
        self.connection_options_layout.addWidget(self.rotate_y_checkbox_connection, 1, 3)
        self.connection_options_layout.addWidget(self.rotate_z_checkbox_connection, 1, 4)

        self.connection_options_layout.addWidget(scale_label, 2, 0, alignment=Qt.AlignRight)
        self.connection_options_layout.addWidget(self.scale_all_checkbox_connection, 2, 1)
        self.connection_options_layout.addWidget(self.scale_x_checkbox_connection, 2, 2)
        self.connection_options_layout.addWidget(self.scale_y_checkbox_connection, 2, 3)
        self.connection_options_layout.addWidget(self.scale_z_checkbox_connection, 2, 4)

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

        self.influence_combo_box_1 = QComboBox()
        self.influence_combo_box_1.addItems(ITEMS)

        self.influence_combo_box_2 = QComboBox()
        self.influence_combo_box_2.addItems(ITEMS)

        self.influence_combo_box_3 = QComboBox()
        self.influence_combo_box_3.addItems(ITEMS)

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
    
    @Slot()
    def load_selected_objects(self, list_widget_object):
    # Get selected objects in Maya
        selected_objects = cmds.ls(selection=True) or []

        if not selected_objects:
            cmds.warning("No objects selected in Maya.")
            return

        # adding sleected objects 
        for obj in selected_objects:     
            list_widget_object.addItem(obj)
        print(f"Added Selected Objects in object ListBox ")
        self.status_bar.showMessage("Added Selected Objects in object ListBox")

    @Slot()
    def clear_list(self, list_widget_object):
        list_widget_object.clear()
        print(f"List Box Cleared")
        self.status_bar.showMessage("List Box Cleard ")

    @Slot()
    def move_selected_item_up(self, list_widget_object):
        row = list_widget_object.currentRow()
        if row <= 0:
            return
        # print(row)
        item = list_widget_object.takeItem(row)
        # print(item.text())
        list_widget_object.insertItem(row - 1, item)
        list_widget_object.setCurrentRow(row - 1)

    @Slot()
    def move_selected_item_down(self, list_widget_object):
        row = list_widget_object.currentRow()
        if row < 0 or row >= list_widget_object.count() - 1:
            return

        item = list_widget_object.takeItem(row)
        list_widget_object.insertItem(row + 1, item)
        list_widget_object.setCurrentRow(row + 1)

    @Slot()
    def update_translate_checkboxes(self, checked):
        if checked:
            self.translate_x_checkbox_constraint.setChecked(False)
            self.translate_y_checkbox_constraint.setChecked(False)
            self.translate_z_checkbox_constraint.setChecked(False)

        self.translate_x_checkbox_constraint.setEnabled(not checked)
        self.translate_y_checkbox_constraint.setEnabled(not checked)
        self.translate_z_checkbox_constraint.setEnabled(not checked)

    @Slot()
    def update_rotate_checkboxes(self, checked):
        if checked:
            self.rotate_x_checkbox_constraint.setChecked(not checked)
            self.rotate_y_checkbox_constraint.setChecked(not checked)
            self.rotate_z_checkbox_constraint.setChecked(not checked)

        self.rotate_x_checkbox_constraint.setEnabled(not checked)
        self.rotate_y_checkbox_constraint.setEnabled(not checked)
        self.rotate_z_checkbox_constraint.setEnabled(not checked)

    @Slot()
    def update_scale_checkboxes(self, checked):
        if checked:
            self.scale_x_checkbox_constraint.setChecked(not checked)
            self.scale_y_checkbox_constraint.setChecked(not checked)
            self.scale_z_checkbox_constraint.setChecked(not checked)

        self.scale_x_checkbox_constraint.setEnabled(not checked)
        self.scale_y_checkbox_constraint.setEnabled(not checked)
        self.scale_z_checkbox_constraint.setEnabled(not checked)

    @Slot()
    def create_constraints(self):
        source_objects = self.get_items_from_list(self.source_obj_list)
        target_objects = self.get_items_from_list(self.target_obj_list)
        print(source_objects)
        print(target_objects)
        if not source_objects or not target_objects:
            print("Source And Target object list needs to be populated.")
            self.status_bar.showMessage("Error: Source and Target object needs to be populated.")
            return
        
        constraint_type = self.constraint_type_combobox.currentIndex()
        print(constraint_type)
        offset_type = self.offset_radio_on.isChecked()
        print(offset_type)

        translate_chkbox_ischecked = []
        rotate_chkbox_ischecked = []
        scale_chkBox_ischecked = []

        if self.translate_all_checkbox_constraint.isChecked():
            translate_chkbox_ischecked.append("x")
            translate_chkbox_ischecked.append("y")
            translate_chkbox_ischecked.append("z")

        if self.translate_x_checkbox_constraint.isChecked():
            translate_chkbox_ischecked.append("x")
        if self.translate_y_checkbox_constraint.isChecked():
            translate_chkbox_ischecked.append("y")
        if self.translate_z_checkbox_constraint.isChecked():
            translate_chkbox_ischecked.append("z")


        if self.rotate_all_checkbox_constraint.isChecked():
            rotate_chkbox_ischecked.append("x")
            rotate_chkbox_ischecked.append("y")
            rotate_chkbox_ischecked.append("z")

        if self.rotate_x_checkbox_constraint.isChecked():
            rotate_chkbox_ischecked.append("x")
        if self.rotate_y_checkbox_constraint.isChecked():
            rotate_chkbox_ischecked.append("y")
        if self.rotate_z_checkbox_constraint.isChecked():
            rotate_chkbox_ischecked.append("z")

        if self.scale_all_checkbox_constraint.isChecked():
            scale_chkBox_ischecked.append("x")
            scale_chkBox_ischecked.append("y")
            scale_chkBox_ischecked.append("z")

        if self.scale_x_checkbox_constraint.isChecked():
            scale_chkBox_ischecked.append("x")
        if self.scale_z_checkbox_constraint.isChecked():
            scale_chkBox_ischecked.append("y")
        if self.scale_z_checkbox_constraint.isChecked():
            scale_chkBox_ischecked.append("z")
            
        print(f" translate {translate_chkbox_ischecked}")
        print(f" rotate {rotate_chkbox_ischecked}")
        print(f" rotate {scale_chkBox_ischecked}")

    def get_items_from_list(self, list_widget_object):
        items = []
        for i in range(list_widget_object.count()):
            items.append(list_widget_object.item(i).text())
        return items

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

# show_window()

