# A program which uses recursive backtracking to generate a maze
import random
from enum import Enum
from time import sleep
import threading
import numpy as np
import sys
import astar_logic

sys.setrecursionlimit(8000)

{0:"#28262c",
        1: "#e1eff6",
        2:"#19297C",
        3:"#D72638",
        4:"#248232",
        5:"#ffba08",
        }
class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    
class Cell:
    VISITED = -1
    WALL = 0
    WALKABLE = 1
    START = 2
    END = 3

  
class Backtracking:

    def __init__(self, height, width, buttons):

        self.width = width
        self.height = height
        self.buttons = buttons

    
    def createMaze(self):
        maze = np.ones((self.height +2, self.width +2), dtype=np.int)

        for row in range(self.height + 2):
            for col in range(self.width +2):
                if row % 2 == 1 or col % 2 == 1:
                    maze[row, col] = Cell.WALL
                if row == 0 or col == 0 or row == self.height +1 or col == self.width +1:
                    maze[row, col] = Cell.VISITED

        sx = random.choice(range(2, self.width -2, 2))
        sy = random.choice(range(2, self.height -2, 2))

        self.generator(sy, sx, maze)

        for row in range(1,self.height +1):
            for col in range(1,self.width +1):
                if maze[row, col] == Cell.VISITED:
                    maze[row, col] = Cell.WALKABLE
                    self.buttons[row-1][col-1].setStyleSheet('QPushButton {background-color: #e1eff6}')
    
        start_y, start_x = self.generate_endpoints(maze)
        end_y, end_x = self.generate_endpoints(maze)
        while start_x == end_x and start_y == end_y:
            start_y, start_x = self.generate_endpoints(maze)
            end_y, end_x = self.generate_endpoints(maze)
            
        self.buttons[start_y-1][start_x-1].setStyleSheet('QPushButton {background-color: #19297C}')
        self.buttons[end_y-1][end_x-1].setStyleSheet('QPushButton {background-color: #D72638}')
        maze[start_y,start_x] = Cell.START
        maze[end_y,end_x] = Cell.END
        astar_logic.PathPoint.set_goal(astar_logic.Point(end_y,end_x))
        a = astar_logic.Astar((start_y,start_x),(end_y,end_x),maze, self.buttons)
        last_point = a.find_path()

        point:astar_logic.PathPoint = last_point
        while point != None:
            self.buttons[point.row-1,point.col-1].setStyleSheet('QPushButton {background-color: #5AFF15}')
            point = point.origin
            sleep(0.01)
            
        
    def generate_endpoints(self, maze):
        x = random.choice(range(1, self.width))
        y = random.choice(range(1, self.height))
        while maze[y, x] == Cell.WALL:
            x = random.choice(range(1, self.width))
            y = random.choice(range(1, self.height)) 
        return y, x
    
    def generator(self, curr_y, curr_x, grid):
        grid[curr_y, curr_x] = Cell.VISITED
        self.buttons[curr_y-1][curr_x-1].setStyleSheet('QPushButton {background-color: "#65a86f"}')
        
        if grid[curr_y - 2, curr_x] == Cell.VISITED and grid[curr_y + 2, curr_x] == Cell.VISITED and grid[curr_y, curr_x - 2] == Cell.VISITED and grid[curr_y, curr_x + 2] == Cell.VISITED:
            pass
        else:
            li = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                if dir == Direction.LEFT:
                    new_x = curr_x - 2
                    mx = curr_x - 1
                elif dir == Direction.RIGHT:
                    new_x = curr_x + 2
                    mx = curr_x + 1
                else:
                    new_x = curr_x
                    mx = curr_x

                if dir == Direction.UP:
                    new_y = curr_y - 2
                    my = curr_y - 1
                elif dir == Direction.DOWN:
                    new_y = curr_y + 2
                    my = curr_y + 1
                else:
                    new_y = curr_y
                    my = curr_y
                    
                sleep(0.001)
                if grid[new_y, new_x] != Cell.VISITED:
                    grid[my, mx] = Cell.VISITED
                    self.buttons[my-1][mx-1].setStyleSheet('QPushButton {background-color: "#65a86f"}')

                    self.generator(new_y, new_x, grid)
                    