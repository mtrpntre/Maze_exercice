from graphic import *
import time
import random

class Square_Cell:
    def __init__(self, win, x, y, width, u=True, d=True, l=True, r=True):
        self.__win = win
        self._x = x
        self._y = y
        self.up_left_corner = Point(x,y)
        self.down_left_corner = Point(x, y + width)
        self.up_right_corner = Point(x + width, y)
        self.down_right_corner = Point(x + width, y + width)
        self.visited = False
        self.walls = [u, r, d, l]
        self.neighbours = {"up":False, "right":False, "down":False, "left":False}

    def draw(self,  color="black", width=2):
        if self.__win is None:
            return
        if self.walls[0]:
            line = Line(self.up_left_corner, self.up_right_corner)
            self.__win.draw_line(line, color, width)
        else:
            line = Line(self.up_left_corner, self.up_right_corner)
            self.__win.draw_line(line, "white", width)

        if self.walls[1]:
            line = Line(self.up_right_corner, self.down_right_corner)
            self.__win.draw_line(line, color, width)
        else:
            line = Line(self.up_right_corner, self.down_right_corner)
            self.__win.draw_line(line, "white", width)

        if self.walls[2]:
            line = Line(self.down_right_corner, self.down_left_corner)
            self.__win.draw_line(line, color, width)
        else:
            line = Line(self.down_right_corner, self.down_left_corner)
            self.__win.draw_line(line, "white", width)

        if self.walls[3]:
            line = Line(self.down_left_corner, self.up_left_corner)
            self.__win.draw_line(line, color, width)
        else:
            line = Line(self.down_left_corner, self.up_left_corner)
            self.__win.draw_line(line, "white", width)
        
    
    def draw_move(self, to_cell, undo=False):
        x_mid = (self.up_left_corner.x + self.up_right_corner.x) / 2
        y_mid = (self.up_left_corner.y + self.down_left_corner.y) / 2
        center = Point(x_mid, y_mid)

        to_x_mid = (to_cell.up_left_corner.x + to_cell.up_right_corner.x) / 2
        to_y_mid = (to_cell.up_left_corner.y + to_cell.down_left_corner.y) / 2
        to_center = Point(to_x_mid, to_y_mid)

        line_color = "red"
        if undo:
            line_color = "blue"
        
        line = Line(center, to_center)
        self.__win.draw_line(line, line_color, 5)

class Maze:

    def __init__(
            self,
            win,
            x1,
            y1,
            number_of_rows,
            number_of_columns,
            cell_size,
            seed=None
            
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
        self.__start = None
        self.__end = None
        self.__moves = []
        if seed:
            random.seed(seed)
        
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
        
        
        self.entrance_and_exit()
        self.break_walls(0,0)
        self.reset_cells_visited()
            
    def draw_cell(self, i, j):
        self.__cells[i][j].draw()
        self.animate()
            
            
    def animate(self):
        self.__win.redraw()
        time.sleep(0.01)
    
    def entrance_and_exit(self):
        self.__start = self.__cells[0][0]
        self.__end = self.__cells[-1][-1]
        self.__start.walls[3] = False
        self.__end.walls[1] = False
        self.draw_cell(0,0)
        self.draw_cell(-1,-1)
        
    
    def get_directions(self, i, j):
        if self.__number_of_columns < 1 or self.__number_of_rows < 0:
            return
        if i == 0:
            self.__cells[i][j].neighbours["down"]=True
        elif i == (self.__number_of_rows - 1):
            self.__cells[i][j].neighbours["up"]=True
        else:
            self.__cells[i][j].neighbours["down"]=True
            self.__cells[i][j].neighbours["up"]=True
            
        
        if j == 0:
            self.__cells[i][j].neighbours["right"]=True
        elif j == (self.__number_of_columns - 1):
            self.__cells[i][j].neighbours["left"]=True
        else:
            self.__cells[i][j].neighbours["right"]=True
            self.__cells[i][j].neighbours["left"]=True

        true_directions = [key for key, value in self.__cells[i][j].neighbours.items() if value]

        return true_directions
    
    def break_walls(self, i, j):
        
        current = self.__cells[i][j]
        current.visited = True
        true_directions = self.get_directions(i,j)
        random.shuffle(true_directions)
        for direction in true_directions:
            if direction == "up":
                if not self.__cells[i-1][j].visited:
                    current.walls[0] = False
                    self.__cells[i-1][j].walls[2] = False
                    self.draw_cell(i,j)
                    self.draw_cell(i-1,j)
                    self.break_walls(i-1, j)
            elif direction == "down":
                if not self.__cells[i+1][j].visited:
                    current.walls[2] = False
                    self.__cells[i+1][j].walls[0] = False
                    self.draw_cell(i,j)
                    self.draw_cell(i+1,j)
                    self.break_walls(i+1, j)
            elif direction == "left":
                if not self.__cells[i][j-1].visited:
                    current.walls[3] = False
                    self.__cells[i][j-1].walls[1] = False
                    self.draw_cell(i,j)
                    self.draw_cell(i,j-1)
                    self.break_walls(i, j-1)
            elif direction == "right":
                if not self.__cells[i][j+1].visited:
                    current.walls[1] = False
                    self.__cells[i][j+1].walls[3] = False
                    self.draw_cell(i,j)
                    self.draw_cell(i,j+1)
                    self.break_walls(i, j+1)
            else:
                return

    def reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def solve(self, i, j):
        current = self.__cells[i][j]
        current.visited = True
        if current == self.__end:
            return True
        
        rows, cols = len(self.__cells), len(self.__cells[0])
        true_directions = self.get_directions(i,j)
        up_cell = self.__cells[i-1][j] if i > 0 else None
        down_cell = self.__cells[i+1][j] if i < rows - 1 else None
        left_cell = self.__cells[i][j-1] if j > 0 else None
        right_cell = self.__cells[i][j+1] if j < cols - 1 else None
        
        if "up" in true_directions and current.walls[0] == False and not up_cell.visited:
            self.__moves.append("up")
            current.draw_move(up_cell)
            self.animate()
            if self.solve(i-1, j):
                return True
        elif "right" in true_directions and current.walls[1] == False and not right_cell.visited:
            self.__moves.append("right")
            current.draw_move(right_cell)
            self.animate()
            if self.solve(i, j+1):
                return True
        elif "down" in true_directions and current.walls[2] == False and not down_cell.visited:
            self.__moves.append("down")
            current.draw_move(down_cell)
            self.animate()
            if self.solve(i+1, j):
                return True
        elif "left" in true_directions and current.walls[3] == False and not left_cell.visited:
            self.__moves.append("left")
            current.draw_move(left_cell)
            self.animate()
            if self.solve(i, j-1):
                return True
            

        elif self.__moves[-1] == "up" and down_cell:
            self.__moves.pop()
            current.draw_move(down_cell, True)
            self.animate()
            self.solve(i+1, j)
        elif self.__moves[-1] == "right" and left_cell:
            self.__moves.pop()
            current.draw_move(left_cell, True)
            self.animate()
            self.solve(i, j-1)
        elif self.__moves[-1] == "down" and up_cell:
            self.__moves.pop()
            current.draw_move(up_cell, True)
            self.animate()
            self.solve(i-1, j)
        elif self.__moves[-1] == "left" and right_cell:
            self.__moves.pop()
            current.draw_move(right_cell, True)
            self.animate()
            self.solve(i, j+1)
            
        else:
            return False

    def solve_bot(self, i, j):
        current = self.__cells[i][j]
        current.visited = True
        possible_directions = self.get_directions(i, j)
        rows, cols = len(self.__cells), len(self.__cells[0])
        up_cell = self.__cells[i-1][j] if i > 0 else None
        down_cell = self.__cells[i+1][j] if i < rows - 1 else None
        left_cell = self.__cells[i][j-1] if j > 0 else None
        right_cell = self.__cells[i][j+1] if j < cols - 1 else None
        
        


