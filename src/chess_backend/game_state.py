from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameState:
    turn: int
    game_is_over: bool
    winner: int
    
    # These variables are meant to be lists (of length three) where index 1 is white, -1 is black
    king_in_check: list[bool]
    enpassant_end_square: list[Tuple[int]|None]
    kingside_castling_possible: list[bool]
    queenside_castling_possible: list[bool]
    
    def copy(self) -> "GameState":
        gs = GameState(
            turn = self.turn,
            game_is_over= self.game_is_over,
            winner = self.winner,
            king_in_check= self.king_in_check[:],
            enpassant_end_square= self.enpassant_end_square[:],
            kingside_castling_possible= self.kingside_castling_possible[:],
            queenside_castling_possible= self.queenside_castling_possible[:]
        )
        return gs
    
    def __repr__(self) -> str:
        s = f"id: {id(self)}\n"
        for key, val in self.__dict__.items():
            s += f"{key}: {val}\n"
        return s
    
    def to_json(self):
        data = {
            "turn" : self.turn,
            "game_is_over" : self.game_is_over,
            "winner " : self.winner,
            "king_in_check" : self.king_in_check,
            "enpassant_end_square" : self.enpassant_end_square,
            "kingside_castling_possible" : self.kingside_castling_possible,
            "queenside_castling_possible" : self.queenside_castling_possible
        }
        return data
        
    @staticmethod
    def from_json(data) -> "GameState":
        gs = GameState(
            turn = data["turn"],
            game_is_over= data["game_is_over"],
            winner = data["winner"],
            king_in_check= data["king_in_check"],
            enpassant_end_square= data["enpassant_end_square"],
            kingside_castling_possible= data["kingside_castling_possible"],
            queenside_castling_possible= data["queenside_castling_possible"]
        )
        return gs