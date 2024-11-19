
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from src.bitboard_utils import get_active_positions
from src.chess_backend_v2.piece import Piece, PieceTypeEnum

@dataclass
class Move:
    start_bitboard: int
    end_bitboard: int
    
class MoveTypeEnum(Enum):
    NORMAL = 1
    CAPTURE = 2
    ENPASSANT = 3
    CASTLING = 4
    PROMOTION = 5
    PROMOTION_CAPTURE = 6
    
    def to_json(self):
        return self.value
        
    @staticmethod
    def from_json(value) -> "MoveTypeEnum":
        return MoveTypeEnum(value)

@dataclass
class MoveRecord:
    start_bitboard: int
    end_bitboard: int
    move_type: MoveTypeEnum
    
    # For 50 move rule
    moved_piece_type: PieceTypeEnum
    
    # For enpassant
    enpassant_bitboard: int
    enpassant_capture_bitboard: int
    
    # For captures
    captured_piece: Optional[Piece] = None
    
    # For castling
    rook_start_bitboard: Optional[int] = None
    rook_end_bitboard: Optional[int] = None
    
    def __repr__(self) -> str:
        s = f"Start: {get_active_positions(self.start_bitboard)}"
        s += f", End: {get_active_positions(self.end_bitboard)}"
        s += f", Type: {self.move_type}"
        if self.captured_piece:
            s += f", Captured piece: {self.captured_piece}"
        if self.enpassant_bitboard:
            s += f", Enpassant: {get_active_positions(self.enpassant_bitboard)}"
        if self.enpassant_capture_bitboard:
            s += f", Enpassant_capture: {get_active_positions(self.enpassant_capture_bitboard)}"
        if self.rook_start_bitboard:
            s += f", Rook start: {get_active_positions(self.rook_start_bitboard)}"
        if self.rook_start_bitboard:
            s += f", Rook end: {get_active_positions(self.rook_start_bitboard)}"
        return s

    def to_json(self):
        data= {
            "start_bitboard": self.start_bitboard,
            "end_bitboard": self.end_bitboard,
            "move_type": self.move_type.to_json(),
            "moved_piece_type": self.moved_piece_type.to_json(),
            "enpassant_bitboard": self.enpassant_bitboard,
            "enpassant_capture_bitboard": self.enpassant_capture_bitboard,
            
            # For captures
            "captured_piece": self.captured_piece.to_json() if self.captured_piece is not None else None,
            
            # For castling
            "rook_start_bitboard": self.rook_start_bitboard,
            "rook_end_bitboard": self.rook_end_bitboard
        }
        return data
    
    @staticmethod
    def from_json(data) -> "MoveRecord":
        captured_piece = Piece.from_json(data["captured_piece"]) if data["captured_piece"] is not None else None
        
        return MoveRecord(
            start_bitboard = data["start_bitboard"],
            end_bitboard = data["end_bitboard"],
            move_type = MoveTypeEnum.from_json(data["move_type"]),
            moved_piece_type = PieceTypeEnum.from_json(data["moved_piece_type"]),  
            enpassant_bitboard = data["enpassant_bitboard"],
            enpassant_capture_bitboard = data["enpassant_capture_bitboard"],

            captured_piece = captured_piece,  

            rook_start_bitboard = data["rook_start_bitboard"],
            rook_end_bitboard = data["rook_end_bitboard"]
        )