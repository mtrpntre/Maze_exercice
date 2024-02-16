import unittest
from cell_and_maze import Maze

class TestMaze(unittest.TestCase):
    def test_maze_create_cells(self):
        num_columns = 10
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_columns, 50)
        self.assertEqual(len(m1._Maze__cells), num_rows)
        self.assertEqual(len(m1._Maze__cells[0]), num_columns)

if __name__ == '__main__':
    unittest.main()