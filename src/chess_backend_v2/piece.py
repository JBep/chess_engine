from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set

from src.chess_backend_v2.bitboard_utils import activate_position

class ColorEnum(Enum):
    WHITE = 1
    BLACK = 2

class PieceTypeEnum(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    KINGSIDE_ROOK = 4
    QUEENSIDE_ROOK = 5
    QUEEN = 6
    KING = 7
    
@dataclass(eq = True)
class Piece:
    type: PieceTypeEnum
    color: ColorEnum
    placement_bitboard: int 
    has_moved: Optional[bool] = False
    
def initialize_pieces() -> dict[int,Piece]:
    for i in range(8,16):
        white_pawns = {
            Piece(
                type = PieceTypeEnum.PAWN,
                color = ColorEnum.WHITE,
                placement_bitboard = activate_position(bitboard = 0, position = i)
            )
        }
        
    for i in range(48,56):
        black_pawns = {
            Piece(
                type = PieceTypeEnum.PAWN,
                color = ColorEnum.BLACK,
                placement_bitboard = activate_position(bitboard = 0, position = i)
            )
        }
        
    other_pieces = {
        Piece(
            type = PieceTypeEnum.KINGSIDE_ROOK,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 0)
        ),
        Piece(
            type = PieceTypeEnum.QUEENSIDE_ROOK,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 7)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 1)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 6)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 2)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 5)
        ),
        Piece(
            type = PieceTypeEnum.KING,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 4)
        ),
        Piece(
            type = PieceTypeEnum.QUEEN,
            color = ColorEnum.WHITE,
            placement_bitboard = activate_position(bitboard = 0, position = 3)
        ),
        
        # BLACK PIECES
        Piece(
            type = PieceTypeEnum.KINGSIDE_ROOK,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 56)
        ),
        Piece(
            type = PieceTypeEnum.QUEENSIDE_ROOK,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 63)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 57)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 62)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 58)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 61)
        ),
        Piece(
            type = PieceTypeEnum.KING,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 60)
        ),
        Piece(
            type = PieceTypeEnum.QUEEN,
            color = ColorEnum.BLACK,
            placement_bitboard = activate_position(bitboard = 0, position = 59)
        ) 
    }
    
    pieces = white_pawns.union(black_pawns).union(other_pieces)
    piece_dict = []
    for piece in pieces:
        piece_dict[piece.placement_bitboard] = piece
    return piece_dict