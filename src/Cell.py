from Window import Window
from typing import Literal, Self

class Cell:
    def __init__(self, row: int, col: int, side_size: int, window: Window) -> None:
        canvas_padding = window.get_canvas_padding() / 2
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

    def draw_to(self, to_cell: Self, delay_ms: int, type: Literal["maze_solv", "maze_solv_backtrack"]):
        from_center = self.get_center_coord()
        to_center = to_cell.get_center_coord()
        self.__renderer.delay_execution(lambda: self.__renderer.draw_line(from_center, to_center, type=type), delay_ms=delay_ms)

    
    def get_matrix_idxs(self):
        return self.__matrix_idx
    
    def get_overlapping_walls(self, neighbour_cell: Self):
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
