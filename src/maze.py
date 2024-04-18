import random as rand
from typing import Literal
from gui import Window

MS_DELAY_BETWEEN_ACTIONS = 20

type MazeMatrix = list[list[Cell]]
type VisitedCells = list[Cell]
type TCell = Cell  # workaround

class Maze:
    def __init__(self, NUM_COLUMNS: int = 1, NUM_ROWS: int = 1, CELL_SIZE: int = 50, SEED: int | None = None,
                 ROOT_BG: str = "#fff", CANVAS_BG: str = "#fff", CANVAS_PADDING: int = 3,
                 WALL_LINE_WIDTH: int = 3, WALL_LINE_COLOR: str = "#000", SOLVING_LINE_WIDTH: int = 2, SOLVING_LINE_COLOR: str = "#f00",
                 SOLVING_LINE_COLOR_BACKTRACK: str = "#aaa", SOLVE_AUTOMATICALLY = True,
                 MS_DELAY_BETWEEN_ACTIONS_MAZE_GENERATION: int = 20, MS_DELAY_BETWEEN_ACTIONS_MAZE_SOLVING: int = 10) -> None:
        
        window_w, window_h = NUM_COLUMNS * CELL_SIZE, NUM_ROWS * CELL_SIZE
        self.__renderer = Window(width=window_w, height=window_h, root_bg=ROOT_BG, canvas_bg=CANVAS_BG, canvas_padding=CANVAS_PADDING*2, 
                                 wall_line_width=WALL_LINE_WIDTH, wall_line_color=WALL_LINE_COLOR, 
                                 solving_line_width=SOLVING_LINE_WIDTH, solving_line_color=SOLVING_LINE_COLOR,
                                 solving_line_color_backtrack=SOLVING_LINE_COLOR_BACKTRACK)
        self.__maze = self._create_cells(NUM_COLUMNS, NUM_ROWS, CELL_SIZE)
        self.__dimensions = (NUM_ROWS, NUM_COLUMNS)
        self.__should_solve = SOLVE_AUTOMATICALLY
        self.__ms_config = {
            "delay_maze_generation": MS_DELAY_BETWEEN_ACTIONS_MAZE_GENERATION,
            "delay_maze_solving": MS_DELAY_BETWEEN_ACTIONS_MAZE_SOLVING 
        }

        if (SEED):
            rand.seed(SEED)

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
    
    def _create_path(self) -> None:
        # open entrance - top-left's left wall
        self.__maze[0][0].delete_wall(3, delay_ms=self.__ms_config["delay_maze_generation"])
        # open exit - bottom-right's right wall
        self.__maze[-1][-1].delete_wall(1, delay_ms=self.__ms_config["delay_maze_generation"])

        # choose random cell to start from
        i, j = rand.randrange(0, self.__dimensions[0]), rand.randrange(0, self.__dimensions[1])
        self._generate_maze_dfs(self.__maze[i][j])

    # there's two solutions to create the gui's visualization delay wanted when solving the maze 
    # (both using tkinter's after() method since sleep() is not much of a good practice):
    #    - recursion calling itself with the after() method, causing the delay
    #    - looping sequentially and multiplying the delay in the after() with an incrementing value (which will queue all the events for tkinter to handle)
    # I'll be using recursion for the sake of practicing it, albeit sequencial loop might be easier to understand
    # (I believe there's not much of a performance difference: queueing will result in a lot of events stored in memory, but recursion is recursion
    #  and all the function calls are also stored until the recursion meets its base case? - actually, it probably is worse than queue's solution)
    # p.s.: I pity the one who wrote the comment above
        
    # using most simple maze generation method
    def _generate_maze_dfs(self, curr_cell: TCell) -> None:
        curr_cell.set_visited_maze_generation()
        unvisited_neighbours = curr_cell.get_neighbours_idxs(num_cols=self.__dimensions[1], num_rows=self.__dimensions[0])

        # base case (a bit strange indeed)
        while len(unvisited_neighbours) != 0:
            rand_neigh_idx = unvisited_neighbours.pop(rand.randrange(0, len(unvisited_neighbours)))
            neigh_to_visit = self.__maze[rand_neigh_idx[0]][rand_neigh_idx[1]]

            if neigh_to_visit.is_visited_maze_generation():
                continue

            overlapping_walls = curr_cell.get_overlapping_walls(neigh_to_visit)
            if overlapping_walls:
                self._delete_two_walls(curr_cell, overlapping_walls[0], neigh_to_visit, overlapping_walls[1])
            
            self._generate_maze_dfs(neigh_to_visit)

        return
   
    def _solve_maze_dfs(self, curr_cell: TCell) -> bool:
        curr_cell.set_visited_maze_solving()
        # base case = reached goal
        if curr_cell.get_matrix_idxs() == self.__maze[-1][-1].get_matrix_idxs():
            return True
        unvisited_neighbours = curr_cell.get_neighbours_idxs(num_cols=self.__dimensions[1], num_rows=self.__dimensions[0])

        for neigh_idx in unvisited_neighbours:
            neigh_to_visit = self.__maze[neigh_idx[0]][neigh_idx[1]]
            overlapping_walls = curr_cell.get_overlapping_walls(neigh_to_visit)
            if not neigh_to_visit.is_visited_maze_solving() and not overlapping_walls:
                curr_cell.draw_to(neigh_to_visit, type="maze_solv", delay_ms=self.__ms_config["delay_maze_solving"])
                solved = self._solve_maze_dfs(neigh_to_visit)
                # if exit was not found, "undo" moves by drawing a line with other color on top of it
                if not solved:
                    neigh_to_visit.draw_to(curr_cell, type="maze_solv_backtrack", delay_ms=self.__ms_config["delay_maze_solving"])
                    continue

                return True
        
        return False
    
    def start(self) -> None:
        self._create_path()
        if self.__should_solve:
            # starts at top-left cell
            self._solve_maze_dfs(self.__maze[0][0])
            
        self.__renderer.mainloop()
    
     # workaround for the ms delay
    def _delete_two_walls(self, cell1: TCell, wall1: int, cell2: TCell, wall2: int):
        cell1.delete_wall(wall1, delay_ms=(self.__ms_config["delay_maze_generation"]) // 2)
        cell2.delete_wall(wall2, delay_ms=(self.__ms_config["delay_maze_generation"] // 2))


class Cell:
    def __init__(self, row: int, col: int, side_size: int, window: Window) -> None:
        canvas_padding = window.get_canvas_pading() / 2
        x, y = (col * side_size) + canvas_padding, (row * side_size) + canvas_padding
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
                self.__walls_canvas_ids[i] = self.__renderer.draw_line(self.__lines_coords[i][0], self.__lines_coords[i][1], type="maze_gen")

    def get_center_coord(self):
        top_l_x, top_l_y = self.__lines_coords[0][0][0], self.__lines_coords[0][0][1]
        # simple math midpoint formula
        center_x, center_y = (top_l_x + (top_l_x + self.__side_size)) / 2, (top_l_y + (top_l_y + self.__side_size)) / 2
        return (center_x, center_y)

    def draw_to(self, to_cell: TCell, delay_ms: int, type: Literal["maze_solv", "maze_solv_backtrack"]):
        from_center = self.get_center_coord()
        to_center = to_cell.get_center_coord()
        self.__renderer.delay_execution(lambda: self.__renderer.draw_line(from_center, to_center, type=type), delay_ms=delay_ms)

    
    def get_matrix_idxs(self):
        return self.__matrix_idx
    
    def get_overlapping_walls(self, neighbour_cell: TCell):
        self_row, self_col = self.get_matrix_idxs()[0], self.get_matrix_idxs()[1]
        neigh_row, neigh_col = neighbour_cell.get_matrix_idxs()[0], neighbour_cell.get_matrix_idxs()[1]
        # to the left of curr cell
        if neigh_col == self_col - 1 and self.has_wall(3) and neighbour_cell.has_wall(1):
            return (3, 1)
        # to the right of curr cell
        if neigh_col == self_col + 1 and self.has_wall(1) and neighbour_cell.has_wall(3):
            return (1, 3)
        # to the top of curr cell
        if neigh_row == self_row - 1 and self.has_wall(0) and neighbour_cell.has_wall(2):
            return (0, 2)
        # to the bottom of curr cell
        if neigh_row == self_row + 1 and self.has_wall(2) and neighbour_cell.has_wall(0):
            return(2, 0)

    def get_walls(self):
        return self.__walls
    
    def has_wall(self, idx: int):
        return self.__walls[idx]

    # because cells are adjacent to one another, there is actually two walls - one for each cell - on each side of the cells (except the edges' ones)
    # e.g. one cell has a right wall, but the adjacent to it also has a left wall, so we need to delete both of them to open a path there
    def delete_wall(self, wall_idx: int, delay_ms: int):
        if self.__walls[wall_idx]:
            self.__renderer.delay_execution(lambda: self.__renderer.delete_canvas_item(self.__walls_canvas_ids[wall_idx]), delay_ms=delay_ms)
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
