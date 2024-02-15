from graphic import *
from cell import *


def main():
    win = Window(800, 800)
    maze = Maze(10, 10, 15, 10, 50, win)
    win.wait_for_close()


main()