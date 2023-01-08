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
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtCore import Qt, QEvent
from settings_window import settings, get_primary_screen_name, screens


class MainMindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fields_x = settings["width"]
        self.fields_y = settings["height"]
        self.left_mouse_button_toogle = False
        self.setWindowTitle("Maze")
        self.buttons = [[Button(x,y,self) for x in range(self.fields_x)] for y in range(self.fields_y)]
        self.setupButtons()
        
        
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            #handle the left-button press in here
            # self.label.setText("mousePressEvent LEFT")
            pass

        elif e.button() == Qt.MouseButton.MiddleButton:
            #handle the middle-button press in here.
            # self.label.setText("mousePressEvent MIDDLE")
            pass

        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here.
            if self.left_mouse_button_toogle == False:
                self.left_mouse_button_toogle = True
            else: 
                self.left_mouse_button_toogle = False
    
    def eventFilter(self, obj, event):
        print(event.type())
        sender = obj
        if event.type() == QEvent.Type.HoverEnter and self.left_mouse_button_toogle:
            if sender.styleSheet() == 'QPushButton {background-color: #00ff2f}': sender.setStyleSheet('QPushButton {background-color: #ffffff}')
            else: sender.setStyleSheet('QPushButton {background-color: #00ff2f}')
        sender.nextCheckState()
        return super().eventFilter(obj, event)
            
    def setupButtons(self):
        for x in range(self.fields_x):
            for y in range(self.fields_y):
                self.buttons[y][x].clicked.connect(self.buttons[y][x].button_clicked)
                self.buttons[y][x].installEventFilter(self)



class Button(QPushButton):
    def __init__(self, posX, posY, parent):
        super(Button, self).__init__(parent)
        self.posX = posX
        self.posY = posY
        self.parent = parent
        self.setStyleSheet('QPushButton {background-color: #ffffff}')
        self.screen_name = get_primary_screen_name()
        self.button_size = 0
        if parent.fields_x < parent.fields_y:
            self.button_size = (screens[self.screen_name]["height"] -20)/parent.fields_y
        else:  
            self.button_size = (screens[self.screen_name]["width"] -60)/parent.fields_x
            temp_check_but_size = (screens[self.screen_name]["height"] -20)/parent.fields_y
            if self.button_size > temp_check_but_size:
                self.button_size = temp_check_but_size
        self.init(posX,posY,self.button_size)
        
    def init(self, x, y, s):
        self.setGeometry(4+x*s,10+y*s, s, s)
        
    def button_clicked(self):
        print(self.styleSheet())
        if self.styleSheet() == 'QPushButton {background-color: #00ff2f}': self.setStyleSheet('QPushButton {background-color: #ffffff}')
        else: self.setStyleSheet('QPushButton {background-color: #00ff2f}')
            

def run_main_gui():
    app = QApplication(sys.argv)
    window = MainMindow()
    window.show()
    sys.exit(app.exec())