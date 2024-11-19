
import json
import uuid
from src.chess_backend.chess_board import ChessBoard

def write_json(data, filename:str, dir:str):
    path = f"{dir}/{filename}"
    with open(path,'w') as file:
        json.dump(data, file)
    
def read_json(filename:str, dir:str):
    path = f"{dir}/{filename}"
    with open(path,'r') as file:
        data = json.load(file)
    return data    
