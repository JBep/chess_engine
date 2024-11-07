
import json
import uuid
from src.chess_board import ChessBoard

def save_as_json(board: ChessBoard, dir: str):
    game_id = str(uuid.uuid4())
    
    path = f"{dir}/{game_id}"
    with open(path,'w') as f:
        json.dump(board.to_json(), f)
        
    return game_id

def read_from_json(dir: str, game_id: str) -> ChessBoard:
    path = f"{dir}/{game_id}"
    with open(path, 'r') as f:
            data = json.load(f)
        
    board = ChessBoard.from_json(data)
    return board
        
        
