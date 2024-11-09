
from abc import ABC
from typing import Set

from src.chess_backend_v2.move import Move
from src.chess_backend_v2.piece import Piece


class ChessBoard(ABC):
    def get_legal_moves(lazy:bool) -> Set[Move]:
        pass
    
    def make_move(move:Move):
        pass
    
    def unmake_move(move:Move):
        pass
    
    # For drawing
    def get_piece(rank:int, file:int) -> Piece | None:
        pass
    
    