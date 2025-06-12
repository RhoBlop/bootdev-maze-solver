import unittest
from Maze import Maze

RANDOM_SEED = 1

# ========= NOT FINISHED =========

# since there isn't much to test I'll use this class for both Maze and Cell classes
# also, this test don't account in any way for visuals with tkinter, not in the mood to search how tow
class TestMaze(unittest.TestCase):
    def test_maze_create_cells_1(self):
        """
        Should create cell's structure correctly for square maze (tests only for 2d matrix size)
        """
        maze = Maze(NUM_ROWS=2, NUM_COLUMNS=2, SEED=RANDOM_SEED)
        num_rows = len(maze.get_cells())
        num_cols = len(maze.get_cells()[0])
        self.assertEqual((num_rows, num_cols), (2, 2))

    def test_maze_create_cells_2(self):
        """
        Should create cell's structure correctly for maze with more rows than columns (tests only for 2d matrix size)
        """
        maze = Maze(NUM_ROWS=3, NUM_COLUMNS=2, SEED=RANDOM_SEED)
        num_rows = len(maze.get_cells())
        num_cols = len(maze.get_cells()[0])
        self.assertEqual((num_rows, num_cols), (3, 2))

    def test_maze_create_cells_3(self):
        """
        Should create cell's structure correctly for maze with more columns than rows (tests only for 2d matrix size)
        """
        maze = Maze(NUM_ROWS=2, NUM_COLUMNS=3, SEED=RANDOM_SEED)
        num_rows = len(maze.get_cells())
        num_cols = len(maze.get_cells()[0])
        self.assertEqual((num_rows, num_cols), (2, 3))

    def test_maze_neighbours_corners(self):
        """
        Should get only two neighbours indices for cells on corners
        """
        nr, nc = 4, 4
        maze = Maze(NUM_ROWS=nr, NUM_COLUMNS=nc, SEED=RANDOM_SEED)
        cells = maze.get_cells()
        c1, c2, c3, c4 = cells[0][0], cells[0][3], cells[3][0], cells[3][3]

        self.assertEqual(c1.get_neighbours_idxs(nr, nc), [(0, 1), (1, 0)], "Incorrect output on top-left corner")
        self.assertEqual(c2.get_neighbours_idxs(nr, nc), [(0, 2), (1, 3)], "Incorrect output on top-right corner")
        self.assertEqual(c3.get_neighbours_idxs(nr, nc), [(3, 1), (2, 0)], "Incorrect output on bottom-left corner")
        self.assertEqual(c4.get_neighbours_idxs(nr, nc), [(3, 2), (2, 3)], "Incorrect output on bottom-right corner")

    def test_maze_neighbours_edges(self):
        """
        Should get only three neighbours indices for cells on edges (that are also not on corners)
        """
        nr, nc = 4, 4
        maze = Maze(NUM_ROWS=nr, NUM_COLUMNS=nc, SEED=RANDOM_SEED)
        cells = maze.get_cells()
        e1, e2 = cells[0][1], cells[2][3]

        self.assertEqual(e1.get_neighbours_idxs(nr,nc), [(0, 0), (0, 2), (1, 1)], "Incorrect output for [0][1]")
        self.assertEqual(e2.get_neighbours_idxs(nr,nc), [(2, 2), (1, 3), (3, 3)], "Incorrect output for [2][3]")

    def test_maze_neighbours_inner(self):
        """
        Should get four neighbours indices for cells that are not in edges nor in corners
        """
        nr, nc = 4, 4
        maze = Maze(NUM_ROWS=nr, NUM_COLUMNS=nc, SEED=RANDOM_SEED)
        cells = maze.get_cells()
        in1, in2 = cells[1][2], cells[2][1]

        self.assertEqual(in1.get_neighbours_idxs(nr,nc), [(1, 1), (1, 3), (0, 2), (2, 2)], "Incorrect output for [1][2]")
        self.assertEqual(in2.get_neighbours_idxs(nr,nc), [(2, 0), (2, 2), (1, 1), (3, 1)], "Incorrect output for [2][1]")

    def test_delete_wall(self):
        maze = Maze(NUM_ROWS=2, NUM_COLUMNS=2, SEED=RANDOM_SEED)

if __name__ == "__main__":
    unittest.main()