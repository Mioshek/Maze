#imports
import sys
#from imports
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QSlider,
)
from PyQt6.QtCore import Qt
from screeninfo import get_monitors

settings = {
    "width":4,
    "height":4,
    "autogenerate":True,
}

#get screen info
screens = {}
for m in get_monitors():
    screens["{name}".format(name=m.name)]={"x":m.x,
                                          "y":m.y,
                                          "height":m.height,
                                          "width":m.width,
                                          "is_primary":m.is_primary,}
    
def get_primary_screen_name() -> str:
    for screen_name in screens.keys():
        if screens[screen_name]["is_primary"]:
            return screen_name


class AutogenerateButton(QWidget):
    def __init__(self):
        super().__init__()
        self.primary_screen_name = get_primary_screen_name()
        self.x = screens[self.primary_screen_name]["width"]/3
        self.y = screens[self.primary_screen_name]["height"]/6
        self.resize(self.x, self.y)
        self.setWindowTitle("Set Autogenerate")
        self.button_is_checked = True
        
        self.button = QPushButton("True",self)
        self.button.setGeometry(self.x/5,self.x/10, self.x/2, self.x/12)# <1>
        self.button.setCheckable(True)
        self.button.released.connect(
            self.the_button_was_released
        )  # <2>
        self.button.setChecked(self.button_is_checked)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()  # <3>
        self.button.setText(str(self.button_is_checked))
        settings["autogenerate"] = str(self.button_is_checked)
    

class SetSizeWidgets(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.primary_screen_name = get_primary_screen_name()
        self.x = screens[self.primary_screen_name]["width"]/3
        self.y = screens[self.primary_screen_name]["height"]/6
        self.resize(self.x, self.y)
        self.setWindowTitle("Set Maze {name}".format(name=self.name))
        
        self.label = QLabel(self)
        self.label.move(self.x/2, self.y/3)
 
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setGeometry(self.x/10,self.x/15, self.x/1.2, self.x/6)
        slider.setMinimum(5)
        if self.name == "Width":
            slider.setMaximum(199)
        else: slider.setMaximum(99)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setSingleStep(2)
        slider.setTickInterval(2)
        slider.valueChanged.connect(self.display)
           
     
    def display(self):
        self.label.setText("{name}: ".format(name=self.name) +str(self.sender().value()))
        if self.windowTitle() == "Set Maze Width":
            settings["width"] = self.sender().value()
        else: settings["height"] = self.sender().value()
        self.label.adjustSize()
 
 
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Set Maze Size")
        self.primary_screen_name = get_primary_screen_name()
        self.x = screens[self.primary_screen_name]["width"]/3
        self.y = screens[self.primary_screen_name]["height"]/6
        self.resize(self.x, self.y)
        
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.TabPosition.South)
        tabs.setMovable(True)
        for i, name in enumerate(["Width", "Height",]):
            tabs.addTab(SetSizeWidgets(name), name)
            
        tabs.addTab(AutogenerateButton(), "Autogenerate Maze")
        tabs.addTab(NextWindow(self.app),"Submit")
        self.setCentralWidget(tabs)

          # Expands label size as numbers get larger
          

class NextWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Submit")
        self.primary_screen_name = get_primary_screen_name()
        self.x = screens[self.primary_screen_name]["width"]/3
        self.y = screens[self.primary_screen_name]["height"]/6
        
        self.button = QPushButton("Submit",self)
        self.button.setGeometry(self.x/5,self.x/10, self.x/2, self.x/12)#
        self.button.clicked.connect(self.exit)
        
    def exit(self):
        self.app.quit()

def run_settings_window(): 
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()

