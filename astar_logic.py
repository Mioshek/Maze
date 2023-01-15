import numpy as np
from time import sleep


class Cell:
    BORDER = -1
    WALL = 0
    WALKABLE = 1
    START = 2
    END = 3
    FRISK = 4


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
    def __key(self):
        return (self.row, self.col)
        
    def __hash__(self) -> int:
        return hash((self.row, self.col))
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.__key() == other.__key()
        return NotImplemented

class PathPoint(Point):
    END: Point
    
    def __init__(self, row, col, origin) -> None:
        super().__init__(row, col)
        self.g_cost: int = 0 #distance from start
        self.h_cost: int = 0 #distance from end
        self.f_cost: int = 0 #sum
        self.origin: PathPoint = origin
        self.calculate_costs()
        
    @staticmethod    
    def distance(row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2)
    
    def path_distance(self):
        nodes:int = 0
        point:PathPoint = self
        while point != None:
            point = point.origin
            nodes +=1
        print("nodes",nodes)
        return 0 if nodes == 0 else nodes-1

    
    def calculate_costs(self):
        self.g_cost:int = self.path_distance()
        self.h_cost:int = self.distance(self.row, self.col, PathPoint.END.row, PathPoint.END.col)
        self.f_cost:int = self.g_cost + self.h_cost
        
    @staticmethod
    def set_goal(point):
        PathPoint.END = point
    
    def equals(self, pathpoint):
        return self.row == pathpoint.row and self.col == pathpoint.col
          
            
class Astar:
    def __init__(self, startlocation, endlocation, maze, buttons) -> None:
        self.startpoint:PathPoint = PathPoint(startlocation[0],startlocation[1], None)
        self.endpoint:PathPoint = PathPoint(endlocation[0],endlocation[1], None)
        self.current_point:PathPoint = self.startpoint
        self.closed:set[PathPoint] = {self.startpoint}
        self.available:set[PathPoint] = set()
        self.maze = maze
        self.buttons = buttons
    
    def check_if_wall(self,row,col):
        # height, width = self.maze.shape
        # if row > height-1 or col > width-1:
        #     return True
        if self.maze[row, col] == Cell.WALL or self.maze[row,col] == Cell.BORDER:
            return True
        
    def find_next_point(self):
        
        upwards_row, upwards_col = self.current_point.row -1,  self.current_point.col
        downwards_row, downwards_col = self.current_point.row +1,  self.current_point.col
        leftwards_row, leftwards_col = self.current_point.row,  self.current_point.col -1
        rightwards_row, rightwards_col = self.current_point.row,  self.current_point.col +1
        sleep(0.005)
        self.buttons[self.current_point.row-1, self.current_point.col-1].setStyleSheet('QPushButton {background-color: #ffba08}')
        if self.is_inside_maze(rightwards_row, rightwards_col) and not self.check_if_wall(rightwards_row, rightwards_col):
            pp = PathPoint(rightwards_row, rightwards_col, self.current_point)
            self.process_neighbour(pp,self.current_point)
        if self.is_inside_maze(leftwards_row, leftwards_col) and not self.check_if_wall(leftwards_row, leftwards_col):
            pp = PathPoint(leftwards_row, leftwards_col, self.current_point)
            self.process_neighbour(pp,self.current_point)
        if self.is_inside_maze(upwards_row, upwards_col) and not self.check_if_wall(upwards_row, upwards_col):
            pp = PathPoint(upwards_row, upwards_col, self.current_point)
            self.process_neighbour(pp,self.current_point)
        if self.is_inside_maze(downwards_row, downwards_col) and not self.check_if_wall(downwards_row, downwards_col):
            pp = PathPoint(downwards_row, downwards_col, self.current_point)
            self.process_neighbour(pp,self.current_point)
        
        if len(self.available) == 0:
            raise Exception("No available nodes to proceed")
        minimum:int = 100_000
        minimum_pathpoint:PathPoint
        for item in self.available: #todo
            if item.f_cost < minimum:
                minimum = item.f_cost
                minimum_pathpoint = item
        
        return minimum_pathpoint
            
    
    def is_inside_maze(self, row, col):
        if row > 0 and row < len(self.maze) and col > 0 and col < len(self.maze[0]):
            return True
        
    def find_path(self):
        while not self.current_point.equals(self.endpoint):
            self.current_point = self.find_next_point()
            self.maze[self.current_point.row,self.current_point.col] = Cell.FRISK 
            print(self.maze)
            self.closed.add(self.current_point) #todo
            self.available.remove(self.current_point) #todo
        return self.current_point
            
    def process_neighbour(self, neighbour, current):
        if neighbour in self.closed: #todo
            return
        if neighbour in self.available: #todo!
            previous:PathPoint #todo!
            for item in self.available:
                if item.row == neighbour.row and item.col == neighbour.col:
                    previous = item
            current_distance = current.path_distance() + 1
            if previous.path_distance() > current_distance:
                previous.origin = current
                previous.calculate_costs()
        else:
            self.available.add(neighbour) #todo
            print("added new node")
            