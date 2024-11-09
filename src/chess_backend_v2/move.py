
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
from src.chess_backend_v2.piece import Piece
from src.chess_backend.chess_utils import algebraic_move
from src.chess_backend.game_state import GameState

class MoveTypeEnum(Enum):
    NORMAL = 1
    CAPTURE = 2
    KINGSIDE_CASTLING = 3
    QUEENSIDE_CASTLING = 4
    PAWN_DOUBLE_STEP = 5
    ENPASSANT = 6
    PAWN_PROMOTION = 7
    

@dataclass
class Move:
    start_bitboard: Tuple[int,int]
    end_bitboard: Tuple[int,int]
    

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            if self.start_bitboard == other.start_bitboard and self.end_bitboard == other.end_bitboard:
                return True
        return False
    
    def __hash__(self) -> int:
        return hash((self.start_bitboard, self.end_bitboard, self.move_type))

    # def __repr__(self) -> str:
    #     return algebraic_move(self)
        
    # def to_json(self):
    #     data = {
    #         "start_square": self. start_square,
    #         "end_square": self.end_square,
    #         "piece": self.piece,
    #         "move_type": self.move_type.value,
    #         "captured_piece": self.captured_piece,
    #         "enpassant_capture_square": self.enpassant_capture_square,
    #         "pawn_promotion_piece": self.pawn_promotion_piece,
    #         "rook_start_square": self.rook_start_square,
    #         "rook_end_square": self.rook_end_square
    #     }
    #     return data
    
    # @staticmethod
    # def from_json(data) -> "Move":
    #     move = Move(
    #         start_square = data["start_square"],
    #         end_square = data["end_square"],
    #         piece = data["piece"],
    #         move_type = MoveTypeEnum(data["move_type"]),
    #         captured_piece = data["captured_piece"],
    #         enpassant_capture_square = data["enpassant_capture_square"],
    #         pawn_promotion_piece = data["pawn_promotion_piece"],
    #         rook_start_square = data["rook_start_square"],
    #         rook_end_square = data["rook_end_square"],
    #     )
    #     return move

@dataclass
class MoveRecord:
    move: Move
    game_state: GameState
    
    def to_json(self):
        data = {
            "move": self.move.to_json(),
            "game_state": self.game_state.to_json()
        }
        return data
    
    @staticmethod
    def from_json(data) -> "MoveRecord":
        record = MoveRecord(
            move = Move.from_json(data["move"]),
            game_state = data["game_state"],
        )
        return record