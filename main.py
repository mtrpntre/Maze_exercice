from graphic import *
from cell_and_maze import *


def main():
    win = Window(800, 800)
    maze = Maze(win, 10,10,10,10,30, 3)
    win.wait_for_close()


main()