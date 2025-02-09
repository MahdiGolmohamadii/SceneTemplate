import sys
from PySide6 import QtCore, QtGui, QtWidgets


class UseWindow(QtWidgets.QDialog):

    def __init__(self, scene_setup, code, parent=None):
        super().__init__(parent)

        self.sc = scene_setup
        self.code = code
        self.setWindowTitle('creat')
        self.setMinimumSize(300,200)
        self.create_widget()
        self.create_layout()
        self.create_conections()

    def create_widget(self):

        self.file_name_le = QtWidgets.QLineEdit()
        self.destination_path_le = QtWidgets.QLineEdit()
        self.destination_path_btn = QtWidgets.QPushButton()

        self.creat_btn = QtWidgets.QPushButton('Creat')
        self.cancel_btn = QtWidgets.QPushButton('Cancel')

    def create_layout(self):
        
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(self.file_name_le)

        destination_layout = QtWidgets.QHBoxLayout()
        destination_layout.addWidget(self.destination_path_le)
        destination_layout.addWidget(self.destination_path_btn)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('file name:', name_layout)
        form_layout.addRow('destination:', destination_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.creat_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_conections(self):
        self.destination_path_btn.clicked.connect(self.destination_btn_pressed)
        self.creat_btn.clicked.connect(self.use_btn_pressed)
        self.cancel_btn.clicked.connect(self.close)

    def destination_btn_pressed(self):
        path = self.open_file_dialog()
        self.destination_path_le.setText(path)

    def use_btn_pressed(self):
        if self.file_name_le.text() and self.destination_path_le.text():
            self.sc.open_scene(self.code, self.destination_path_le.text())
        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No name And/Or No destination')
            msg.setWindowTitle("Error")
            msg.exec()

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptOpen)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            print("Selected File:", selected_files[0])
            return selected_files[0]


class AddNewTemplateWindow(QtWidgets.QDialog):

    def __init__(self, parent, scene_setup):
        super().__init__(parent)
        
        self.sc = scene_setup
        
        self.setWindowTitle('Add New Template')
        self.setMinimumSize(300,500)
        
        self.create_widget()
        self.create_layout()
        self.create_conections()

    def create_widget(self):
        self.template_code_le = QtWidgets.QLineEdit()
        self.template_name_le = QtWidgets.QLineEdit()

        self.software_cd = QtWidgets.QComboBox()
        self.software_cd.addItem('Maya')
        self.software_cd.addItem('Blender')
        self.software_cd.addItem('3DsMax')
        self.software_cd.addItem('Houdini')

        self.template_path_lb = QtWidgets.QLabel('')
        self.choose_template_path_btn = QtWidgets.QPushButton('open')

        self.categoty_cd = QtWidgets.QComboBox()
        self.categoty_cd.addItem('Modeling')
        self.categoty_cd.addItem('Rig')
        self.categoty_cd.addItem('lighting')
        self.categoty_cd.addItem('Animation')


        self.save_btn = QtWidgets.QPushButton('Save')
        self.cancel_btn = QtWidgets.QPushButton('Cancel')
    def create_layout(self):
        
        template_path_layout = QtWidgets.QHBoxLayout()
        template_path_layout.addWidget(self.template_path_lb)
        template_path_layout.addStretch()
        template_path_layout.addWidget(self.choose_template_path_btn)



        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('Code:', self.template_code_le)
        form_layout.addRow('name', self.template_name_le)
        form_layout.addRow('software', self.software_cd)
        form_layout.addRow('template: ', template_path_layout)
        form_layout.addRow('category: ', self.categoty_cd)


        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.save_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)


    def create_conections(self):
        self.cancel_btn.clicked.connect(self.close)
        self.choose_template_path_btn.clicked.connect(self.choose_template_btn_pressed)

        self.save_btn.clicked.connect(self.save_btn_pressed)

    def choose_template_btn_pressed(self):
        path = self.open_file_dialog()
        self.template_path_lb.setText(path)

    def save_btn_pressed(self):
        if self.template_code_le.text() and self.template_name_le.text() and self.template_path_lb.text():
            self.sc.add_template(self.template_code_le.text(), self.template_name_le.text(), 
                                    self.software_cd.currentText(), self.categoty_cd.currentText(), 
                                    self.template_path_lb.text())
            self.close()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Not all sections are filled")
            msg.setWindowTitle("Error")
            msg.exec()
        
    
    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptOpen)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            # print("Selected File:", selected_files[0])
            return selected_files[0]