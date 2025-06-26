import random as rand
from Cell import Cell
from Window import Window

type MazeMatrix = list[list[Cell]]
type VisitedCells = list[Cell]

class Maze:
    # if not AUTO_CELL_SIZE, cell size is used to calculate the window size
    def __init__(self, 
            NUM_COLUMNS: int = 1,
            NUM_ROWS: int = 1,
            AUTO_CELL_SIZE: bool = True,
            CELL_SIZE: int = 0,
            SEED: int | None = None,
            ROOT_BG: str = "#fff",
            CANVAS_BG: str = "#fff",
            CANVAS_PADDING: int = 3,
            WALL_LINE_WIDTH: int = 3,
            WALL_LINE_COLOR: str = "#000",
            SOLVING_LINE_WIDTH: int = 2,
            SOLVING_LINE_COLOR: str = "#f00",
            SOLVING_LINE_COLOR_BACKTRACK: str = "#aaa",
            SHOULD_SOLVE_MAZE = True,
            MS_DELAY_BETWEEN_ACTIONS_MAZE_GENERATION: int = 20,
            MS_DELAY_BETWEEN_ACTIONS_MAZE_SOLVING: int = 10
        ) -> None:
        
        self.__renderer = Window(
            num_cols=NUM_COLUMNS,
            num_rows=NUM_ROWS,
            auto_cell_size=AUTO_CELL_SIZE,
            cell_size=CELL_SIZE,
            root_bg=ROOT_BG,
            canvas_bg=CANVAS_BG,
            canvas_padding=CANVAS_PADDING*2,
            wall_line_width=WALL_LINE_WIDTH,
            wall_line_color=WALL_LINE_COLOR,
            solving_line_width=SOLVING_LINE_WIDTH, solving_line_color=SOLVING_LINE_COLOR,
            solving_line_color_backtrack=SOLVING_LINE_COLOR_BACKTRACK
        )
        self.__maze = self._create_cells(NUM_COLUMNS, NUM_ROWS, self.__renderer.get_cell_size())
        self.__dimensions = (NUM_ROWS, NUM_COLUMNS)
        self.__should_solve = SHOULD_SOLVE_MAZE
        self.__ms_config = {
            "delay_maze_generation": MS_DELAY_BETWEEN_ACTIONS_MAZE_GENERATION,
            "delay_maze_solving": MS_DELAY_BETWEEN_ACTIONS_MAZE_SOLVING 
        }

        if (SEED):
            rand.seed(SEED)

    def get_cells(self):
        return self.__maze

    def _create_cells(self, num_cols: int, num_rows: int, cell_size: int) -> MazeMatrix:
        cells = []
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
    # p.s.: I pity the one who wrote the comment above. I now realize a graph was probably a better way to structure the maze, the overlapping walls really were annoying to deal with
    #       Also, I ended up queueing all the events sequentially for tkinter to deal with
        
    # using most simple maze generation method
    def _generate_maze_dfs(self, curr_cell: Cell) -> None:
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
   
    def _solve_maze_dfs(self, curr_cell: Cell) -> bool:
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
    def _delete_two_walls(self, cell1: Cell, wall1: int, cell2: Cell, wall2: int):
        cell1.delete_wall(wall1, delay_ms=(self.__ms_config["delay_maze_generation"]) // 2)
        cell2.delete_wall(wall2, delay_ms=(self.__ms_config["delay_maze_generation"] // 2))
