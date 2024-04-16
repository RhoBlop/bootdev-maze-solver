from textwrap import fill
import tkinter as ttk

LINE_WIDTH = 3
LINE_FILL_COLOR = "#000"
#
CANVAS_BG = "#fff"
ROOT_BG = "#fff" # not configured yet
MS_DELAY_BETWEEN_ACTIONS = 500

# (x, y) coordinates
type Point = tuple[int, int]

class Window:
    def __init__(self, width: int, height: int, canvas_padding: int = 0) -> None:
        self.__root = ttk.Tk()
        self.__root.title("Maze Solver")
        self.__root.minsize(width=width+50, height=height+50)
        self.__canvas = ttk.Canvas(self.__root, bg="#fff", width=width+canvas_padding, height=height+canvas_padding, border=0, highlightthickness=0)
        self.__canvas.grid(column=0, row=0)

        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        self.__root.eval('tk::PlaceWindow . center')

        self.__action_count = 0

    def draw_line(self, p1: Point, p2: Point, tags: str = "") -> int:
        return self.__canvas.create_line(p1[0], p1[1], p2[0], p2[1], tags=tags, fill=LINE_FILL_COLOR, width=LINE_WIDTH)
    
    def delete_canvas_item(self, item_id: int) -> None:
        self.__canvas.delete(item_id)

    def animate(self, callback) -> None:
        self.__action_count += 1
        self.__root.after(MS_DELAY_BETWEEN_ACTIONS * self.__action_count, callback)

    def mainloop(self):
        self.__root.mainloop()