from graphics import Window

def main():
    win = Window(width=600, height=600)
    win.draw_line((0, 0), (300, 300))
    win.mainloop()

if __name__ == "__main__":
    main()