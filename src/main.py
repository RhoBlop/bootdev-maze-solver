import json
from Maze import Maze

def main():
    with open("config.json", "r") as f:
        config_dict = json.load(f)
        if config_dict.get("NUM_COLUMNS") > 40 or config_dict.get("NUM_ROWS") > 40:
            print("Erro: NUM_COLUMNS e NUM_ROWS devem ser menores ou iguais a 40. (motivos de desempenho)")
            return
        
        maze = Maze(**config_dict)
        maze.start()

if __name__ == "__main__":
    main()