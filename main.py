from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout, 
                               QLabel, QListWidget, QHBoxLayout, QVBoxLayout, 
                               QRadioButton, QTabWidget, QComboBox, QStatusBar, QGroupBox,
                               QCheckBox, QFormLayout, QStyle, QLineEdit, QFrame)

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
        # self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #007FFF;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5980;
            }        
            QPushButton:disabled {
                background-color: #cbd5e1;
                color: white;
            }
            QLineEdit {
                color: white;
                border: 1px solid #00a8ff;
                padding: 6px;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid purple;
            }
                           
            QLineEdit:disabled {
                background-color: grey;
            }   
                           
            QTextEdit {
                color: black;
                font-size: 15px;
                border: 1px solid #485460;
                padding: 6px;
                border-radius: 10px;
            }
            QTextEdit:focus {
                border: 2px solid purple;
            }
                           
            QTabWidget::pane {
                border: 1px solid #555;
                border-radius: 8px;
                background: #323232;
            }
                           
            QTabBar::tab {
                background: #3a3a3a;
                padding: 8px 18px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
                           
            QTabBar::tab:selected {
                background: #3C7BEA;
                color: white;
            }

            QTabBar::tab:hover {
                background: #2980b9;
            }
        """)

    def set_status_message(self, message):
        
        self.status_bar.showMessage(message, timeout=3000)
        
        # self.status_bar.setStyleSheet("""
        #     QStatusBar{
        #         background: #007FFF;
        #         border: 1px solid grey;
        #         color: black;
        #         font-size: 10px;
        #         font-style: italic;
        #         border-radius: 2px;
        #     }
        # """)
        # if "ERROR" not in message:
        #     self.status_bar.setStyleSheet("""
        #         QStatusBar{
        #             background: #007FFF;
        #             border: 1px solid grey;
        #             color: black;
        #             font-size: 10px;
        #             font-style: italic;
        #             border-radius: 2px;
        #         }
        #     """)
        # else:
        #     self.status_bar.setStyleSheet("""
        #         QStatusBar{
        #             background: red;
        #             border: 1px solid grey;
        #             color: black;
        #             font-size: 10px;
        #             font-style: italic;
        #             border-radius: 2px;
        #         }
        #     """)

        print(message)
        
    def primary_button(self, text):

        new_push_button = QPushButton(text)
        new_push_button.setFixedSize(300, 40)
        # new_push_button.setStyleSheet("""
        #     QPushButton{
        #         background:#2E8BFF;
        #         color:white;
        #         border-radius:8px;
        #         font-weight:bold;
        #         font-size:11pt;
        #     }

        #     QPushButton:hover{
        #         background:#5CA7FF;
        #     }

        #     QPushButton:pressed{
        #         background:#1C6FD9;
        #     }
        # """)

        return new_push_button

    def main_ui(self):

        # Add Labels to the Grid Layout 
        self.objects_grid_layout = QGridLayout()

        source_obj_label = QLabel("Source Objects")
        target_obj_label = QLabel("Target Objects")
        source_obj_label.setStyleSheet("""
            QLabel
                {
                font: 15px;
                color: white;
            }""")
        
        target_obj_label.setStyleSheet("""
            QLabel
                {
                font: 15px;
                color: white;
            }""")

        self.source_obj_list = QListWidget()
        self.source_obj_list.setMinimumHeight(200)
        self.target_obj_list = QListWidget()
        self.target_obj_list.setMinimumHeight(200)

        # set Tool Tips 
        self.source_obj_list.setToolTip("All the Source Objects")
        self.target_obj_list.setToolTip("All the Target Objects")

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

        # Set Tool Tip 
        self.load_select_obj_source_button.setToolTip("Load Selected objects to Source")
        self.clear_list_source_button.setToolTip("Clear objects List Widget")

        source_buttons_layout = QHBoxLayout()
        source_buttons_layout.addWidget(self.load_select_obj_source_button)
        source_buttons_layout.addWidget(self.clear_list_source_button)

        source_list_row_layout = QHBoxLayout()
        
        source_button_column_layout = QVBoxLayout()
        source_button_column_layout.setSpacing(4)
        source_button_column_layout.setAlignment(Qt.AlignCenter)
        source_button_column_layout.addWidget(self.source_move_up_btn)
        source_button_column_layout.addWidget(self.source_move_down_btn)
        source_list_row_layout.addLayout(source_button_column_layout)
        source_list_row_layout.addWidget(self.source_obj_list)
        
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

        # Set Tool Tip 
        self.load_target_obj_button.setToolTip("Load Selected objects to Target")
        self.clear_list_target_button.setToolTip("Clear objects List Widget")

        # connections Target list buttons 
        self.load_target_obj_button.clicked.connect(lambda: self.load_selected_objects(self.target_obj_list))
        self.clear_list_target_button.clicked.connect(lambda: self.clear_list(self.target_obj_list))
        self.target_move_up_btn.clicked.connect(lambda: self.move_selected_item_up(self.target_obj_list))
        self.target_move_down_btn.clicked.connect(lambda: self.move_selected_item_down(self.target_obj_list))

        target_buttons_layout = QHBoxLayout()
        target_buttons_layout.addWidget(self.load_target_obj_button)
        target_buttons_layout.addWidget(self.clear_list_target_button)

        target_list_row_layout = QHBoxLayout()

        target_button_column_layout = QVBoxLayout()
        target_button_column_layout.setSpacing(4)
        target_button_column_layout.setAlignment(Qt.AlignCenter)
        target_button_column_layout.addWidget(self.target_move_up_btn)
        target_button_column_layout.addWidget(self.target_move_down_btn)
        target_list_row_layout.addLayout(target_button_column_layout)
        target_list_row_layout.addWidget(self.target_obj_list)


        target_column_layout = QVBoxLayout()
        target_column_layout.addWidget(target_obj_label, alignment=Qt.AlignCenter)
        target_column_layout.addLayout(target_list_row_layout)
        target_column_layout.addLayout(target_buttons_layout)

        # Adding Both Source and target layout in Grid Layout  
        self.objects_grid_layout.addLayout(source_column_layout, 0, 0)
        source_divider = self.create_divider_for_ui(QFrame.VLine)
        self.objects_grid_layout.addWidget(source_divider, 0, 1)

        self.objects_grid_layout.addLayout(target_column_layout, 0, 2)

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

        # Suffix text box
        self.suffix_lineedit = QLineEdit()
        self.suffix_lineedit.setPlaceholderText("Target suffix (e.g. _bind)")
        self.suffix_lineedit.setFixedWidth(250)
        self.suffix_lineedit.setEnabled(False)

        self.match_group.addWidget(relationship_label)
        self.match_group.addWidget(self.radio_button_order)
        self.match_group.addWidget(self.radio_button_name)
        self.match_group.addWidget(self.suffix_lineedit)

        # connections matchby name 
        self.radio_button_name.toggled.connect(self.radio_buttondisable)

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

        # setToolTIp
        self.first_tab.setToolTip("Constraint Tab")
        self.second_tab.setToolTip("Connection Tab")
        self.third_tab.setToolTip("CopySkin Tab")

        # self.constraint_tab_ui()
        # Status bar  
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.set_status_message("Ready")

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
        self.constraint_type_combobox.setToolTip("Select The Type of constraint")

        constraint_type_layout.addWidget(constraint_type_label, alignment=Qt.AlignRight)
        constraint_type_layout.addWidget(self.constraint_type_combobox, alignment=Qt.AlignLeft)

        # maintain offset Options Creation 
        maintain_offset_layout = QHBoxLayout()
        maintain_offset = QLabel("Maintain Offset:")
        self.offset_radio_on = QRadioButton("On")
        self.offset_radio_off = QRadioButton("Off")
        self.offset_radio_off.setChecked(True)
        self.offset_radio_on.setToolTip("Maintain Offset off and on ")
    
        maintain_offset_layout.addWidget(maintain_offset, alignment=Qt.AlignRight)
        maintain_offset_layout.addWidget(self.offset_radio_on, alignment=Qt.AlignLeft)
        maintain_offset_layout.addWidget(self.offset_radio_off, alignment=Qt.AlignLeft)
        maintain_offset_layout.setSpacing(12)

        # constraint adding everything to main Tab widget 

        constraint_main_layout.addLayout(constraint_type_layout) 
        constraint_main_layout.addLayout(maintain_offset_layout)
        divider_offsets = self.create_divider_for_ui(QFrame.HLine)
        constraint_main_layout.addWidget(divider_offsets)

        self.first_tab.setLayout(constraint_main_layout)  

        # creation constraint Axes Group 
        constraint_axes_group = QGroupBox("Constraint Axes ")

        constraint_axes_group.setStyleSheet("""
            QLabel
                {
                font: 15px;
                color: white;
            }""")
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
        divider_offsets = self.create_divider_for_ui(QFrame.HLine)
        constraint_main_layout.addWidget(divider_offsets)

        # Constraint Button creation 
        self.constraint_button_layout = QHBoxLayout()
        self.create_constraint_btn = self.primary_button("Create Constraint")
        self.constraint_button_layout.addWidget(self.create_constraint_btn)
        constraint_main_layout.addLayout(self.constraint_button_layout)

        # Set Tool Tip 
        self.create_constraint_btn.setToolTip("Create Constraints button")

        self.translate_all_checkbox_constraint.setChecked(True)
        self.rotate_all_checkbox_constraint.setChecked(True)
        self.scale_all_checkbox_constraint.setChecked(True)
        # added all enable disbale 
        if self.translate_all_checkbox_constraint.isChecked():
            self.translate_x_checkbox_constraint.setEnabled(False)
            self.translate_y_checkbox_constraint.setEnabled(False)
            self.translate_z_checkbox_constraint.setEnabled(False)

        if self.rotate_all_checkbox_constraint.isChecked():
            self.rotate_x_checkbox_constraint.setEnabled(False)
            self.rotate_y_checkbox_constraint.setEnabled(False)
            self.rotate_z_checkbox_constraint.setEnabled(False)

        if self.scale_all_checkbox_constraint.isChecked():
            self.scale_x_checkbox_constraint.setEnabled(False)
            self.scale_y_checkbox_constraint.setEnabled(False)
            self.scale_z_checkbox_constraint.setEnabled(False)

        # addLAyouts in main_layout
        self.main_layout.addLayout(self.objects_grid_layout)    
        divider_main = self.create_divider_for_ui(QFrame.HLine)
        self.main_layout.addWidget(divider_main)
        self.main_layout.addLayout(self.match_group)  
        self.main_layout.addWidget(self.main_tab_widget)
        
        self.central_widget.setLayout(self.main_layout)

        # signals for constraints 
        self.create_constraint_btn.clicked.connect(self.create_constraints)
        self.translate_all_checkbox_constraint.toggled.connect(self.enable_disable_translate_constraints)
        self.rotate_all_checkbox_constraint.toggled.connect(self.enable_disable_rotate_constraints)
        self.scale_all_checkbox_constraint.toggled.connect(self.enable_disable_scale_constraints)
   
    def connection_tab_ui(self):
        # create The connection tab
        connection_tab_layout = QVBoxLayout()
        # creation connection Axes Group 
        self.connection_axes_group = QGroupBox("Connection Axes ")
        self.connection_axes_group.setCheckable(True)
        self.connection_axes_group.setChecked(True)
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
        self.driver_driven_group = QGroupBox("Driver / Driven Attributes")
        self.driver_driven_group.setCheckable(True)
        self.driver_driven_group.setChecked(False)
        self.driver_driven_layout = QGridLayout()
        self.all_driver_label = QLabel("Driver Attribute")
        self.driver_combobox = QComboBox()
        self.all_drivers_listwidget = QListWidget()
        self.all_driven_label = QLabel("Driven Attribute")
        self.driven_combobox = QComboBox()
        self.all_driven_listwidget = QListWidget()
        
        self.driver_combobox.addItem("Default")
        self.driver_combobox.addItem("Custom")
        self.driver_combobox.addItem("Translate")
        self.driver_combobox.addItem("All")

        self.driven_combobox.addItem("Default")
        self.driven_combobox.addItem("Custom")
        self.driven_combobox.addItem("Translate")
        self.driven_combobox.addItem("All")

        # self.add_attributes_button = QPushButton()
        # self.add_attributes_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        # self.add_attributes_button.setFixedSize(40, 30)
        # self.remove_item_button = QPushButton("Remove Item")
        # self.clear_attributes_button = QPushButton("Clear")

        self.driver_driven_layout.addWidget(self.all_driver_label, 0, 0)
        self.driver_driven_layout.addWidget(self.all_driven_label, 0, 2)
        self.driver_driven_layout.addWidget(self.driver_combobox, 1, 0)
        self.driver_driven_layout.addWidget(self.driven_combobox, 1, 2)
        divider_connection = self.create_divider_for_ui(QFrame.VLine)
        self.driver_driven_layout.addWidget(divider_connection, 0, 1, 3, 1)
        self.driver_driven_layout.addWidget(self.all_drivers_listwidget, 2, 0)
        self.driver_driven_layout.addWidget(self.all_driven_listwidget, 2, 2)
        

        self.translate_all_checkbox_connection.setChecked(True)
        self.rotate_all_checkbox_connection.setChecked(True)
        self.scale_all_checkbox_connection.setChecked(True)
        # added all enable disbale 
        if self.translate_all_checkbox_connection.isChecked():
            self.translate_x_checkbox_connection.setEnabled(False)
            self.translate_y_checkbox_connection.setEnabled(False)
            self.translate_z_checkbox_connection.setEnabled(False)

        if self.rotate_all_checkbox_connection.isChecked():
            self.rotate_x_checkbox_connection.setEnabled(False)
            self.rotate_y_checkbox_connection.setEnabled(False)
            self.rotate_z_checkbox_connection.setEnabled(False)

        if self.scale_all_checkbox_connection.isChecked():
            self.scale_x_checkbox_connection.setEnabled(False)
            self.scale_y_checkbox_connection.setEnabled(False)
            self.scale_z_checkbox_connection.setEnabled(False)

        # Create connection buttons 
        self.connection_button_layout = QHBoxLayout()
        self.create_connection_button = self.primary_button("Create Connections")

        connection_tab_layout.addWidget(self.connection_axes_group)

        divider_connection = self.create_divider_for_ui(QFrame.HLine)
        connection_tab_layout.addWidget(divider_connection)
        self.driver_driven_group.setLayout(self.driver_driven_layout)
        connection_tab_layout.addWidget(self.driver_driven_group)
        
        divider_connection = self.create_divider_for_ui(QFrame.HLine)
        connection_tab_layout.addWidget(divider_connection)
        self.connection_button_layout.addWidget(self.create_connection_button)
        connection_tab_layout.addLayout(self.connection_button_layout)
        
        self.connection_axes_group.setLayout(self.connection_options_layout)
        self.second_tab.setLayout(connection_tab_layout)

        # set ToolTips 
        self.create_connection_button.setToolTip("Create Connections on selected objects")

        # create signals 
        self.translate_all_checkbox_connection.toggled.connect(self.enable_disable_translate_connection)
        self.rotate_all_checkbox_connection.toggled.connect(self.enable_disable_rotate_connection)
        self.scale_all_checkbox_connection.toggled.connect(self.enable_disable_scale_connection)
        self.create_connection_button.clicked.connect(self.create_connections)

        # signals For Populating cutom attributes 
        # self.source_obj_list.itemSelectionChanged.connect(
        #     lambda: self.populate_custom_attributes(self.source_obj_list, self.all_drivers_listwidget)
        # )
        # self.target_obj_list.itemSelectionChanged.connect(
        #     lambda: self.populate_custom_attributes(self.target_obj_list, self.all_driven_listwidget)
        # )

        self.source_obj_list.itemSelectionChanged.connect(
            lambda: self.update_list(
                self.source_obj_list,
                self.all_drivers_listwidget,
                self.driver_combobox.currentText(),
            )
        )
        self.driver_combobox.currentTextChanged.connect(
            lambda: self.update_list(
                self.source_obj_list,
                self.all_drivers_listwidget,
                self.driver_combobox.currentText(),
            )
        )

        self.target_obj_list.itemSelectionChanged.connect(
            lambda: self.update_list(
                self.target_obj_list,
                self.all_driven_listwidget,
                self.driven_combobox.currentText(),
            )
        )
        self.driven_combobox.currentTextChanged.connect(
            lambda: self.update_list(
                self.target_obj_list,
                self.all_driven_listwidget,
                self.driven_combobox.currentText(),
            )
        )

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

        self.copyskin_form_layout.addRow(self.influence_label_1, self.influence_combo_box_1)
        self.copyskin_form_layout.addRow(self.influence_label_2, self.influence_combo_box_2)
        self.copyskin_form_layout.addRow(self.influence_label_3, self.influence_combo_box_3)

        # Set Defaults 
        self.closest_point_radio_btn.setChecked(True)
        self.influence_combo_box_1.setCurrentIndex(2)
        self.influence_combo_box_2.setCurrentIndex(5)
        self.influence_combo_box_3.setCurrentIndex(5)

        # self.copy_skin_btn = QPushButton("Copy Skin")

        self.copyskin_button_layout = QHBoxLayout()
        self.copy_skin_btn = self.primary_button("Copy Skin")
        self.copyskin_button_layout.addWidget(self.copy_skin_btn)

        # set ToolTips 
        self.create_connection_button.setToolTip("Copied skin To target Objects.")

        copy_skin_group.setLayout(self.copyskin_form_layout)
        copyskin_tab_layout.addWidget(copy_skin_group)
        divider_copyskin = self.create_divider_for_ui(QFrame.HLine)
        copyskin_tab_layout.addWidget(divider_copyskin)
        copyskin_tab_layout.addLayout(self.copyskin_button_layout)
        self.third_tab.setLayout(copyskin_tab_layout)

        # signals for copy Skin button 
        self.copy_skin_btn.clicked.connect(self.copy_skins)
    
    def create_divider_for_ui(self, linetype):
        divider = QFrame()
        divider.setFrameShape(linetype)
        divider.setFrameShadow(QFrame.Sunken)
        return divider

    def get_translations(self, loaded_selected_item):
        # Return all translated names
        # print(list_widget.text())
        current_object = loaded_selected_item.text()
        custom_attributes = cmds.listAttr(current_object, keyable=True, unlocked=True)
        # print(custom_attributes)

        transform_attrs = {
            "translateX", "translateY", "translateZ",
            "rotateX", "rotateY", "rotateZ",
            "scaleX", "scaleY", "scaleZ",
            "visibility"
        }
        attributes = []
        for attr in custom_attributes:
            if attr in transform_attrs:
                # print(attr)
                attributes.append(attr)

        return attributes

    def get_custom_items(self, loaded_selected_item):
        # Return user-defined items which is manually created 
        current_object = loaded_selected_item.text()
        custom_attributes = cmds.listAttr(current_object, userDefined=True) or []
        return custom_attributes
    
    def get_all_items(self, loaded_selected_item):
        # Return all items
        current_object = loaded_selected_item.text()
        custom_attributes = cmds.listAttr(current_object, keyable=True)
        return custom_attributes

    @Slot()
    def populate_custom_attributes(self, list_widget, target_list_widget):
        target_list_widget.clear()

        current_object_selected = list_widget.currentItem()
        if not current_object_selected:
            return

        current_object_name = current_object_selected.text()
        print(current_object_name)

        # driven_combobox_value = self.driver_combobox.currentText()
        # print(driven_combobox_value)
        custom_attributes = cmds.listAttr(current_object_name, userDefined=True) or []
        for attribute in custom_attributes:
            target_list_widget.addItem(attribute)
            
    @Slot()
    def update_list(self, list_widget, target_list_widget, driver_driven_combobox_value):
        current_object_selected = list_widget.currentItem()
        if not current_object_selected:
            return
        
        target_list_widget.clear()

        if driver_driven_combobox_value == "Translate":
            items = self.get_translations(current_object_selected)
        elif driver_driven_combobox_value == "Custom":
            items = self.get_custom_items(current_object_selected)
        elif driver_driven_combobox_value == "All":
            items = self.get_all_items(current_object_selected)
        else:
            items = []
        target_list_widget.addItems(items)

    @Slot()
    def load_selected_objects(self, list_widget_object):
    # Get selected objects in Maya
        selected_objects = cmds.ls(selection=True) or []
        if not selected_objects:
            cmds.warning("No objects selected in Maya.")
            self.set_status_message("ERROR: No objects selected in Maya.")
            return

        # adding sleected objects 
        for obj in selected_objects:     
            list_widget_object.addItem(obj)
        print(f"Added Selected Objects in object ListBox ")
        self.set_status_message("Added selected objects to the list.")

    @Slot()
    def radio_buttondisable(self, checked):
        if checked:
            self.target_obj_list.setEnabled(not checked)
            self.load_target_obj_button.setEnabled(not checked)
            self.clear_list_target_button.setEnabled(not checked)
            self.target_move_up_btn.setEnabled(not checked)
            self.target_move_down_btn.setEnabled(not checked)
            self.suffix_lineedit.setEnabled(checked)
            self.all_driven_listwidget.clear()
            self.set_status_message("Driven attribute list cleared.")
        else:
            self.target_obj_list.setEnabled(not checked)
            self.load_target_obj_button.setEnabled(not checked)
            self.clear_list_target_button.setEnabled(not checked)
            self.target_move_up_btn.setEnabled(not checked)
            self.target_move_down_btn.setEnabled(not checked)
            self.suffix_lineedit.setEnabled(checked)

    @Slot()
    def clear_list(self, list_widget_object):
        list_widget_object.clear()
        print(f"List Box Cleared")
        self.set_status_message("List box cleared.")

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
        self.set_status_message("Selected Object Moved Up.")

    @Slot()
    def move_selected_item_down(self, list_widget_object):
        row = list_widget_object.currentRow()
        if row < 0 or row >= list_widget_object.count() - 1:
            return

        item = list_widget_object.takeItem(row)
        list_widget_object.insertItem(row + 1, item)
        list_widget_object.setCurrentRow(row + 1)
        self.set_status_message("Selected Object Moved Down.")

    @Slot()
    def enable_disable_translate_constraints(self, checked):
        if checked:
            self.translate_x_checkbox_constraint.setChecked(False)
            self.translate_y_checkbox_constraint.setChecked(False)
            self.translate_z_checkbox_constraint.setChecked(False)

        self.translate_x_checkbox_constraint.setEnabled(not checked)
        self.translate_y_checkbox_constraint.setEnabled(not checked)
        self.translate_z_checkbox_constraint.setEnabled(not checked)

    @Slot()
    def enable_disable_rotate_constraints(self, checked):
        if checked:
            self.rotate_x_checkbox_constraint.setChecked(not checked)
            self.rotate_y_checkbox_constraint.setChecked(not checked)
            self.rotate_z_checkbox_constraint.setChecked(not checked)

        self.rotate_x_checkbox_constraint.setEnabled(not checked)
        self.rotate_y_checkbox_constraint.setEnabled(not checked)
        self.rotate_z_checkbox_constraint.setEnabled(not checked)

    @Slot()
    def enable_disable_scale_constraints(self, checked):
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
        # print(source_objects)
        # print(target_objects)

        constraint_type = self.constraint_type_combobox.currentIndex()
        # print(constraint_type)
        offset_type = self.offset_radio_on.isChecked()
        # print(offset_type)

        skip_translate = []
        skip_rotate = []
        skip_scale = []

        if not self.translate_all_checkbox_constraint.isChecked():
            if not self.translate_x_checkbox_constraint.isChecked():
                skip_translate.append("x")
            if not self.translate_y_checkbox_constraint.isChecked():
                skip_translate.append("y")
            if not self.translate_z_checkbox_constraint.isChecked():
                skip_translate.append("z")

        if not self.rotate_all_checkbox_constraint.isChecked():
            if not self.rotate_x_checkbox_constraint.isChecked():
                skip_rotate.append("x")
            if not self.rotate_y_checkbox_constraint.isChecked():
                skip_rotate.append("y")
            if not self.rotate_z_checkbox_constraint.isChecked():
                skip_rotate.append("z")

        if not self.scale_all_checkbox_constraint.isChecked():
            if not self.scale_x_checkbox_constraint.isChecked():
                skip_scale.append("x")
            if not self.scale_y_checkbox_constraint.isChecked():
                skip_scale.append("y")
            if not self.scale_z_checkbox_constraint.isChecked():
                skip_scale.append("z")
                
        # print(f" translate {skip_translate}")
        # print(f" rotate {skip_rotate}")
        # print(f" rotate {skip_scale}")

        # match by order 
        if self.radio_button_order.isChecked():

            if not source_objects or not target_objects:
                print("Source and Target object lists need to be populated.")
                self.set_status_message("ERROR: Source and Target object lists need to be populated.")

                if self.radio_button_order.isChecked() and len(source_objects) != len(target_objects):
                    cmds.warning("Source and Target lists must contain the same number of objects.")
                    self.set_status_message("ERROR: Source and Target lists must contain the same number of objects.")
                    return

            for i in range(len(source_objects)):
                if constraint_type == 0:
                    cmds.parentConstraint(source_objects[i], target_objects[i], mo=offset_type, skipTranslate=skip_translate, skipRotate=skip_rotate)
                elif constraint_type == 1:
                    cmds.pointConstraint(source_objects[i], target_objects[i], mo=offset_type, skip=skip_translate)
                if constraint_type == 2:
                    cmds.orientConstraint(source_objects[i], target_objects[i], mo=offset_type, skip=skip_rotate)
                if constraint_type == 3:
                    cmds.scaleConstraint(source_objects[i], target_objects[i], mo=offset_type, skip=skip_scale) 

        # match by name 
        else:
            # Only the source list is Checked if it is filled
            if not source_objects:
                cmds.warning("Source object list needs to be populated.")
                self.set_status_message("ERROR: Source object list needs to be populated.")
                return
            
            suffix = self.suffix_lineedit.text().strip()
            # print(suffix)
            for obj in source_objects:
                target_suffix = obj.rsplit("_", 1)[0]
                target_name = f"{target_suffix}{suffix}"

                if not cmds.objExists(target_name):
                    cmds.warning("{} does not exist.".format(target_name))
                    continue
                # target_dict.append(target_name)
                # print(target_suffix)
                if constraint_type == 0:
                    cmds.parentConstraint(obj, target_name, mo=offset_type, skipTranslate=skip_translate, skipRotate=skip_rotate)
                elif constraint_type == 1:
                    cmds.pointConstraint(obj, target_name, mo=offset_type, skip=skip_translate)
                if constraint_type == 2:
                    cmds.orientConstraint(obj, target_name, mo=offset_type, skip=skip_rotate)
                if constraint_type == 3:
                    cmds.scaleConstraint(obj, target_name, mo=offset_type, skip=skip_scale)  


        self.set_status_message("Constraints completed")
            # print(target_dict)
            
    def connect_attrs(self, source_obj, target_obj, connection_attrs):
        if not cmds.objExists(source_obj):
            cmds.warning("Source object {} does not exist.".format(source_obj))
            return
        if not cmds.objExists(target_obj):
            cmds.warning("Target object {} does not exist.".format(target_obj))
            return

        connected = False
        for attr in connection_attrs:
            attr = attr.strip()
            if not attr:
                continue

            source_attr = "{}.{}".format(source_obj, attr)
            target_attr = "{}.{}".format(target_obj, attr)
            if not cmds.objExists(source_attr):
                cmds.warning("Attribute {} does not exist on {}.".format(attr, source_obj))
                continue
            if not cmds.objExists(target_attr):
                cmds.warning("Attribute {} does not exist on {}.".format(attr, target_obj))
                continue
            cmds.connectAttr(source_attr, target_attr, force=True)
            connected = True

        if connected:
            print("Connected {} -> {}".format(source_obj, target_obj))

    def connect_selected_custom_attribute(self, source_obj, target_obj, driver_attr, driven_attr):
        if not cmds.objExists(source_obj):
            cmds.warning("Source object {} does not exist.".format(source_obj))
            return
        if not cmds.objExists(target_obj):
            cmds.warning("Target object {} does not exist.".format(target_obj))
            return

        source_attr = "{}.{}".format(source_obj, driver_attr)
        target_attr = "{}.{}".format(target_obj, driven_attr)
        if not cmds.objExists(source_attr):
            cmds.warning("Attribute {} does not exist on {}.".format(driver_attr, source_obj))
            return
        if not cmds.objExists(target_attr):
            cmds.warning("Attribute {} does not exist on {}.".format(driven_attr, target_obj))
            return

        cmds.connectAttr(source_attr, target_attr, force=True)
        print("Connected {} -> {}".format(source_attr, target_attr))

    def get_selected_custom_attributes(self):
        source_item = self.source_obj_list.currentItem()
        target_item = self.target_obj_list.currentItem()
        driver_item = self.all_drivers_listwidget.currentItem()
        driven_item = self.all_driven_listwidget.currentItem()

        if not source_item or not target_item or not driver_item or not driven_item:
            return []

        source_obj = source_item.text().strip()
        target_obj = target_item.text().strip()
        driver_attr = driver_item.text().strip()
        driven_attr = driven_item.text().strip()

        if not source_obj or not target_obj or not driver_attr or not driven_attr:
            return []

        selected_pairs = []
        selected_pairs.append((source_obj, target_obj, driver_attr, driven_attr))
        return selected_pairs

    @Slot()
    def create_connections(self):
        source_objects = self.get_items_from_list(self.source_obj_list)
        target_objects = self.get_items_from_list(self.target_obj_list)

        if self.connection_axes_group.isChecked():
            translate_attrs = []
            rotate_attrs = []
            scale_attrs = []
            if self.translate_all_checkbox_connection.isChecked():
                translate_attrs = ["translateX", "translateY", "translateZ"]
            else:
                if self.translate_x_checkbox_connection.isChecked():
                    translate_attrs.append("translateX")
                if self.translate_y_checkbox_connection.isChecked():
                    translate_attrs.append("translateY")
                if self.translate_z_checkbox_connection.isChecked():
                    translate_attrs.append("translateZ")

            if self.rotate_all_checkbox_connection.isChecked():
                rotate_attrs = ["rotateX", "rotateY", "rotateZ"]
            else:
                if self.rotate_x_checkbox_connection.isChecked():
                    rotate_attrs.append("rotateX")
                if self.rotate_y_checkbox_connection.isChecked():
                    rotate_attrs.append("rotateY")
                if self.rotate_z_checkbox_connection.isChecked():
                    rotate_attrs.append("rotateZ")

            if self.scale_all_checkbox_connection.isChecked():
                scale_attrs = ["scaleX", "scaleY", "scaleZ"]
            else:
                if self.scale_x_checkbox_connection.isChecked():
                    scale_attrs.append("scaleX")
                if self.scale_y_checkbox_connection.isChecked():
                    scale_attrs.append("scaleY")
                if self.scale_z_checkbox_connection.isChecked():
                    scale_attrs.append("scaleZ")

            connection_attrs = translate_attrs + rotate_attrs + scale_attrs
            custom_attrs = []
        elif self.driver_driven_group.isChecked():
            selected_pairs = self.get_selected_custom_attributes()
            if not selected_pairs:
                self.set_status_message("ERROR: Select driver and driven attributes.")
                return

            for source_obj, target_obj, driver_attr, driven_attr in selected_pairs:
                self.connect_selected_custom_attribute(source_obj, target_obj, driver_attr, driven_attr)

            self.set_status_message("Connections done.")
            return
        else:
            self.set_status_message("ERROR: Select a connection section to run.")
            return

        if not connection_attrs and not custom_attrs:
            cmds.warning("No translate/rotate/scale channels or custom attributes selected to connect.")
            self.set_status_message("ERROR: No channels or custom attributes selected to connect.")
            return

        # match by order
        if self.radio_button_order.isChecked():
            if not source_objects or not target_objects:
                print("Source and Target object lists need to be populated.")
                self.set_status_message("ERROR: Source and Target object lists need to be populated.")
                return

            if len(source_objects) != len(target_objects):
                cmds.warning("Source and Target lists must contain the same number of objects.")
                self.set_status_message("ERROR: Source and Target lists must contain the same number of objects.")
                return

            for i, source_obj in enumerate(source_objects):
                target_obj = target_objects[i]
                if connection_attrs:
                    self.connect_attrs(source_obj, target_obj, connection_attrs)
                if custom_attrs:
                    self.connect_attrs(source_obj, target_obj, custom_attrs)

        # match by name
        else:
            if not source_objects:
                cmds.warning("Source object list needs to be populated.")
                self.set_status_message("ERROR: Source object list needs to be populated.")
                return

            suffix = self.suffix_lineedit.text().strip()
            for source_obj in source_objects:
                target_suffix = source_obj.rsplit("_", 1)[0]
                target_obj = f"{target_suffix}{suffix}"

                if not cmds.objExists(target_obj):
                    cmds.warning("{} does not exist.".format(target_obj))
                    continue

                if connection_attrs:
                    self.connect_attrs(source_obj, target_obj, connection_attrs)
                if custom_attrs:
                    self.connect_attrs(source_obj, target_obj, custom_attrs)

        self.set_status_message("Connections done.")

    def has_skin_cluster(self, source_objects):
        if not source_objects:
            return False

        if not cmds.objExists(source_objects):
            return False

        history_of_skin = cmds.listHistory(source_objects)
        skin_clusters = cmds.ls(history_of_skin, type="skinCluster")

        if skin_clusters:
            return True

        return False

    def copy_skin_wts_mesh(self, source_obj, target_obj, association_type, influenceAssociation_list):
        source_skin = cmds.ls(cmds.listHistory(source_obj), type="skinCluster")
        if not source_skin:
            cmds.warning("{} has no skinCluster.".format(source_obj))
            return False

        source_skin = source_skin[0]

        target_skin = cmds.ls(cmds.listHistory(target_obj), type="skinCluster")
        if not target_skin:
            influences_joint_source = cmds.skinCluster(source_skin, q=True, influence=True)
            target_skin = cmds.skinCluster(influences_joint_source, target_obj, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1,)
            if not target_skin:
                cmds.warning("Failed to create a skinCluster on {}.".format(target_obj))
                return False
            target_skin = target_skin[0]
        else:
            target_skin = target_skin[0]

        cmds.copySkinWeights(
            ss=source_skin,
            ds=target_skin,
            noMirror=True,
            surfaceAssociation=association_type,
            influenceAssociation=influenceAssociation_list,
        )
        print("Copied {} -> {}".format(source_obj, target_obj))
        self.set_status_message("Copied Skin weights done.")
        return True

    @Slot()
    def copy_skins(self):
        source_objects = self.get_items_from_list(self.source_obj_list)
        target_objects = self.get_items_from_list(self.target_obj_list)

        association_type = ""
        if self.closest_point_radio_btn.isChecked():
            association_type = "closestPoint"
        elif self.ray_cast_radio_btn.isChecked():
            association_type = "rayCast"
        elif self.closest_component_radio_btn.isChecked():
            association_type = "closestComponent"
        else:
            association_type = "closestPoint"

        association_map = {
            "Closest Joint": "closestJoint",
            "Closest Bone": "closestBone",
            "Name": "name",
            "Label": "label",
            "One To One": "oneToOne",
        }

        influenceAssociation_list = []
        for combo in (self.influence_combo_box_1, self.influence_combo_box_2, self.influence_combo_box_3):
            influence_text = combo.currentText()
            if influence_text == "None":
                continue
            influenceAssociation_list.append(association_map[influence_text])

        # match by order
        if self.radio_button_order.isChecked():
            if not source_objects and target_objects:
                print("Source and Target object lists need to be populated.")
                self.set_status_message("ERROR: Source and Target object lists need to be populated.")
                return

            if len(source_objects) != len(target_objects):
                cmds.warning("Source and Target lists must contain the same number of objects.")
                self.set_status_message("ERROR: Source and Target lists must contain the same number of objects.")
                return

            for i in range(len(source_objects)):
                source_obj = source_objects[i]
                target_obj = target_objects[i]
                if not self.has_skin_cluster(source_obj):
                    cmds.warning("{} has no skinCluster.".format(source_obj))
                    self.set_status_message("ERROR: {} has no skinCluster.".format(source_obj))
                    continue
                self.copy_skin_wts_mesh(source_obj, target_obj, association_type, influenceAssociation_list)
                print(i)

        # match by name
        else:
            if not source_objects:
                cmds.warning("Source object list needs to be populated.")
                self.set_status_message("ERROR: Source object list needs to be populated.")
                return

            suffix = self.suffix_lineedit.text().strip()
            for source_obj in source_objects:
                if not self.has_skin_cluster(source_obj):
                    cmds.warning("{} has no skinCluster.".format(source_obj))
                    self.set_status_message("ERROR: {} has no skinCluster.".format(source_obj))
                    continue

                target_suffix = source_obj.rsplit("_", 1)[0]
                target_obj = f"{target_suffix}{suffix}"

                if not cmds.objExists(target_obj):
                    cmds.warning("{} does not exist.".format(target_obj))
                    continue

                self.copy_skin_wts_mesh(source_obj, target_obj, association_type, influenceAssociation_list)

    @Slot()
    def enable_disable_translate_connection(self, checked):
        if checked:
            self.translate_x_checkbox_connection.setChecked(False)
            self.translate_y_checkbox_connection.setChecked(False)
            self.translate_z_checkbox_connection.setChecked(False)

        self.translate_x_checkbox_connection.setEnabled(not checked)
        self.translate_y_checkbox_connection.setEnabled(not checked)
        self.translate_z_checkbox_connection.setEnabled(not checked)

    @Slot()
    def enable_disable_rotate_connection(self, checked):
        if checked:
            self.rotate_x_checkbox_connection.setChecked(False)
            self.rotate_y_checkbox_connection.setChecked(False)
            self.rotate_z_checkbox_connection.setChecked(False)

        self.rotate_x_checkbox_connection.setEnabled(not checked)
        self.rotate_y_checkbox_connection.setEnabled(not checked)
        self.rotate_z_checkbox_connection.setEnabled(not checked)

    @Slot()
    def enable_disable_scale_connection(self, checked):
        if checked:
            self.scale_x_checkbox_connection.setChecked(False)
            self.scale_y_checkbox_connection.setChecked(False)
            self.scale_z_checkbox_connection.setChecked(False)

        self.scale_x_checkbox_connection.setEnabled(not checked)
        self.scale_y_checkbox_connection.setEnabled(not checked)
        self.scale_z_checkbox_connection.setEnabled(not checked)

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




