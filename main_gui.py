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
from PyQt6.QtGui import QMouseEvent, QKeyEvent
from PyQt6.QtCore import Qt, QEvent
from settings_window import settings, get_primary_screen_name, screens

fields = {0:"#832232",
        1: "#e1eff6",
        2:"#8884ff",
        3:"#f679e5",
        4:"#248232",
        5:"#ffba08",
        }
class Color:
    def __init__(self):
        self.bg_color = fields[0]
        self.current_col_index = 0


c = Color()

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
        if e.button() == Qt.MouseButton.LeftButton: pass
        elif e.button() == Qt.MouseButton.MiddleButton: pass
        elif e.type() == QEvent.Type.MouseButtonDblClick: pass
        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here.
            if self.left_mouse_button_toogle == False:
                self.left_mouse_button_toogle = True
            else: 
                self.left_mouse_button_toogle = False
    
    def keyPressEvent(self, e):
        if e.key() == 16777220:
            fields_size = len(fields)
            c.current_col_index +=1
            if c.current_col_index == fields_size:
                c.current_col_index = 0
            c.bg_color = fields[c.current_col_index]
            
    def eventFilter(self, obj, event):
        sender = obj
        if event.type() == QEvent.Type.HoverEnter and self.left_mouse_button_toogle:
            sender.setStyleSheet('QPushButton {background-color: ' + c.bg_color + '}')
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
        self.setStyleSheet('QPushButton {background-color: #e1eff6}')
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
        self.setStyleSheet('QPushButton {background-color: ' + c.bg_color + '}')

            
def run_main_gui():
    app = QApplication(sys.argv)
    window = MainMindow()
    window.show()
    sys.exit(app.exec())