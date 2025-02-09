import sys
import Logic
import CustomDialogs
from PySide6 import QtCore, QtGui, QtWidgets

class TemplateWidget(QtWidgets.QWidget):
    def __init__(self, code, name, software, category):
        super().__init__()
        self.code = code
        self.name = name
        self.software = software
        self.category = category

        match category:
            case 'Rig':
                color = 'brown'
            case 'Lighting':
                color = 'orange'
            case 'Modeling':
                color = 'blue'
            case 'Animation':
                color = 'green'
        match self.software:
            case 'Maya':
                self.image_path = './src/maya.png'
            case 'Blender':
                self.image_path = './src/blender.png'
            case _:
                self.image_path = ''

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


        self.creat_widget()
        self.create_layout()
        self.create_connection()

    
    def creat_widget(self):
        self.software_lb = QtWidgets.QLabel(self.software)
        self.template_lb = QtWidgets.QLabel(self.name)
        self.category_lb = QtWidgets.QLabel(self.category)

        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.software_lb.setFont(font)
        self.template_lb.setFont(font)
        self.category_lb.setFont(font)

        self.image_lb = QtWidgets.QLabel()
        pixmp = QtGui.QPixmap(self.image_path)
        pixmp = pixmp.scaled(100, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.image_lb.setPixmap(pixmp)
        self.image_lb.setScaledContents(True)

        self.creat_btn = QtWidgets.QPushButton('Use')
        self.customize_btn = QtWidgets.QPushButton('customize')

        
    def create_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.creat_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.customize_btn)

        info_layout = QtWidgets.QFormLayout()
        info_layout.addRow('Name: ', self.template_lb)
        info_layout.addRow('Category: ', self.category_lb)
        info_layout.addRow('Software: ' ,self.software_lb)
 
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addLayout(info_layout)
        title_layout.addStretch()
        title_layout.addWidget(self.image_lb)
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def create_connection(self):
        self.creat_btn.clicked.connect(self.use_button_pressed)


    def use_button_pressed(self):
        window = CustomDialogs.UseWindow(scene_setup, self.code, self)
        window.show()
        window.exec()
    




class TemplateLibraryMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(TemplateLibraryMainWindow,self).__init__(parent=None)
        self.setWindowTitle('Templates')
        self.setMinimumSize(500, 700)

        self.sc = Logic.SceneSetup()
        global scene_setup 
        scene_setup = self.sc
        self.templates = self.sc.templates

        self.create_widgets()
        self.create_layout()
        self.create_connection()
        
    def create_widgets(self):

        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        self.boxes = []
        templates = scene_setup.search_in_templates('')
        for item in templates:
            bx = TemplateWidget(item, self.templates[item]['name'], self.templates[item]['software'], 
                                self.templates[item]['category'])
            self.boxes.append(bx)
        
        self.search_le = QtWidgets.QLineEdit()
        self.template_group_box = QtWidgets.QGroupBox()
        self.template_group_box.setContentsMargins(5,5,5,5)
        
        self.add_new_btn = QtWidgets.QPushButton('add new')
        
    def create_layout(self):
        
        self.templates_form_layout = QtWidgets.QFormLayout()
        for box in self.boxes:
            self.templates_form_layout.addWidget(box)

        self.template_group_box.setLayout(self.templates_form_layout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.template_group_box)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.search_le)
        main_layout.addWidget(scroll)
        main_layout.addWidget(self.add_new_btn)
        
        self.main_widget.setLayout(main_layout)
        
    def create_connection(self):
        self.add_new_btn.clicked.connect(self.on_add_new_pressed)
        self.search_le.textChanged.connect(self.search_le_changed)

    def search_le_changed(self):
        self.update_template_list(self.search_le.text())

    def update_template_list(self, str=''):
        templates = scene_setup.search_in_templates(str)
        #print(templates)

    def on_add_new_pressed(self):
        new_window = CustomDialogs.AddNewTemplateWindow(self, scene_setup)
        new_window.exec()
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('windows'))

    window = TemplateLibraryMainWindow()
    window.show()
    app.exec()