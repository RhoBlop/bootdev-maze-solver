import json
from Maze import Maze

def main():
    with open("config.json", "r") as f:
        config_dict = json.load(f)
        maze = Maze(**config_dict)
        maze.start()

if __name__ == "__main__":
    main()