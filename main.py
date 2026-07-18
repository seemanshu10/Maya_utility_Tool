"""
Multi-Object Rigging Toolkit: batch-creates constraints, connects attributes, and copies skin weights between a "Source" object list and a "Target" object list.

Source/Target pairing has two mutually exclusive modes, chosen with radio button:
  - Order: positional pairing, source[i] -> target[i]
  - Name:  each source is paired with a target found by stripping the source's trailing and appending a suffix, searched within the source's
    own top-level group.

"""

from PySide2.QtWidgets import (QMainWindow, QPushButton, QWidget, QGridLayout,
                               QLabel, QListWidget, QHBoxLayout, QVBoxLayout,
                               QRadioButton, QTabWidget, QComboBox, QGroupBox,
                               QCheckBox, QFormLayout, QLineEdit, QFrame, QMessageBox)

from PySide2.QtCore import Qt, Slot

# maya Python API 
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import shiboken2

INFLUENCE_ASSOCIATION_ITEMS = ["None", "Closest Bone", "Closest Joint", "One To One", "Label", "Name" ]

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QWidget)


class RiggingUtilityTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Multi-Object Rigging Toolkit")
        self.setGeometry(100, 100, 600, 900)
        self.initUI()

    def initUI(self):
        # Create a basic central widget
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_ui()
        self.constraint_tab_ui()    # constraint tab creation
        self.connection_tab_ui()    # connection tab creation
        self.copyskin_tab_ui()      # copy skin Tab creation
        self.apply_theme()

    def apply_theme(self):
        # :: - Means which piece of widget 
        # :  - means which state so (checked, diabled , indicator) 
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #444444;
                color: #cccccc;
                font-size: 12px;
            }

            QToolTip {
                background-color: #2b2b2b;
                color: #cccccc;
                border: 1px solid #222222;
                padding: 4px;
            }

            /* ---------- Buttons ---------- */
            QPushButton {
                background-color: #5d5d5d;
                color: #e6e6e6;
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #6b6b6b;
                border: 1px solid #E8792A;
            }
            QPushButton:pressed {
                background-color: #E8792A;
                color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #4a4a4a;
                color: #7a7a7a;
                border: 1px solid #3a3a3a;
            }

            /* ---------- Text inputs ---------- */
            QLineEdit, QTextEdit {
                background-color: #232323;
                color: #cccccc;
                border: 1px solid #1e1e1e;
                border-radius: 3px;
                padding: 5px;
                selection-background-color: #E8792A;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #E8792A;
            }
            QLineEdit:disabled, QTextEdit:disabled {
                background-color: #3a3a3a;
                color: #7a7a7a;
            }

            /* ---------- Labels ---------- */
            QLabel {
                color: #cccccc;
                background: transparent;
            }
            QLabel:disabled {
                color: #7a7a7a;
            }

            /* ---------- GroupBox ---------- */
            QGroupBox {
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #3d3d3d;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 8px;
                padding: 0 4px;
                color: #f0b98a;
            }

            /* ---------- CheckBox / RadioButton ---------- */
            QCheckBox, QRadioButton {
                color: #cccccc;
                spacing: 6px;
                background: transparent;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 13px;
                height: 13px;
                background-color: #232323;
                border: 1px solid #1a1a1a;
            }
            QCheckBox::indicator {
                border-radius: 2px;
            }
            QRadioButton::indicator {
                border-radius: 7px;
            }
            QCheckBox::indicator:hover, QRadioButton::indicator:hover {
                border: 1px solid #E8792A;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background-color: #E8792A;
                border: 1px solid #E8792A;
            }
            QCheckBox:disabled, QRadioButton:disabled {
                color: #7a7a7a;
            }
            QCheckBox::indicator:disabled, QRadioButton::indicator:disabled {
                background-color: #3a3a3a;
                border: 1px solid #2e2e2e;
            }
            QCheckBox::indicator:checked:disabled, QRadioButton::indicator:checked:disabled {
                background-color: #7a7a7a;
                border: 1px solid #6a6a6a;
            }

            /* ---------- ComboBox ----------*/ 
            QComboBox {
                background-color: #5d5d5d;
                color: #e6e6e6;
                border: 1px #2a2a2a;
                border-radius: 1px;
                padding: 4px 8px;
                min-width: 120px;
            }
            QComboBox:hover {
                border: 1px solid #E8792A;
            }      
            QComboBox:disabled {
                background-color: #4a4a4a;
                color: #7a7a7a;
                border: 1px solid #3a3a3a;
            }
            QComboBox::drop-down {
                width: 18px;
            }     
            
            QComboBox QAbstractItemView {
                background-color: #383838;
                color: #cccccc;
                border: 1px solid #2a2a2a;
                selection-background-color: #E8792A;
                selection-color: #ffffff;
                outline: none;
            }
            
            /* ---------- ListWidget ---------- */
            QListWidget {
                background-color: #232323;
                color: #cccccc;
                border: 1px solid #1e1e1e;
                border-radius: 3px;
                alternate-background-color: #282828;
            }
            QListWidget::item {
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: #E8792A;
                color: #ffffff;
            }
            QListWidget::item:hover:!selected {
                background-color: #3a3a3a;
            }
            QListWidget:disabled {
                background-color: #3a3a3a;
                color: #7a7a7a;
            }
            QListWidget::item:disabled {
                color: #7a7a7a;
            }

            /* ---------- TabWidget ---------- */
            QTabWidget::pane {
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                background: #3d3d3d;
                top: -1px;
            }
            QTabBar::tab {
                background: #393939;
                color: #b0b0b0;
                padding: 7px 18px;
                border: 1px solid #2a2a2a;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #E8792A;
                color: #ffffff;
            }
            QTabBar::tab:hover:!selected {
                background: #4a4a4a;
            }

            /* ---------- Frame (dividers) ---------- */
            QFrame[frameShape="4"], QFrame[frameShape="5"] {
                color: #2a2a2a;
            }

            /* ---------- ScrollBar ---------- */
            QScrollBar:vertical {
                background: #393939;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #5d5d5d;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #E8792A;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: #393939;
                height: 12px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background: #5d5d5d;
                border-radius: 5px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #E8792A;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

    def dialog_box_window(self, message):
        print(message)
        # convention: prefix a message with "ERROR" to get a critical dialog instead of an info one
        if message.upper().startswith("ERROR"):
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Completed", message)

    def primary_button(self, text):
        # creating Qpush Buttons 
        new_push_button = QPushButton(text)
        return new_push_button

    def main_ui(self):
        # Add Labels to the Grid Layout 
        self.objects_grid_layout = QGridLayout()
        source_obj_label = QLabel("Source Objects")
        target_obj_label = QLabel("Target Objects")
        source_obj_label.setStyleSheet("""
            QLabel
                {
                font: 13px;
                color: white;
                font-weight: bold;
            }""")
        
        target_obj_label.setStyleSheet("""
            QLabel
                {
                font: 13px;
                color: white;
                font-weight: bold;
            }""")

        self.source_obj_list = QListWidget()
        self.source_obj_list.setMinimumHeight(200)
        self.target_obj_list = QListWidget()
        self.target_obj_list.setMinimumHeight(200)

        # full DAG paths for target and source object lists 
        self.source_object_paths = []
        self.target_object_paths = []

        # set Tool Tips
        self.source_obj_list.setToolTip("Objects that will drive the constraint / connection")
        self.target_obj_list.setToolTip("Objects that will receive the constraint / connection")
        # alt+24 - ↑ alt+25 - ↓
        self.source_move_up_btn = QPushButton("↑")
        self.source_move_up_btn.setFixedSize(25, 25)
        self.source_move_up_btn.setToolTip("Move selected source item up")
        self.source_move_down_btn = QPushButton("↓")
        self.source_move_down_btn.setFixedSize(25, 25)
        self.source_move_down_btn.setToolTip("Move selected source item down")

        self.target_move_up_btn = QPushButton("↑")
        self.target_move_up_btn.setFixedSize(25, 25)
        self.target_move_up_btn.setToolTip("Move selected target item up")
        self.target_move_down_btn = QPushButton("↓")
        self.target_move_down_btn.setFixedSize(25, 25)
        self.target_move_down_btn.setToolTip("Move selected target item down")

        # Source Objects Side
        self.load_select_obj_source_button = QPushButton("Load Selected Objects")
        self.clear_list_source_button = QPushButton("Clear")

        # Set Tool Tip
        self.load_select_obj_source_button.setToolTip("Load the current Maya selection into the Source list")
        self.clear_list_source_button.setToolTip("Remove all items from the Source list")

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
        self.load_target_obj_button.setToolTip("Load the current Maya selection into the Target list")
        self.clear_list_target_button.setToolTip("Remove all items from the Target list")

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

        self.match_group_offset = QGroupBox()
        self.match_group_offset.setToolTip("Match by Order: Will Use Relationship on one to one \nMatch by Name: Will Use source objects and suffix to find the target objects ")
        self.match_group = QHBoxLayout()

        # Reduce the space around the layout
        self.match_group.setContentsMargins(20, 0, 20, 5)

        # Reduce the space between widgets
        self.match_group.setSpacing(5)
        relationship_label = QLabel("Match by:")

        self.radio_button_order = QRadioButton("Order")
        self.radio_button_name = QRadioButton("Name")
        self.radio_button_order.setChecked(True)
        self.radio_button_order.setToolTip("Match source to target one-to-one by list order")
        self.radio_button_name.setToolTip("Match source to target by name, using the suffix below")

        # Suffix text box
        self.suffix_lineedit = QLineEdit()
        self.suffix_lineedit.setPlaceholderText("Target suffix (e.g. _bind)")
        self.suffix_lineedit.setToolTip("Suffix appended to each source name to find its matching target, \nSuffix find Object correctly only if the top grp is same between source and target")
        self.suffix_lineedit.setFixedWidth(160)
        self.suffix_lineedit.setEnabled(False)

        # Stretches on both sides keep the row centered regardless of group box width
        self.match_group.addStretch(1)
        self.match_group.addWidget(relationship_label)
        self.match_group.addWidget(self.radio_button_order)
        self.match_group.addWidget(self.radio_button_name)
        self.match_group.addWidget(self.suffix_lineedit)
        self.match_group.addStretch(1)
        self.match_group_offset.setLayout(self.match_group)

        # connections matchby name
        self.radio_button_name.toggled.connect(self.on_match_by_name_toggled)

        # creating TabWidget 
        self.main_tab_widget = QTabWidget()
        self.constraint_tab = QWidget()
        self.connection_tab = QWidget()
        self.copyskin_tab = QWidget()

        self.main_tab_widget.addTab(self.constraint_tab, "Constraint")
        self.main_tab_widget.addTab(self.connection_tab, "Connnection")
        self.main_tab_widget.addTab(self.copyskin_tab, "Copy Skin")

        # setToolTip (on the tab bar itself, not the page content)
        self.main_tab_widget.setTabToolTip(0, "Create or delete constraints between source and target objects")
        self.main_tab_widget.setTabToolTip(1, "Connect attributes directly between source and target objects")
        self.main_tab_widget.setTabToolTip(2, "Copy skin weights from source to target objects")

        # addLAyouts in main_layout
        self.main_layout.addLayout(self.objects_grid_layout)    
        divider_main = self.create_divider_for_ui(QFrame.HLine)
        self.main_layout.addWidget(divider_main)
        self.main_layout.addWidget(self.match_group_offset)  
        self.main_layout.addWidget(self.main_tab_widget)
        
        self.central_widget.setLayout(self.main_layout)

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
        self.constraint_type_combobox.setToolTip("Choose which constraint to create: Parent, Point, Orient, or Scale")

        constraint_type_layout.addWidget(constraint_type_label, alignment=Qt.AlignRight)
        constraint_type_layout.addWidget(self.constraint_type_combobox, alignment=Qt.AlignLeft)

        # maintain offset Options Creation 
        maintain_offset_layout = QHBoxLayout()
        maintain_offset_label = QLabel("Maintain Offset:")
        self.offset_radio_on = QRadioButton("On")
        self.offset_radio_off = QRadioButton("Off")
        self.offset_radio_off.setChecked(True)
        self.offset_radio_on.setToolTip("Keep the target's current offset from the source when constrained")
        self.offset_radio_off.setToolTip("Snap the target directly onto the source (no offset)")
        maintain_offset_layout.setContentsMargins(120, 0, 100, 0)
        maintain_offset_layout.setSpacing(0)
    
        maintain_offset_layout.addWidget(maintain_offset_label)
        maintain_offset_layout.addWidget(self.offset_radio_on)
        maintain_offset_layout.addWidget(self.offset_radio_off)

        # constraint adding everything to main Tab widget 
        constraint_main_layout.addLayout(constraint_type_layout) 
        constraint_main_layout.addLayout(maintain_offset_layout, alignment=Qt.AlignCenter)
        divider_offsets = self.create_divider_for_ui(QFrame.HLine)
        constraint_main_layout.addWidget(divider_offsets)

        self.constraint_tab.setLayout(constraint_main_layout)

        # creation constraint Axes Group 
        constraint_axes_group = QGroupBox("Constraint Axes Attributes")
        constraint_axes_group.setStyleSheet("""
            QGroupBox
                {
                font: 12px;
                color: white;
            }""")
        
        constraint_options_layout = QGridLayout()
        constraint_options_layout.setHorizontalSpacing(12)
        constraint_options_layout.setVerticalSpacing(8)
        constraint_options_layout.setColumnMinimumWidth(5, 24)
        translate_label = QLabel("Translate ")
        self.translate_all_checkbox_constraint = QCheckBox("All")
        self.translate_x_checkbox_constraint = QCheckBox("X")
        self.translate_y_checkbox_constraint = QCheckBox("Y")
        self.translate_z_checkbox_constraint = QCheckBox("Z")
        self.translate_all_checkbox_constraint.setToolTip("Constrain all Translate axes (locks X/Y/Z individually)")
        self.translate_x_checkbox_constraint.setToolTip("Constrain Translate X")
        self.translate_y_checkbox_constraint.setToolTip("Constrain Translate Y")
        self.translate_z_checkbox_constraint.setToolTip("Constrain Translate Z")

        rotate_label = QLabel("Rotate ")
        self.rotate_all_checkbox_constraint = QCheckBox("All")
        self.rotate_x_checkbox_constraint = QCheckBox("X")
        self.rotate_y_checkbox_constraint = QCheckBox("Y")
        self.rotate_z_checkbox_constraint = QCheckBox("Z")
        self.rotate_all_checkbox_constraint.setToolTip("Constrain all Rotate axes (locks X/Y/Z individually)")
        self.rotate_x_checkbox_constraint.setToolTip("Constrain Rotate X")
        self.rotate_y_checkbox_constraint.setToolTip("Constrain Rotate Y")
        self.rotate_z_checkbox_constraint.setToolTip("Constrain Rotate Z")

        scale_label = QLabel("Scale ")
        self.scale_all_checkbox_constraint = QCheckBox("All")
        self.scale_x_checkbox_constraint = QCheckBox("X")
        self.scale_y_checkbox_constraint = QCheckBox("Y")
        self.scale_z_checkbox_constraint = QCheckBox("Z")
        self.scale_all_checkbox_constraint.setToolTip("Constrain all Scale axes (locks X/Y/Z individually)")
        self.scale_x_checkbox_constraint.setToolTip("Constrain Scale X")
        self.scale_y_checkbox_constraint.setToolTip("Constrain Scale Y")
        self.scale_z_checkbox_constraint.setToolTip("Constrain Scale Z")

        # Reset button
        self.reset_constraint = self.primary_button("Reset")
        self.reset_constraint.setToolTip("Reset all axis checkboxes back to their default (All enabled)")

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
        constraint_options_layout.addWidget(self.reset_constraint, 0, 6, 3, 1, alignment=Qt.AlignCenter)
        self.reset_constraint.setFixedSize(60, 32)
        
        constraint_axes_group.setLayout(constraint_options_layout)
        constraint_main_layout.addWidget(constraint_axes_group)
        divider_offsets = self.create_divider_for_ui(QFrame.HLine)
        constraint_main_layout.addWidget(divider_offsets)

        # Constraint Button creation 
        self.constraint_button_layout = QHBoxLayout()
        self.create_constraint_btn = self.primary_button("Create Constraints")
        self.disconnect_constraint_btn = self.primary_button("Delete Constraints")
        self.constraint_button_layout.addWidget(self.create_constraint_btn)
        self.constraint_button_layout.addWidget(self.disconnect_constraint_btn)
        constraint_main_layout.addLayout(self.constraint_button_layout, alignment=Qt.AlignCenter)

        # Set Tool Tip
        self.create_constraint_btn.setToolTip("Create the selected constraint type from Source onto Target objects")
        self.disconnect_constraint_btn.setToolTip("Delete existing constraints from the Target objects")

        self.translate_all_checkbox_constraint.setChecked(True)
        self.rotate_all_checkbox_constraint.setChecked(True)
        self.scale_all_checkbox_constraint.setChecked(True)
        self.translate_x_checkbox_constraint.setChecked(True)
        self.translate_y_checkbox_constraint.setChecked(True)
        self.translate_z_checkbox_constraint.setChecked(True)
        self.rotate_x_checkbox_constraint.setChecked(True)
        self.rotate_y_checkbox_constraint.setChecked(True)
        self.rotate_z_checkbox_constraint.setChecked(True)
        self.scale_x_checkbox_constraint.setChecked(True)
        self.scale_y_checkbox_constraint.setChecked(True)
        self.scale_z_checkbox_constraint.setChecked(True)

        # signals for constraints
        self.translate_all_checkbox_constraint.toggled.connect(self.sync_translate_all_constraint)
        self.translate_x_checkbox_constraint.toggled.connect(self.sync_translate_axis_constraint)
        self.translate_y_checkbox_constraint.toggled.connect(self.sync_translate_axis_constraint)
        self.translate_z_checkbox_constraint.toggled.connect(self.sync_translate_axis_constraint)

        self.rotate_all_checkbox_constraint.toggled.connect(self.sync_rotate_all_constraint)
        self.rotate_x_checkbox_constraint.toggled.connect(self.sync_rotate_axis_constraint)
        self.rotate_y_checkbox_constraint.toggled.connect(self.sync_rotate_axis_constraint)
        self.rotate_z_checkbox_constraint.toggled.connect(self.sync_rotate_axis_constraint)

        self.scale_all_checkbox_constraint.toggled.connect(self.sync_scale_all_constraint)
        self.scale_x_checkbox_constraint.toggled.connect(self.sync_scale_axis_constraint)
        self.scale_y_checkbox_constraint.toggled.connect(self.sync_scale_axis_constraint)
        self.scale_z_checkbox_constraint.toggled.connect(self.sync_scale_axis_constraint)
        self.reset_constraint.clicked.connect(self.reset_constraint_options)

        self.create_constraint_btn.clicked.connect(
            lambda: self.dialog_message_box(
                "Create constraints confirmation", 
                "Are you sure to create the constraints ?",
                self.create_constraints))

        self.disconnect_constraint_btn.clicked.connect(
            lambda:self.dialog_message_box(
                "Delete constraints confirmation",
                "Are you sure to delete the constraints ?", 
                self.delete_constraints))

    def connection_tab_ui(self):
        # create The connection tab
        connection_tab_layout = QVBoxLayout()
        # creation connection Axes Group 
        self.connection_axes_group = QGroupBox("Connection Axes Attributes")
        self.connection_axes_group.setCheckable(True)
        self.connection_axes_group.setChecked(True)
        self.connection_axes_group.setToolTip("Uncheck to skip axis connections entirely")
        self.connection_options_layout = QGridLayout()
        translate_label = QLabel("Translate ")
        self.translate_all_checkbox_connection = QCheckBox("All")
        self.translate_x_checkbox_connection = QCheckBox("X")
        self.translate_y_checkbox_connection = QCheckBox("Y")
        self.translate_z_checkbox_connection = QCheckBox("Z")
        self.translate_all_checkbox_connection.setToolTip("Connect all Translate axes (locks X/Y/Z individually)")
        self.translate_x_checkbox_connection.setToolTip("Connect Translate X")
        self.translate_y_checkbox_connection.setToolTip("Connect Translate Y")
        self.translate_z_checkbox_connection.setToolTip("Connect Translate Z")

        rotate_label = QLabel("Rotate ")
        self.rotate_all_checkbox_connection = QCheckBox("All")
        self.rotate_x_checkbox_connection = QCheckBox("X")
        self.rotate_y_checkbox_connection = QCheckBox("Y")
        self.rotate_z_checkbox_connection = QCheckBox("Z")
        self.rotate_all_checkbox_connection.setToolTip("Connect all Rotate axes (locks X/Y/Z individually)")
        self.rotate_x_checkbox_connection.setToolTip("Connect Rotate X")
        self.rotate_y_checkbox_connection.setToolTip("Connect Rotate Y")
        self.rotate_z_checkbox_connection.setToolTip("Connect Rotate Z")

        scale_label = QLabel("Scale ")
        self.scale_all_checkbox_connection = QCheckBox("All")
        self.scale_x_checkbox_connection = QCheckBox("X")
        self.scale_y_checkbox_connection = QCheckBox("Y")
        self.scale_z_checkbox_connection = QCheckBox("Z")
        self.scale_all_checkbox_connection.setToolTip("Connect all Scale axes (locks X/Y/Z individually)")
        self.scale_x_checkbox_connection.setToolTip("Connect Scale X")
        self.scale_y_checkbox_connection.setToolTip("Connect Scale Y")
        self.scale_z_checkbox_connection.setToolTip("Connect Scale Z")

        # Reset button
        self.reset_connection_axes_button = self.primary_button("Reset")

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
        self.connection_options_layout.addWidget(self.reset_connection_axes_button, 2, 5, 2, 2)
        self.reset_connection_axes_button.setFixedSize(80, 25)

        # All connection Atrributes List
        self.driver_driven_group = QGroupBox("Custom Connection Attributes")
        self.driver_driven_group.setCheckable(True)
        self.driver_driven_group.setChecked(False)
        self.driver_driven_group.setToolTip("Enable to connect custom attributes instead of / in addition to the axes above")
        self.driver_driven_layout = QGridLayout()
        self.driver_attr_type_label = QLabel("Driver Attribute Type")
        self.driver_combobox = QComboBox()
        self.driver_attrs_listwidget = QListWidget()
        self.driven_attr_type_label = QLabel("Driven Attribute Type")
        self.driven_combobox = QComboBox()
        self.driven_attrs_listwidget = QListWidget()
        self.driver_attrs_listwidget.setToolTip("Attributes available on the Source objects")
        self.driven_attrs_listwidget.setToolTip("Attributes available on the Target objects")
        
        self.driver_combobox.addItem("All Attributes")
        self.driver_combobox.addItem("Default Attributes")
        self.driver_combobox.addItem("Custom Attributes")
        
        self.driven_combobox.addItem("All Attributes")
        self.driven_combobox.addItem("Default Attributes")
        self.driven_combobox.addItem("Custom Attributes")

        # self.add_attributes_button = QPushButton()
        # self.add_attributes_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        # self.add_attributes_button.setFixedSize(40, 30)
        # self.remove_item_button = QPushButton("Remove Item")
        # self.clear_attributes_button = QPushButton("Clear")

        self.driver_driven_layout.addWidget(self.driver_attr_type_label, 0, 0)
        self.driver_driven_layout.addWidget(self.driven_attr_type_label, 0, 2)
        self.driver_driven_layout.addWidget(self.driver_combobox, 1, 0)
        self.driver_driven_layout.addWidget(self.driven_combobox, 1, 2)
        divider_connection = self.create_divider_for_ui(QFrame.VLine)
        self.driver_driven_layout.addWidget(divider_connection, 0, 1, 3, 1)
        self.driver_driven_layout.addWidget(self.driver_attrs_listwidget, 2, 0)
        self.driver_driven_layout.addWidget(self.driven_attrs_listwidget, 2, 2)
        

        self.translate_all_checkbox_connection.setChecked(True)
        self.rotate_all_checkbox_connection.setChecked(True)
        self.scale_all_checkbox_connection.setChecked(True)
        self.translate_x_checkbox_connection.setChecked(True)
        self.translate_y_checkbox_connection.setChecked(True)
        self.translate_z_checkbox_connection.setChecked(True)
        self.rotate_x_checkbox_connection.setChecked(True)
        self.rotate_y_checkbox_connection.setChecked(True)
        self.rotate_z_checkbox_connection.setChecked(True)
        self.scale_x_checkbox_connection.setChecked(True)
        self.scale_y_checkbox_connection.setChecked(True)
        self.scale_z_checkbox_connection.setChecked(True)

        # Create connection buttons
        self.connection_button_layout = QHBoxLayout()
        self.create_connection_button = self.primary_button("Create Connections")
        self.disconnect_connection_button = self.primary_button("Delete Connections")

        connection_tab_layout.addWidget(self.connection_axes_group)

        divider_connection = self.create_divider_for_ui(QFrame.HLine)
        connection_tab_layout.addWidget(divider_connection)
        self.driver_driven_group.setLayout(self.driver_driven_layout)
        connection_tab_layout.addWidget(self.driver_driven_group)
        
        divider_connection = self.create_divider_for_ui(QFrame.HLine)
        connection_tab_layout.addWidget(divider_connection)
        self.connection_button_layout.addWidget(self.create_connection_button)
        self.connection_button_layout.addWidget(self.disconnect_connection_button)
        connection_tab_layout.addLayout(self.connection_button_layout)
        
        self.connection_axes_group.setLayout(self.connection_options_layout)
        self.connection_tab.setLayout(connection_tab_layout)

        # set ToolTips
        self.create_connection_button.setToolTip("Connect attributes from Source objects onto Target objects")
        self.disconnect_connection_button.setToolTip("Disconnect the attribute connections from the Target objects")
        self.driver_combobox.setToolTip("Attribute set to pull from on the Driver (Source) objects")
        self.driven_combobox.setToolTip("Attribute set to push to on the Driven (Target) objects")
        self.reset_connection_axes_button.setToolTip("Reset all axis checkboxes back to their default (All enabled)")

        # create signals
        self.translate_all_checkbox_connection.toggled.connect(self.sync_translate_all_connection)
        self.translate_x_checkbox_connection.toggled.connect(self.sync_translate_axis_connection)
        self.translate_y_checkbox_connection.toggled.connect(self.sync_translate_axis_connection)
        self.translate_z_checkbox_connection.toggled.connect(self.sync_translate_axis_connection)

        self.rotate_all_checkbox_connection.toggled.connect(self.sync_rotate_all_connection)
        self.rotate_x_checkbox_connection.toggled.connect(self.sync_rotate_axis_connection)
        self.rotate_y_checkbox_connection.toggled.connect(self.sync_rotate_axis_connection)
        self.rotate_z_checkbox_connection.toggled.connect(self.sync_rotate_axis_connection)

        self.scale_all_checkbox_connection.toggled.connect(self.sync_scale_all_connection)
        self.scale_x_checkbox_connection.toggled.connect(self.sync_scale_axis_connection)
        self.scale_y_checkbox_connection.toggled.connect(self.sync_scale_axis_connection)
        self.scale_z_checkbox_connection.toggled.connect(self.sync_scale_axis_connection)
        self.reset_connection_axes_button.clicked.connect(self.reset_connection_options)
        self.driver_driven_group.toggled.connect(self.driver_driven_connection_axes_enable)
        self.connection_axes_group.toggled.connect(self.connection_axes_enabled)

     
        self.source_obj_list.itemSelectionChanged.connect(
            lambda: self.update_driver_driven_listwidget_order(
                self.source_obj_list,
                self.driver_attrs_listwidget,
                self.driver_combobox.currentText(),
            )
        )
        self.driver_combobox.currentTextChanged.connect(
            lambda: self.update_driver_driven_listwidget_order(
                self.source_obj_list,
                self.driver_attrs_listwidget,
                self.driver_combobox.currentText(),
            )
        )

        self.target_obj_list.itemSelectionChanged.connect(
            lambda: self.update_driver_driven_listwidget_order(
                self.target_obj_list,
                self.driven_attrs_listwidget,
                self.driven_combobox.currentText(),
            )
        )
        self.driven_combobox.currentTextChanged.connect(
            lambda: self.update_driver_driven_listwidget_order(
                self.target_obj_list,
                self.driven_attrs_listwidget,
                self.driven_combobox.currentText(),
            )
        )

        # Name-match mode disables target_obj_list, so the driven list must instead
        # react to the source selection, the suffix, and the driven attribute
        # combobox used to resolve the target.
        self.source_obj_list.itemSelectionChanged.connect(self.update_driver_driven_listwidget_name)
        self.suffix_lineedit.textChanged.connect(self.update_driver_driven_listwidget_name)
        self.radio_button_name.toggled.connect(self.update_driver_driven_listwidget_name)
        self.driven_combobox.currentTextChanged.connect(self.update_driver_driven_listwidget_name)

        self.create_connection_button.clicked.connect(
            lambda: self.dialog_message_box(
                "Create connections confirmation", 
                "Are you sure to create the connections ?",
                self.create_connections))

        self.disconnect_connection_button.clicked.connect(
            lambda:self.dialog_message_box(
                "Delete connections confirmation",
                "Are you sure to delete the connections ?", 
                self.disconnect_connections))

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
        self.closest_point_radio_btn.setToolTip("Match each point to the closest point on the target surface (best for similar topology)")
        self.ray_cast_radio_btn.setToolTip("Match points by casting a ray along vertex normals onto the target surface")
        self.closest_component_radio_btn.setToolTip("Match each point to the closest component (vertex, edge, or face) on the target")
        self.uv_space_radio_btn.setToolTip("Match points using matching UV coordinates (requires matching UV sets)")

        self.influence_label_1 = QLabel("Influence Association 1: ")
        self.influence_label_2 = QLabel("Influence Association 2: ")
        self.influence_label_3 = QLabel("Influence Association 3: ")

        self.influence_combo_box_1 = QComboBox()
        self.influence_combo_box_1.addItems(INFLUENCE_ASSOCIATION_ITEMS)

        self.influence_combo_box_2 = QComboBox()
        self.influence_combo_box_2.addItems(INFLUENCE_ASSOCIATION_ITEMS)

        self.influence_combo_box_3 = QComboBox()
        self.influence_combo_box_3.addItems(INFLUENCE_ASSOCIATION_ITEMS)

        influence_tooltip = "Fallback method used to match influences (joints) between source and target skin clusters"
        self.influence_combo_box_1.setToolTip(influence_tooltip)
        self.influence_combo_box_2.setToolTip(influence_tooltip)
        self.influence_combo_box_3.setToolTip(influence_tooltip)

        self.association_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        association_options_layout = QVBoxLayout()
        association_options_layout.setSpacing(2)
        association_options_layout.setContentsMargins(0, 0, 0, 0)
        association_options_layout.addWidget(self.closest_point_radio_btn)
        association_options_layout.addWidget(self.ray_cast_radio_btn)
        association_options_layout.addWidget(self.closest_component_radio_btn)
        self.copyskin_form_layout.addRow(self.association_label, association_options_layout)

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
        self.copy_skin_btn.setToolTip("Copy skin weights from Source objects onto Target objects")

        copy_skin_group.setLayout(self.copyskin_form_layout)
        copyskin_tab_layout.addWidget(copy_skin_group)
        divider_copyskin = self.create_divider_for_ui(QFrame.HLine)
        copyskin_tab_layout.addWidget(divider_copyskin)
        copyskin_tab_layout.addLayout(self.copyskin_button_layout)
        self.copyskin_tab.setLayout(copyskin_tab_layout)

        # signals for copy Skin button 
        # self.copy_skin_btn.clicked.connect(self.copy_skins)

        self.copy_skin_btn.clicked.connect(
            lambda: self.dialog_message_box(
                "Copy Skin Confirmation", 
                "Are you sure you want to copy the weights?",
                self.copy_skins))

    def create_divider_for_ui(self, linetype):
        divider = QFrame()
        divider.setFrameShape(linetype)
        divider.setFrameShadow(QFrame.Sunken)
        return divider

    def get_translations(self, current_object):
        # Return all translated names
        # unlocked=True skips locked attrs, since connectAttr/constraints can't target them anyway
        custom_attributes = cmds.listAttr(current_object, keyable=True, unlocked=True)

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

    def get_custom_items(self, current_object):
        # Return user-defined items which is manually created
        custom_attributes = cmds.listAttr(current_object, userDefined=True) or []
        return custom_attributes

    def get_all_items(self, current_object):
        # Return all items
        custom_attributes = cmds.listAttr(current_object, keyable=True)
        return custom_attributes
    
    def get_object_pairs_by_name_match(self, suffix, source_items):
        # source_items is a list of full DAG paths 
        object_pairs = []
        for source_item in source_items:
            # full DAG paths start with "|", so split[0] it 
            top_level_group = source_item.split("|")[1]
            source_short_name = source_item.rsplit("|", 1)[-1]
            # Naming convention: drop the source's trailing "_<token>" 
            # and rebuild the target name as "<base><suffix>" 
            source_base_name = source_short_name.rsplit("_", 1)[0]
            target_name = f"{source_base_name}{suffix}"
            # print(target_name)
            all_descendants = cmds.listRelatives(top_level_group, ad=True, f=True) or []
            target_obj = []
            for descendant in all_descendants:
                if descendant.endswith("|" + target_name):
                    target_obj = descendant
                    # print(target_obj)

            object_pairs.append((source_item, target_obj))
        return object_pairs

    def get_object_pairs_by_order(self, source_items, target_objects):
      
        if len(source_items) == 1 and len(target_objects) > 1:
            print("One source object mapped to {} target objects.".format(len(target_objects)))
            object_pairs = []
            for target_obj in target_objects:
                object_pairs.append((source_items[0], target_obj))
            return object_pairs

        if len(source_items) != len(target_objects):
            return None

        object_pairs = []
        for index in range(len(source_items)):
            object_pairs.append((source_items[index], target_objects[index]))
        return object_pairs

    def get_matching_side_paths(self, list_widget_object):
        # Returns the full-path list that mirrors this widget's own rows(source widget->source paths,target widget->target paths)
        if list_widget_object is self.source_obj_list:
            return self.source_object_paths
        if list_widget_object is self.target_obj_list:
            return self.target_object_paths

    def get_opposite_side_paths(self, list_widget_object):
        # this is getting what the source and target objects list contains so it can be checked if objects are already added in the other side 
        if list_widget_object is self.source_obj_list:
            return self.target_object_paths
        if list_widget_object is self.target_obj_list:
            return self.source_object_paths

    @Slot()
    def dialog_message_box(self, title, message, on_confirm):
        response = QMessageBox.question(
            self,
            title,
            message
        )
        if response == QMessageBox.Yes:
            # main function called after confirmation
            on_confirm()
        else:
            print("User Canceled the operation")

    @Slot()
    def update_driver_driven_listwidget_order(self, list_widget, target_list_widget, driver_driven_combobox_value):
        # Repopulates the driver/driven attribute list for whatever object is currently selected in list_widget. Wired to both source and target list
        current_item = list_widget.currentItem()
        if not current_item:
            return

        row = list_widget.row(current_item)
        object_paths = self.get_matching_side_paths(list_widget)
        current_object_selected = object_paths[row]

        target_list_widget.clear()
        if driver_driven_combobox_value == "Default Attributes":
            items = self.get_translations(current_object_selected)
        elif driver_driven_combobox_value == "Custom Attributes":
            items = self.get_custom_items(current_object_selected)
        elif driver_driven_combobox_value == "All Attributes":
            items = self.get_all_items(current_object_selected)
        else:
            items = []
        target_list_widget.addItems(items)

    @Slot()
    def update_driver_driven_listwidget_name(self):
        # Name-match counterpart to update_driver_driven_listwidget_order above. The
        # target isn't selected from a list here - it's resolved from the selected
    
        if self.radio_button_name.isChecked():
            current_item = self.source_obj_list.currentItem()
            if not current_item:
                return
            row = self.source_obj_list.row(current_item)
            current_object_selected = self.source_object_paths[row]

            suffix = self.suffix_lineedit.text().strip()
            self.driven_attrs_listwidget.clear()
            if not suffix:
                return

            object_pairs = self.get_object_pairs_by_name_match(suffix, [current_object_selected])
            if object_pairs:
                target_obj = object_pairs[0][1]
            else:
                target_obj = []
            if not target_obj:
                self.dialog_box_window("No matching target object found for suffix.")
                return
        else:
            current_item = self.target_obj_list.currentItem()
            if not current_item:
                return
            row = self.target_obj_list.row(current_item)
            target_obj = self.target_object_paths[row]

            # target_list_widget.clear()
            self.driven_attrs_listwidget.clear()

        driven_combobox_value = self.driven_combobox.currentText()
        """
        driven_combobox's actual items are "Default Attributes","Custom Attributes","All Attributes"
        """
        if driven_combobox_value == "Default Attributes":
            items = self.get_translations(target_obj)
        elif driven_combobox_value == "Custom Attributes":
            items = self.get_custom_items(target_obj)
        elif driven_combobox_value == "All Attributes":
            items = self.get_all_items(target_obj)
        else:
            items = []
        self.driven_attrs_listwidget.addItems(items)

    @Slot()
    def load_selected_objects(self, list_widget_object):
        # Get selected objects in Maya
        selected_items = cmds.ls(selection=True, long=True) or []
        if not selected_items:
            cmds.warning("No objects selected in Maya.")
            self.dialog_box_window("ERROR: No objects selected in Maya.")
            return

        object_paths = self.get_matching_side_paths(list_widget_object)
        other_object_paths = self.get_opposite_side_paths(list_widget_object)

        # objects already present in the list should not be added again
        existing_objects = set(object_paths)
        # an object already used on the other side (source/target) cannot be added here
        other_existing_objects = set(other_object_paths)

        added_count = 0
        skipped = []

        # appending keeps object_paths[row] aligned with the widget's row order,
        for selected_item in selected_items:
            short_name = selected_item.rsplit("|", 1)[-1]
            if selected_item in existing_objects:
                cmds.warning("{} is already in the list.".format(short_name))
                skipped.append("{} (already in list)".format(short_name))
                continue

            if selected_item in other_existing_objects:
                cmds.warning("{} is already used on the other side.".format(short_name))
                skipped.append("{} (used on other side)".format(short_name))
                continue

            object_paths.append(selected_item)
            list_widget_object.addItem(short_name)
            added_count += 1

        summary = "Added {} objects to the list.".format(added_count)
        if skipped:
            summary += "\nSkipped {}: {}".format(len(skipped), ", ".join(skipped))
        self.dialog_box_window(summary)
    
    @Slot()
    def on_match_by_name_toggled(self, checked):
        """
        checked = Name mode: target is resolved automatically from source + suffix,
        so the manual target-list controls are disabled and the suffix box is
        enabled; 
        unchecked = Order mode, the reverse. Both branches below apply the
        same enable/disable state - the only real difference is clearing the driven
        attribute list when switching into Name mode, since the previous
        target-based selection no longer applies.
        """
        if checked:
            self.target_obj_list.setEnabled(not checked)
            self.load_target_obj_button.setEnabled(not checked)
            self.clear_list_target_button.setEnabled(not checked)
            self.target_move_up_btn.setEnabled(not checked)
            self.target_move_down_btn.setEnabled(not checked)
            self.suffix_lineedit.setEnabled(checked)
            self.driven_attrs_listwidget.clear()
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
        self.get_matching_side_paths(list_widget_object).clear()
        print(f"List Box Cleared")

    # The widget only displays short names, so any reorder must apply the same index change to the parallel object_paths list (get_matching_side_paths)
    @Slot()
    def move_selected_item_up(self, list_widget_object):
        row = list_widget_object.currentRow()
        if row <= 0:
            return
        item = list_widget_object.takeItem(row)
        list_widget_object.insertItem(row - 1, item)
        list_widget_object.setCurrentRow(row - 1)

        object_paths = self.get_matching_side_paths(list_widget_object)
        object_paths[row - 1], object_paths[row] = object_paths[row], object_paths[row - 1]
       

    @Slot()
    def move_selected_item_down(self, list_widget_object):
        row = list_widget_object.currentRow()
        if row < 0 or row >= list_widget_object.count() - 1:
            return

        item = list_widget_object.takeItem(row)
        list_widget_object.insertItem(row + 1, item)
        list_widget_object.setCurrentRow(row + 1)

        object_paths = self.get_matching_side_paths(list_widget_object)
        object_paths[row], object_paths[row + 1] = object_paths[row + 1], object_paths[row]


    # Keeps "All" and the X/Y/Z checkboxes in sync without disabling anything.
    # blockSignals prevents each setChecked() below from re-triggering these
    # same handlers and causing a feedback loop (same pattern repeats for
    # rotate/scale below, and again for the *_connection versions further down).
    @Slot()
    def sync_translate_all_constraint(self, checked):
        for checkbox in (self.translate_x_checkbox_constraint, self.translate_y_checkbox_constraint, self.translate_z_checkbox_constraint):
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    @Slot()
    def sync_translate_axis_constraint(self, checked):
        allchecked = (self.translate_x_checkbox_constraint.isChecked()
                       and self.translate_y_checkbox_constraint.isChecked()
                       and self.translate_z_checkbox_constraint.isChecked())
        self.translate_all_checkbox_constraint.blockSignals(True)
        self.translate_all_checkbox_constraint.setChecked(allchecked)
        self.translate_all_checkbox_constraint.blockSignals(False)

    @Slot()
    def sync_rotate_all_constraint(self, checked):
        for checkbox in (self.rotate_x_checkbox_constraint, self.rotate_y_checkbox_constraint, self.rotate_z_checkbox_constraint):
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    @Slot()
    def sync_rotate_axis_constraint(self, checked):
        allchecked = (self.rotate_x_checkbox_constraint.isChecked()
                       and self.rotate_y_checkbox_constraint.isChecked()
                       and self.rotate_z_checkbox_constraint.isChecked())
        self.rotate_all_checkbox_constraint.blockSignals(True)
        self.rotate_all_checkbox_constraint.setChecked(allchecked)
        self.rotate_all_checkbox_constraint.blockSignals(False)

    @Slot()
    def sync_scale_all_constraint(self, checked):
        for checkbox in (self.scale_x_checkbox_constraint, self.scale_y_checkbox_constraint, self.scale_z_checkbox_constraint):
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    @Slot()
    def sync_scale_axis_constraint(self, checked):
        allchecked = (self.scale_x_checkbox_constraint.isChecked()
                       and self.scale_y_checkbox_constraint.isChecked()
                       and self.scale_z_checkbox_constraint.isChecked())
        self.scale_all_checkbox_constraint.blockSignals(True)
        self.scale_all_checkbox_constraint.setChecked(allchecked)
        self.scale_all_checkbox_constraint.blockSignals(False)

    @Slot()
    def create_constraints(self):
        # openChunk/closeChunk group every constraint created below into one undo step
        cmds.undoInfo(openChunk=True)
        try:
            source_items = self.get_items_from_list(self.source_obj_list)
            target_objects = self.get_items_from_list(self.target_obj_list)
            # print(source_items)
            # print(target_objects)

            # Index into constraint_type_combobox: 0=Parent, 1=Point, 2=Orient, 3=Scale
            # (must stay in sync with the addItem() order in constraint_tab_ui)
            constraint_type = self.constraint_type_combobox.currentIndex()
            # print(constraint_type)
            maintain_offset_enabled = self.offset_radio_on.isChecked()
            # print(maintain_offset_enabled)

            # these feed Maya's skip= args, so an empty list means "skip nothing" (constrain every axis)
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
    
            # match by order 
            if self.radio_button_order.isChecked():

                if not source_items or not target_objects:
                    print("Source and Target object lists need to be populated.")
                    self.dialog_box_window("ERROR: Source and Target object lists need to be populated.")
                    return

                object_pairs = self.get_object_pairs_by_order(source_items, target_objects)
                if object_pairs is None:
                    cmds.warning("Source and Target lists must contain the same number of objects.")
                    self.dialog_box_window("ERROR: Source and Target lists must contain the same number of objects.")
                    return

                for source_item, target_obj in object_pairs:
                    if constraint_type == 0:
                        cmds.parentConstraint(
                            source_item,
                            target_obj,
                            mo=maintain_offset_enabled,
                            skipTranslate=skip_translate,
                            skipRotate=skip_rotate
                            )
                    elif constraint_type == 1:
                        cmds.pointConstraint(
                            source_item,
                            target_obj,
                            mo=maintain_offset_enabled,
                            skip=skip_translate
                            )
                    if constraint_type == 2:
                        cmds.orientConstraint(
                            source_item,
                            target_obj,
                            mo=maintain_offset_enabled,
                            skip=skip_rotate
                            )
                    if constraint_type == 3:
                        cmds.scaleConstraint(
                            source_item,
                            target_obj,
                            mo=maintain_offset_enabled,
                            skip=skip_scale
                            )

            # match by name 
            else:
                # Only the source list is Checked if it is filled
                if not source_items:
                    cmds.warning("Source object list needs to be populated.")
                    self.dialog_box_window("ERROR: Source object list needs to be populated.")
                    return
                
                suffix_name = self.suffix_lineedit.text().strip()
                object_pairs = self.get_object_pairs_by_name_match(suffix_name, self.source_object_paths)
                # print(object_pairs)

                # connect constraints 
                for source_item, target_obj in object_pairs:
                    if not cmds.objExists(target_obj):
                        cmds.warning("{} does not exist.".format(target_obj))
                        continue
                    # target_dict.append(target_name)
                    # print(target_suffix)
                    if constraint_type == 0:
                        cmds.parentConstraint(source_item, target_obj, mo=maintain_offset_enabled, skipTranslate=skip_translate, skipRotate=skip_rotate)
                    elif constraint_type == 1:
                        cmds.pointConstraint(source_item, target_obj, mo=maintain_offset_enabled, skip=skip_translate)
                    if constraint_type == 2:
                        cmds.orientConstraint(source_item, target_obj, mo=maintain_offset_enabled, skip=skip_rotate)
                    if constraint_type == 3:
                        cmds.scaleConstraint(source_item, target_obj, mo=maintain_offset_enabled, skip=skip_scale)  
            self.dialog_box_window("Constraints completed")
                

        finally:
            cmds.undoInfo(closeChunk=True)
        
    def connect_attrs(self, source_item, target_obj, connection_attrs):
        # Connects each attribute individually so one missing/locked attribute only skips itself instead of aborting the whole batch for this object pair
        if not cmds.objExists(source_item):
            cmds.warning("Source object {} does not exist.".format(source_item))
            return
        if not cmds.objExists(target_obj):
            cmds.warning("Target object {} does not exist.".format(target_obj))
            return

        for attribute in connection_attrs:
            attr = attribute.strip()
            if not attr:
                continue

            source_attr = "{}.{}".format(source_item, attr)
            target_attr = "{}.{}".format(target_obj, attr)
            if not cmds.objExists(source_attr):
                cmds.warning("Attribute {} does not exist on {}.".format(attr, source_item))
                continue
            if not cmds.objExists(target_attr):
                cmds.warning("Attribute {} does not exist on {}.".format(attr, target_obj))
                continue
            cmds.connectAttr(source_attr, target_attr, force=True)
            connected = True

        print("Connected {} -> {}".format(source_item, target_obj))

    def connect_selected_custom_attribute(self, source_item, target_obj, driver_attr, driven_attr):
        # Single-pair counterpart to connect_attrs, used by the custom driver/driven attribute mode where the source and target attribute names can differ
        if not cmds.objExists(source_item):
            cmds.warning("Source object {} does not exist.".format(source_item))
            return
        if not cmds.objExists(target_obj):
            cmds.warning("Target object {} does not exist.".format(target_obj))
            return

        source_attr = "{}.{}".format(source_item, driver_attr)
        target_attr = "{}.{}".format(target_obj, driven_attr)
        if not cmds.objExists(source_attr):
            cmds.warning("Attribute {} does not exist on {}.".format(driver_attr, source_item))
            return
        if not cmds.objExists(target_attr):
            cmds.warning("Attribute {} does not exist on {}.".format(driven_attr, target_obj))
            return

        cmds.connectAttr(source_attr, target_attr, force=True)
        print("Connected {} -> {}".format(source_attr, target_attr))

    def get_selected_custom_attributes(self):
        # Resolves the single currently-selected driver/driven attribute pair, returned
        source_item = self.source_obj_list.currentItem()
        driver_item = self.driver_attrs_listwidget.currentItem()
        driven_item = self.driven_attrs_listwidget.currentItem()

        # Nothing to connect unless a source object and one attribute in each of the
        # driver/driven list widgets are all selected at the same time
        if not source_item or not driver_item or not driven_item:
            return []

        source_row = self.source_obj_list.row(source_item)
        source_obj = self.source_object_paths[source_row]

        if self.radio_button_name.isChecked():
            # Name mode: resolve the target the same way update_driver_driven_listwidget_name
            suffix_name = self.suffix_lineedit.text().strip()
            if not suffix_name:
                return []
            object_pairs = self.get_object_pairs_by_name_match(suffix_name, [source_obj])
            if object_pairs:
                target_obj = object_pairs[0][1]
            else:
                target_obj = []
            if not target_obj:
                return []
        else:
            # Order mode: target comes directly from whatever is selected in target_obj_list
            target_item = self.target_obj_list.currentItem()
            if not target_item:
                return []
            target_row = self.target_obj_list.row(target_item)
            target_obj = self.target_object_paths[target_row]

        driver_attr = driver_item.text().strip()
        driven_attr = driven_item.text().strip()

        # Belt-and-braces re-check now that target_obj and both attr names are resolved
        if not source_obj or not target_obj or not driver_attr or not driven_attr:
            return []

        selected_pairs = []
        selected_pairs.append((source_obj, target_obj, driver_attr, driven_attr))
        return selected_pairs

    @Slot()
    def create_connections(self):
        cmds.undoInfo(openChunk=True)
        try:
            source_items = self.get_items_from_list(self.source_obj_list)
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
                # Always empty on this path - custom attribute connections are handled
                # entirely by the driver_driven_group branch below, which returns
                # early. Kept only so the "anything to connect" check further down has
                # something to test.
                custom_attrs = []
            elif self.driver_driven_group.isChecked():
                selected_pairs = self.get_selected_custom_attributes()
                if not selected_pairs:
                    self.dialog_box_window("ERROR: Select driver and driven attributes.")
                    return

                for source_obj, target_obj, driver_attr, driven_attr in selected_pairs:
                    self.connect_selected_custom_attribute(source_obj, target_obj, driver_attr, driven_attr)

                self.dialog_box_window("Connections done.")
                return
            else:
                self.dialog_box_window("ERROR: Select a connection section to run.")
                return

            if not connection_attrs and not custom_attrs:
                cmds.warning("No translate/rotate/scale channels or custom attributes selected to connect.")
                self.dialog_box_window("ERROR: No channels or custom attributes selected to connect.")
                return

            # match by order
            if self.radio_button_order.isChecked():
                if not source_items or not target_objects:
                    print("Source and Target object lists need to be populated.")
                    self.dialog_box_window("ERROR: Source and Target object lists need to be populated.")
                    return

                object_pairs = self.get_object_pairs_by_order(source_items, target_objects)
                if object_pairs is None:
                    cmds.warning("Source and Target lists must contain the same number of objects.")
                    self.dialog_box_window("ERROR: Source and Target lists must contain the same number of objects.")
                    return

                for source_obj, target_obj in object_pairs:
                    if connection_attrs:
                        self.connect_attrs(source_obj, target_obj, connection_attrs)
                    if custom_attrs:
                        self.connect_attrs(source_obj, target_obj, custom_attrs)

            # match by name
            else:
                if not source_items:
                    cmds.warning("Source object list needs to be populated.")
                    self.dialog_box_window("ERROR: Source object list needs to be populated.")
                    return

                suffix_name = self.suffix_lineedit.text().strip()
                object_pairs = self.get_object_pairs_by_name_match(suffix_name, self.source_object_paths)
                # print(object_pairs)

                for source_obj, target_obj in object_pairs:
                    if not cmds.objExists(target_obj):
                        cmds.warning("{} does not exist.".format(target_obj))
                        continue

                    if connection_attrs:
                        self.connect_attrs(source_obj, target_obj, connection_attrs)
                    if custom_attrs:
                        self.connect_attrs(source_obj, target_obj, custom_attrs)

            self.dialog_box_window("Connections done.")
        finally:
            cmds.undoInfo(closeChunk=True)

    def has_skin_cluster(self, source_objects):
        if not source_objects:
            return False

        if not cmds.objExists(source_objects):
            return False

        # skinCluster is upstream deformation history, not a direct attribute of the
        # mesh, so we have to search history for one rather than querying it directly
        history_of_skin = cmds.listHistory(source_objects)
        skin_clusters = cmds.ls(history_of_skin, type="skinCluster")

        if skin_clusters:
            return True

        return False

    def copy_skin_weights_to_mesh(self, source_obj, target_obj, association_type, influence_association_list):
        source_skin = cmds.ls(cmds.listHistory(source_obj), type="skinCluster")
        if not source_skin:
            cmds.warning("{} has no skinCluster.".format(source_obj))
            return False

        source_skin = source_skin[0]

        target_skin = cmds.ls(cmds.listHistory(target_obj), type="skinCluster")
        if not target_skin:
            # target has no skinCluster yet - bind it to the source's influences before copying weights
            influences_joint_source = cmds.skinCluster(source_skin, q=True, influence=True)
            # bindMethod/skinMethod barely matter here - copySkinWeights 
            target_skin = cmds.skinCluster(
                influences_joint_source, 
                target_obj, 
                toSelectedBones=True, 
                bindMethod=0, 
                skinMethod=0, 
                normalizeWeights=1
                )
            
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
            influenceAssociation=influence_association_list,
        )
        print("Copied {} -> {}".format(source_obj, target_obj))
        return True

    @Slot()
    def copy_skins(self):
        # contains the core logic for copy skin wts and its validations 
        cmds.undoInfo(openChunk=True)
        try:
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

            # association settings on surface association 
            # Maps the combobox labels to the keywords copySkinWeights' influenceAssociation expects
            association_map = {
                "Closest Joint": "closestJoint",
                "Closest Bone": "closestBone",
                "Name": "name",
                "Label": "label",
                "One To One": "oneToOne",
            }

            # copySkinWeights tries each influenceAssociation entry in order as a
            # fallback until influences resolve; "None" means "skip this fallback
            # slot" rather than being passed through, since it isn't a valid Maya keyword
            influence_association_list = []
            for combo in (self.influence_combo_box_1, self.influence_combo_box_2, self.influence_combo_box_3):
                influence_text = combo.currentText()
                if influence_text == "None":
                    continue
                influence_association_list.append(association_map[influence_text])

            # tallied instead of shown per-object, so a batch copy ends in one summary
            # dialog rather than a stack of popups the user has to click through
            copied_count = 0
            skipped = []

            # match by order
            if self.radio_button_order.isChecked():
                # NOTE: uses "and" here, unlike the equivalent guards in
                # create_constraints/create_connections which use "or" - if both
                # lists are empty this check is skipped and the loop below silently
                # "copies" 0 objects instead of erroring
                if not source_objects and target_objects:
                    print("Source and Target object lists need to be populated.")
                    self.dialog_box_window("ERROR: Source and Target object lists need to be populated.")
                    return

                object_pairs = self.get_object_pairs_by_order(source_objects, target_objects)
                if object_pairs is None:
                    cmds.warning("Source and Target lists must contain the same number of objects.")
                    self.dialog_box_window("ERROR: Source and Target lists must contain the same number of objects.")
                    return

                for source_obj, target_obj in object_pairs:
                    if not self.has_skin_cluster(source_obj):
                        cmds.warning("{} has no skinCluster.".format(source_obj))
                        skipped.append("{} (no skinCluster)".format(source_obj))
                        continue
                    if self.copy_skin_weights_to_mesh(source_obj, target_obj, association_type, influence_association_list):
                        copied_count += 1
                    else:
                        skipped.append("{} (failed)".format(source_obj))

            # match by name
            else:
                if not source_objects:
                    cmds.warning("Source object list needs to be populated.")
                    self.dialog_box_window("ERROR: Source object list needs to be populated.")
                    return

                suffix_name = self.suffix_lineedit.text().strip()
                object_pairs = self.get_object_pairs_by_name_match(suffix_name, self.source_object_paths)

                for source_obj, target_obj in object_pairs:
                    if not self.has_skin_cluster(source_obj):
                        cmds.warning("{} has no skinCluster.".format(source_obj))
                        skipped.append("{} (no skinCluster)".format(source_obj))
                        continue

                    if not cmds.objExists(target_obj):
                        cmds.warning("{} does not exist.".format(target_obj))
                        skipped.append("{} (target missing)".format(target_obj))
                        continue
                    
                    # copy skin weghts command 
                    if self.copy_skin_weights_to_mesh(source_obj, target_obj, association_type, influence_association_list):
                        copied_count += 1
                    else:
                        skipped.append("{} (failed)".format(source_obj))

            summary = "Copied skin weights for {} object(s).".format(copied_count)
            if skipped:
                summary += "\nSkipped {}: {}".format(len(skipped), ", ".join(skipped))
            self.dialog_box_window(summary)
        finally:
            cmds.undoInfo(closeChunk=True)

    @Slot()
    def sync_translate_all_connection(self, checked):
        for checkbox in (self.translate_x_checkbox_connection, self.translate_y_checkbox_connection, self.translate_z_checkbox_connection):
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    @Slot()
    def sync_translate_axis_connection(self, checked):
        allchecked = (self.translate_x_checkbox_connection.isChecked()
                       and self.translate_y_checkbox_connection.isChecked()
                       and self.translate_z_checkbox_connection.isChecked())
        self.translate_all_checkbox_connection.blockSignals(True)
        self.translate_all_checkbox_connection.setChecked(allchecked)
        self.translate_all_checkbox_connection.blockSignals(False)

    @Slot()
    def sync_rotate_all_connection(self, checked):
        for checkbox in (self.rotate_x_checkbox_connection, self.rotate_y_checkbox_connection, self.rotate_z_checkbox_connection):
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    @Slot()
    def sync_rotate_axis_connection(self, checked):
        allchecked = (self.rotate_x_checkbox_connection.isChecked()
                       and self.rotate_y_checkbox_connection.isChecked()
                       and self.rotate_z_checkbox_connection.isChecked())
        self.rotate_all_checkbox_connection.blockSignals(True)
        self.rotate_all_checkbox_connection.setChecked(allchecked)
        self.rotate_all_checkbox_connection.blockSignals(False)

    @Slot()
    def sync_scale_all_connection(self, checked):
        for checkbox in (self.scale_x_checkbox_connection, self.scale_y_checkbox_connection, self.scale_z_checkbox_connection):
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    @Slot()
    def sync_scale_axis_connection(self, checked):
        allchecked = (self.scale_x_checkbox_connection.isChecked()
                       and self.scale_y_checkbox_connection.isChecked()
                       and self.scale_z_checkbox_connection.isChecked())
        self.scale_all_checkbox_connection.blockSignals(True)
        self.scale_all_checkbox_connection.setChecked(allchecked)
        self.scale_all_checkbox_connection.blockSignals(False)

    # These reset the axis to default values 
    @Slot()
    def reset_connection_options(self):
        # Only the "All" boxes need to be set - each one's toggled signal runs the
        self.translate_all_checkbox_connection.setChecked(True)
        self.rotate_all_checkbox_connection.setChecked(True)
        self.scale_all_checkbox_connection.setChecked(True)

    @Slot()
    def reset_constraint_options(self):
        # Only the "All" boxes need to be set - each one's toggled signal runs the
        # matching sync_*_all_* handler above, which cascades the checked state down
        # to the X/Y/Z boxes automatically.
        self.translate_all_checkbox_constraint.setChecked(True)
        self.rotate_all_checkbox_constraint.setChecked(True)
        self.scale_all_checkbox_constraint.setChecked(True)

    @Slot()
    def disconnect_connections(self):
        # this is responsible for disconnecting connections that were created 
        disconnected_any = False
        source_objects = self.get_items_from_list(self.source_obj_list)
        object_pairs = []

        # Match by order
        if self.radio_button_order.isChecked():
            target_objects = self.get_items_from_list(self.target_obj_list)

            if not source_objects or not target_objects:
                print("Source and Target object lists need to be populated.")
                self.dialog_box_window("ERROR: Source and Target object lists need to be populated.")
                return

            object_pairs = self.get_object_pairs_by_order(source_objects, target_objects)
            if object_pairs is None:
                cmds.warning("Source and Target lists must contain the same number of objects.")
                self.dialog_box_window("ERROR: Source and Target lists must contain the same number of objects.")
                return

        # Match by name
        else:
            if not source_objects:
                cmds.warning("Source object list needs to be populated.")
                self.dialog_box_window("ERROR: Source object list needs to be populated.")
                return

            suffix_name = self.suffix_lineedit.text().strip()
            object_pairs = self.get_object_pairs_by_name_match(suffix_name, self.source_object_paths)
            print(object_pairs)
            
        # Disconnect connections
        for source_obj, target_obj in object_pairs:
            if not cmds.objExists(source_obj) or not cmds.objExists(target_obj):
                continue

            # NOTE: this looks up ALL outgoing connections from source_obj, not just
            # the ones feeding target_obj specifically - target_obj above is only
            # used for the existence check, so a source driving multiple objects
            # gets fully disconnected from all of them here, not just this pair
            connection_attributes = cmds.listConnections(
                source_obj, 
                destination=True, 
                source=False, 
                plugs=True, 
                connections=True
                ) or []

            # connections=True returns a flat list of alternating
            # [source_plug, destination_plug] pairs, so step through two at a time
            for connection_index in range(0, len(connection_attributes), 2):
                try:
                    cmds.disconnectAttr(
                        connection_attributes[connection_index],
                        connection_attributes[connection_index + 1])
                    
                    print(f"Disconnected {connection_attributes[connection_index]} -> {connection_attributes[connection_index + 1]}")
                    disconnected_any = True

                except RuntimeError as exc:
                    print(f"Unable to disconnect {connection_attributes[connection_index]} -> {connection_attributes[connection_index + 1]}: {exc}")

        if disconnected_any:
            self.dialog_box_window("Disconnected matching connections.")
        else:
            self.dialog_box_window("No matching connections found to disconnect.")

    @Slot()
    def delete_constraints(self):
        source_objects = self.get_items_from_list(self.source_obj_list)
        deleted_any = False

        for source_obj in source_objects:
            # A constraint node takes the source's transform as input, so it shows up
            # as a connection on source_obj even though it's the target it actually drives
            constraints = cmds.listConnections(source_obj, type="constraint") or []
            if constraints:
                cmds.delete(constraints)
                deleted_any = True

        if deleted_any:
            self.dialog_box_window("Deleted target constraints.")
        else:
            self.dialog_box_window("No constraints found on target objects.")

    # connection_axes_group and driver_driven_group are two independent checkable
    # QGroupBoxes acting like a 2-way radio button: enabling one turns the other off.
    @Slot()
    def connection_axes_enabled(self, checked):
        if checked:
            self.driver_driven_group.setChecked(False)
            self.connection_axes_group.setChecked(True)
        
    @Slot()
    def driver_driven_connection_axes_enable(self, checked):
        if checked:
            self.connection_axes_group.setChecked(False)
            self.driver_driven_group.setChecked(True)
               
    def get_items_from_list(self, list_widget_object):
        # The widget itself only displays short names; the authoritative full DAG
        # paths live in the parallel object_paths list, indexed by the same row order
        object_paths = self.get_matching_side_paths(list_widget_object)
        items = []
        for row in range(list_widget_object.count()):
            items.append(object_paths[row])
        return items

def show_window():
    global my_window
    # check if already window open close
    # Closes any previously opened instance first so re-running this script doesn't
    # stack duplicate windows; the except below covers the first run, when my_window doesn't exist yet
    try:
        my_window.close()
        my_window.deleteLater()
    except:
        pass

    maya_main_window = get_maya_main_window()
    my_window = RiggingUtilityTool(parent=maya_main_window)
    my_window.show()



