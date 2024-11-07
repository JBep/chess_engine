import logging
from src.log import setup_log
from src.game.gameloop import run_game
def main():
    
    
    setup_log(logging.DEBUG)

    run_game(bot = True)
    
if __name__ == "__main__":
    main() 