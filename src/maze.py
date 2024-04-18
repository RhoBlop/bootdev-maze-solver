import random as rand
from xml.etree.ElementTree import TreeBuilder
from gui import Point, Window

CANVAS_PADDING = 3

type MazeMatrix = list[list[Cell]]
type VisitedCells = list[Cell]
type TCell = Cell  # workaround

class Maze:
    def __init__(self, num_cols: int = 1, num_rows: int = 1, cell_size: int = 50, seed: int | None = None) -> None:
        window_w, window_h = num_cols * cell_size, num_rows * cell_size
        self.__renderer = Window(width=window_w, height=window_h, canvas_padding=CANVAS_PADDING*2)
        self.__maze = self._create_cells(num_cols, num_rows, cell_size)
        self.__dimensions = (num_rows, num_cols)

        if (seed):
            rand.seed(seed)

    def get_cells(self):
        return self.__maze

    def _create_cells(self, num_cols: int, num_rows: int, cell_size: int) -> MazeMatrix:
        cells: MazeMatrix = []
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                cell = Cell(i, j, window=self.__renderer, side_size=cell_size)
                row.append(cell)
                cell.draw_self()
            cells.append(row)
        return cells
    
    def _open_entrance_and_exit(self) -> None:
        # top-left's left wall
        self.__maze[0][0].delete_wall(3)
        # bottom-right's right wall
        self.__maze[-1][-1].delete_wall(1)

    # there's two solutions to create the gui's visualization delay wanted when solving the maze 
    # (both using tkinter's after() method since sleep() is not much of a good practice):
    #    - recursion calling itself with the after() method, causing the delay
    #    - looping sequentially and multiplying the delay in the after() with an incrementing value (which will queue all the events for tkinter to handle)
    # I'll be using recursion for the sake of practicing it, albeit sequencial loop might be easier to understand
    # (I believe there's not much of a performance difference: queueing will result in a lot of events stored in memory, but recursion is recursion
    #  and all the function calls are also stored until the recursion meets its base case? - actually, it probably is worse than queue's solution)
    def _create_exit_and_solve(self) -> None:
        self._open_entrance_and_exit()

        # choose random cell to start from
        i, j = rand.randrange(0, self.__dimensions[0]), rand.randrange(0, self.__dimensions[1])
        self._generate_maze_dfs(self.__maze[i][j])

        self._solve_maze_r()
        
    # using most simple maze generation method
    def _generate_maze_dfs(self, curr_cell: TCell) -> None:
        curr_cell.set_visited_maze_generation()
        unvisited_neighbours = curr_cell.get_neighbours_idxs(num_cols=self.__dimensions[1], num_rows=self.__dimensions[0])

        # base case (a bit strange indeed)
        while len(unvisited_neighbours) != 0:
            rand_neigh_coord = unvisited_neighbours.pop(rand.randrange(0, len(unvisited_neighbours)))
            row_to_visit, col_to_visit = rand_neigh_coord[0], rand_neigh_coord[1]
            neigh_to_visit = self.__maze[row_to_visit][col_to_visit]

            if neigh_to_visit.is_visited_maze_generation():
                continue

            curr_row, curr_col = curr_cell.get_matrix_idxs()[0], curr_cell.get_matrix_idxs()[1]
            # to the left of curr cell
            if col_to_visit == curr_col - 1:
                curr_cell.delete_wall(3)
                neigh_to_visit.delete_wall(1)
            # to the right of curr cell
            if col_to_visit == curr_col + 1:
                curr_cell.delete_wall(1)
                neigh_to_visit.delete_wall(3)
            # to the top of curr cell
            if row_to_visit == curr_row - 1:
                curr_cell.delete_wall(0)
                neigh_to_visit.delete_wall(2)
            # to the bottom of curr cell
            if row_to_visit == curr_row + 1:
                curr_cell.delete_wall(2)
                neigh_to_visit.delete_wall(0)

            
            self._generate_maze_dfs(neigh_to_visit)

        return
        

    def _solve_maze_r(self) -> None:
        
        return

    
    def start(self) -> None:
        self._create_exit_and_solve()
        self.__renderer.mainloop()


class Cell:
    def __init__(self, row: int, col: int, side_size: int, window: Window) -> None:
        x, y = (col * side_size) + CANVAS_PADDING, (row * side_size) + CANVAS_PADDING
        self.__side_size = side_size
        self.__matrix_idx = (row, col)
        self.__walls = [True, True, True, True]  # clock-wise walls - top, right, bottom, left
        self.__walls_canvas_ids = [0, 0, 0, 0]
        self.__lines_coords = [
            [(x, y), (x + self.__side_size, y)],
            [(x + self.__side_size, y), (x + self.__side_size, y + self.__side_size)],
            [(x + self.__side_size, y + self.__side_size), (x, y + self.__side_size)],
            [(x, y + self.__side_size), (x, y)]
        ]
        self.__visited = [False, False]  # [0] = maze_generation; [1] = maze_solving
        self.__renderer = window

    def __repr__(self):
        return f"({self.__matrix_idx[0]}, {self.__matrix_idx[1]})"

    def draw_self(self):
        for i in range(len(self.__walls)):
            if self.__walls[i]:
                self.__walls_canvas_ids[i] = self.__renderer.draw_line(self.__lines_coords[i][0], self.__lines_coords[i][1])

    def get_walls(self):
        return self.__walls
    
    def get_matrix_idxs(self):
        return self.__matrix_idx

    # because cells are adjacent to one another, there is actually two walls - one for each cell - on each side of the cells (except the edges' ones)
    # e.g. one cell has a right wall, but the adjacent to it also has a left wall, so we need to delete both of them to open a path there
    def delete_wall(self, wall_idx):
        if self.__walls[wall_idx]:
            self.__renderer.delay_execution(lambda: self.__renderer.delete_canvas_item(self.__walls_canvas_ids[wall_idx]))
            self.__walls[wall_idx] = False

    def get_neighbours_idxs(self, num_rows: int, num_cols: int) -> list[tuple[int, int]]:
        neigh = []
        # starts at 0 because it's index
        row, col = self.__matrix_idx[0], self.__matrix_idx[1]

        # left
        if col > 0:
            neigh.append((row, col - 1))
        # right
        if col < num_cols - 1:
            neigh.append((row, col + 1))
        #up
        if row > 0:
            neigh.append((row - 1, col))
        #down
        if row < num_rows - 1:
            neigh.append((row + 1, col))

        return neigh
    
    def is_visited_maze_generation(self) -> bool:
        return self.__visited[0]
    def set_visited_maze_generation(self) -> None:
        self.__visited[0] = True

    def is_visited_maze_solving(self) -> bool:
        return self.__visited[1]
    def set_visited_maze_solving(self) -> None:
        self.__visited[1] = True 
