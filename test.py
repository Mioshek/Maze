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
        
PathPoint.set_goal(Point(20,20))
        
s = {PathPoint(1,1,PathPoint(20,20,None))}
print(s)
if PathPoint(1,1,PathPoint(20,20,None)) in s:
    print("cos")
    
if not PathPoint(1,2,PathPoint(20,20,None)) in s:
    print("not in")

if PathPoint(1,1,PathPoint(20,21,None)) in s:
    print("cos origin")


for i in range(0,32000):
    for j in range(0,32000):
        new_hash = PathPoint(i,j, PathPoint(i,j,None))
        if new_hash in s:
            print(i,j)
            print("collision: ",new_hash)
        else:
            s.add(new_hash)
# print(s)
