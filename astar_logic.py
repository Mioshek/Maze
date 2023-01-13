
class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

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
    def __init__(self, startpoint, endpoint, maze) -> None:
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.current_point = startpoint
        self.closed = []
        self.available = []
        self.maze = maze
    
        
    def find_next_point(self):
        upwards_row, upwards_col = self.current_point.row -1,  self.current_point.col
        downwards_row, downwards_col = self.current_point.row -1,  self.current_point.col
        leftwards_row, leftwards_col = self.current_point.row -1,  self.current_point.col
        rightwards_row, rightwards_col = self.current_point.row -1,  self.current_point.col
        
        if self.is_inside_maze(rightwards_row, rightwards_col):
            pp = PathPoint(rightwards_row, rightwards_col, self.current_point)
            pass
        if self.is_inside_maze(leftwards_row, leftwards_col):
            pp = PathPoint(leftwards_row, leftwards_col, self.current_point)
            pass
        if self.is_inside_maze(upwards_row, upwards_col):
            pp = PathPoint(upwards_row, upwards_col, self.current_point)
            pass
        if self.is_inside_maze(downwards_row, downwards_col):
            pp = PathPoint(downwards_row, downwards_col, self.current_point)
            pass
    
    def is_inside_maze(self, row, col):
        if row > 0 and row < len(self.maze) and col > 0 and col < len(self.maze[0]):
            return True
        
    def find_path(self):
        while not self.current_point.equals(self.endpoint):
            current_point = self.find_next_point()
            self.closed.append(current_point)
            self.available.remove(current_point)
    
    
# def main():
#     END = Point(1,2)
#     PathPoint.set_goal(END)
#     a = PathPoint(10, 8, None)
#     b = PathPoint(9, 9, a)
#     c = PathPoint(7, 9, b)
    
#     print(b.path_distance())
#     print(c.path_distance())

# main()