from Tkinter import *


class GridCanvas:
    UNIT = 50
    
    def __init__(self, grid):
        master = Tk()
        w, h = (len(grid[0])+1)*GridCanvas.UNIT, (len(grid)+1)*GridCanvas.UNIT
        self.c = Canvas(master, width=w, height=h)
        self.c.pack()
        
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] == 1:
                    self.circle(x, y, 0.5)
    
    def show_interest_point(self, point):
        self.circle(point[0], point[1], 0.1, "blue")
    
    def show_path(self, path, color="blue"):
        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            self.line(x1, y1, x2, y2, color)
    
    def map(self, x, y):
        return (y+1)*GridCanvas.UNIT, (x+1)*GridCanvas.UNIT
    
    def line(self, x1, y1, x2, y2, color):
        x1, y1 = self.map(x1, y1)
        x2, y2 = self.map(x2, y2)
        self.c.create_line(x1, y1, x2, y2, fill=color)
    
    def circle(self, x, y, r, color="red"):
        x, y = self.map(x, y)
        r = r * GridCanvas.UNIT
        x0, y0 = x-r, y-r
        x1, y1 = x+r, y+r
        self.c.create_oval(x0, y0, x1, y1, fill=color)
    
    def display(self):
        mainloop()
