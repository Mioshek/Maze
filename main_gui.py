import sys
import numpy as np
import random
from threading import Thread
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
from PyQt6 import QtCore
from settings_window import settings, get_primary_screen_name, screens
from logic import Backtracking
from time import sleep

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
        self.cols = settings["width"]
        self.rows = settings["height"]
        if self.cols % 2 == 0:
            self.cols += 1
        if self.rows % 2 == 0:
            self.rows += 1
        self.left_mouse_button_toogle = False
        self.setWindowTitle("Maze")
        self.buttons = np.empty([self.rows, self.cols], dtype=Button)
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row, col] =  Button(row,col,self)
        self.setupButtons()
        
    def focusOutEvent(self, e):
        print(e)
        
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
        if e.key() == 16777220: #enter
            fields_size = len(fields)
            c.current_col_index +=1
            if c.current_col_index == fields_size:
                c.current_col_index = 0
            c.bg_color = fields[c.current_col_index]
        print(e.key())
        if e.key() == 16777248: 
            bc = Backtracking(self.rows, self.cols, self.buttons)
            t1 = Thread(target=bc.createMaze)
            t1.start()

            
    def eventFilter(self, obj, event):
        sender = obj
        if event.type() == QEvent.Type.HoverEnter and self.left_mouse_button_toogle:
            sender.setStyleSheet('QPushButton {background-color: ' + c.bg_color + '}')
        sender.nextCheckState()
        return super().eventFilter(obj, event)
            
    def setupButtons(self):
        for c in range(self.cols):
            for r in range(self.rows):
                self.buttons[r,c].clicked.connect(self.buttons[r,c].button_clicked)
                self.buttons[r][c].installEventFilter(self)
                # self.buttons[r][c].


class Button(QPushButton):
    def __init__(self, row, col, parent):
        super(Button, self).__init__(parent)
        self.col = col
        self.row = row
        self.parent = parent
        if settings["autogenerate"] == True: self.set_color_if_auto(self.row, self.col)
        else: self.setStyleSheet('QPushButton {background-color: #e1eff6}')
        self.screen_name = get_primary_screen_name()
        self.button_size = 0
        if parent.cols < parent.rows:
            self.button_size = (screens[self.screen_name]["height"] -100)/parent.rows
        else:  
            self.button_size = (screens[self.screen_name]["width"] -100)/parent.cols
            temp_check_but_size = (screens[self.screen_name]["height"] -100)/parent.rows
            if self.button_size > temp_check_but_size:
                self.button_size = temp_check_but_size
        self.setGeometry(col*self.button_size,row*self.button_size, self.button_size, self.button_size)
        
        
    def button_clicked(self):
        self.setStyleSheet('QPushButton {background-color: ' + c.bg_color + '}')

    def set_color_if_auto(self, row, col):
        if row%2 == 0 or col%2 == 0: self.setStyleSheet('QPushButton {background-color: #832232}')
        else: self.setStyleSheet('QPushButton {background-color: #e1eff6}')
    
            
def run_main_gui():
    app = QApplication(sys.argv)
    window = MainMindow()
    window.show()
    sys.exit(app.exec())