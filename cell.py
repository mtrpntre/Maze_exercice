from graphic import *
import time

class Square_Cell:
    def __init__(self,win, x, y, width, u=True, d=True, l=True, r=True):
        self.__win = win
        self._x = x
        self._y = y
        self.up_left_corner = Point(x,y)
        self.down_left_corner = Point(x, y + width)
        self.up_right_corner = Point(x + width, y)
        self.down_right_corner = Point(x + width, y + width)
        self.visited = False
        self.walls = [u, r, d, l]

    def draw(self,  color="black", width=2):
        if self.__win is None:
            return
        if self.walls[0]:
            line = Line(self.up_left_corner, self.up_right_corner)
            self.__win.draw_line(line, color, width)
        if self.walls[1]:
            line = Line(self.up_right_corner, self.down_right_corner)
            self.__win.draw_line(line, color, width)
        if self.walls[2]:
            line = Line(self.down_right_corner, self.down_left_corner)
            self.__win.draw_line(line, color, width)
        if self.walls[3]:
            line = Line(self.down_left_corner, self.up_left_corner)
            self.__win.draw_line(line, color, width)
        
    
    def draw_move(self, to_cell, undo=False):
        x_mid = (self.up_left_corner.x + self.up_right_corner.x) / 2
        y_mid = (self.up_left_corner.y + self.down_left_corner.y) / 2
        center = Point(x_mid, y_mid)

        to_x_mid = (to_cell.up_left_corner.x + to_cell.up_right_corner.x) / 2
        to_y_mid = (to_cell.up_left_corner.y + to_cell.down_left_corner.y) / 2
        to_center = Point(to_x_mid, to_y_mid)

        line_color = "red"
        if undo:
            line_color = "gray"
        
        line = Line(center, to_center)
        self.__win.draw_line(line, line_color, 5)

class Maze:

    def __init__(
            self,
            x1,
            y1,
            number_of_rows,
            number_of_columns,
            cell_size,
            win
        ):
        self.__x1 = x1
        self.__y1 = y1
        self.__number_of_rows = number_of_rows
        self.__number_of_columns = number_of_columns
        self.__cell_size = cell_size
        self.__height = number_of_rows * cell_size
        self.__width = number_of_columns * cell_size
        self.__win = win
        self.__cells = []
        self.__stack = []
        self.__current = None
        self.__start = None
        self.__end = None
        self._create_cells()

    def _create_cells(self):
        if self.__win is None:
            return
        if self.__number_of_columns < 1 or self.__number_of_rows < 1:
            return
        if self.__y1 > self.__height or self.__x1 > self.__width:
            return
        y = self.__y1
            
        while y < self.__height:
            x = self.__x1
            row = []
            while x < self.__width:
                cell = Square_Cell(self.__win, x, y, self.__cell_size)
                row.append(cell)
                x += self.__cell_size
            self.__cells.append(row)
            y += self.__cell_size
            
        for i in range(len(self.__cells)):
            for j in range(len(self.__cells[i])):
                self.draw_cell(i, j)
            
    def draw_cell(self, i, j):
        self.__cells[i][j].draw()
        self.animate()
            
            
    def animate(self):
        self.__win.redraw()
        time.sleep(0.05)


