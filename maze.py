import random as r
from gui import Point, Window

CANVAS_PADDING = 3

type MazeMatrix = list[list[Cell]]

class Maze:
    def __init__(self, num_cols: int = 1, num_rows: int = 1, cell_size: int = 50) -> None:
        window_w, window_h = num_cols * cell_size, num_rows * cell_size
        self.__renderer = Window(width=window_w, height=window_h, canvas_padding=CANVAS_PADDING*2)
        self.__maze = self._create_cells(num_cols, num_rows, cell_size)
        self._create_exit_path_r()

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
    
    def _break_enter_and_exit(self) -> None:
        # top-left's left wall
        self.__maze[0][0].delete_wall(3)
        # bottom-right's right wall
        self.__maze[-1][-1].delete_wall(1)

    def _create_exit_path_r(self) -> None:
        self.__renderer.animate(self._break_enter_and_exit)

    # def solve_r(self) -> None:
    
    
    def start(self) -> None: 
        self.__renderer.mainloop()


class Cell:
    def __init__(self, row: int, col: int, side_size: int, window: Window, walls: list[bool] = [True, True, True, True]) -> None:
        x, y = (col * side_size) + CANVAS_PADDING, (row * side_size) + CANVAS_PADDING
        self.__side_size = side_size
        self.__top_left_coord: Point = (x, y)
        self.__walls = walls  # clock-wise walls - top, right, bottom, left
        self.__walls_ids = [0, 0, 0, 0]
        self.__lines_coords = [
            [(x, y), (x + self.__side_size, y)],
            [(x + self.__side_size, y), (x + self.__side_size, y + self.__side_size)],
            [(x + self.__side_size, y + self.__side_size), (x, y + self.__side_size)],
            [(x, y + self.__side_size), (x, y)]
        ]
        self.__renderer = window

    def __repr__(self) -> str:
        return f"({self.__top_left_coord[0]}, {self.__top_left_coord[1]})"

    def draw_self(self) -> None:
        for i in range(len(self.__walls)):
            if self.__walls[i]:
                self.__walls_ids[i] = self.__renderer.draw_line(self.__lines_coords[i][0], self.__lines_coords[i][1])

    # because cells are adjacent to one another, there is actually two walls - one for each cell - on each side of the cells (except the edges' ones)
    # e.g. one cell has a right wall, but the adjacent to it also has a left wall, so we need to delete both of them to open a path there
    def delete_wall(self, wall_idx) -> None:
        if self.__walls[wall_idx]:
            self.__renderer.delete_canvas_item(self.__walls_ids[wall_idx])
            self.__walls[wall_idx] = False