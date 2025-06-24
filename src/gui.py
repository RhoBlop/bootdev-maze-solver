import tkinter as tk
import sys
from typing import Literal

# (x, y) coordinates
type Point = tuple[float, float]

class Window:
    def __init__(self, width: int, height: int, 
                 root_bg: str, canvas_bg: str, canvas_padding: int,
                 wall_line_width: int, wall_line_color: str, solving_line_width: int, solving_line_color: str,
                 solving_line_color_backtrack: str
                 ) -> None:
        self.__root = tk.Tk()

        # Maximize window depending on platform
        if sys.platform.startswith("win"):
            self.__root.state("zoomed")
        elif sys.platform.startswith("linux"):
            self.__root.attributes("-zoomed", True)

        self.__root.title("Maze Solver")
        self.__root.configure(background=root_bg)
        self.__canvas = tk.Canvas(self.__root, bg=canvas_bg, width=width+canvas_padding, height=height+canvas_padding, border=0, highlightthickness=0)
        self.__canvas.grid(column=0, row=0)

        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        self.__current_delay = 0  # used for delaying the maze visualization
        self.__config = {
            "canvas_padding": canvas_padding,
            "wall_line_width": wall_line_width,
            "wall_line_color": wall_line_color,
            "solving_line_width": solving_line_width,
            "solving_line_color": solving_line_color,
            "solving_line_color_backtrack": solving_line_color_backtrack
        }

    def get_canvas_pading(self):
        return self.__config["canvas_padding"]

    def draw_line(self, p1: Point, p2: Point, type: Literal["maze_gen", "maze_solv", "maze_solv_backtrack"]) -> int:
        line_width = 0
        fill_color = ""

        # Determine the line width and color based on the type of line
        if type == "maze_gen":
            line_width = self.__config["wall_line_width"]
            fill_color = self.__config["wall_line_color"]
        elif type == "maze_solv":
            line_width = self.__config["solving_line_width"]
            fill_color = self.__config["solving_line_color"]
        elif type == "maze_solv_backtrack":
            line_width = self.__config["solving_line_width"]
            fill_color = self.__config["solving_line_color_backtrack"]
            
        return self.__canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=fill_color, width=line_width)
    
    def delete_canvas_item(self, item_id: int) -> None:
        self.__canvas.delete(item_id)

    def delay_execution(self, callback, delay_ms) -> None:
        self.__current_delay += delay_ms
        self.__root.after(self.__current_delay, callback)

    def mainloop(self):
        self.__root.mainloop()