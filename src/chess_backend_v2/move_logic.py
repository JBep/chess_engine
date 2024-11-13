from functools import lru_cache
from typing import Iterable, List
from src.chess_backend_v2.psuedo_legal_moves import get_bishop_psuedo_legal_moves, get_king_psuedo_legal_moves, get_knight_psuedo_legal_moves, get_pawn_psuedo_legal_moves, get_queen_psuedo_legal_moves, get_rook_psuedo_legal_moves
from src.chess_backend_v2.checking_logic import square_is_attacked, squares_are_attacked
from src.chess_backend_v2.bitboard_constants import (
    BLACK_KINGSIDE_CASTLING_LANE, BLACK_KINGSIDE_CASTLING_PASSED_SQUARE, BLACK_QUEENSIDE_CASTLING_LANE, BLACK_QUEENSIDE_CASTLING_PASSED_SQUARE,
    WHITE_KINGSIDE_CASTLING_LANE, WHITE_KINGSIDE_CASTLING_PASSED_SQUARE, WHITE_QUEENSIDE_CASTLING_LANE, WHITE_QUEENSIDE_CASTLING_PASSED_SQUARE,
    KING_STARTING_POSITIONS, 
    KINGSIDE_CASTLING_KING_END_SQUARES, 
    QUEENSIDE_CASTLING_KING_END_SQUARES
    )
from src.chess_backend_v2.piece import ColorEnum, Piece, PieceTypeEnum

"""Helper module to assisst with logic related to making a move."""


@lru_cache
def compute_enpassant_position(start_bitboard: int, end_bitboard:int, piece_type:PieceTypeEnum, color:ColorEnum):
    enpassant_bitboard, enpassant_capture_bitboard = 0,0
    if piece_type == PieceTypeEnum.PAWN:
        if color == ColorEnum.WHITE:
            if start_bitboard << 16 == end_bitboard:
                enpassant_bitboard = start_bitboard << 8
                enpassant_capture_bitboard = end_bitboard
        else:
            if start_bitboard >> 16 == end_bitboard:
                enpassant_bitboard = start_bitboard >> 8
                enpassant_capture_bitboard = end_bitboard
           
    return enpassant_bitboard, enpassant_capture_bitboard


def compute_castling_position(pieces: List[Piece], color: ColorEnum, kingside_castling_lane: int, queenside_castling_lane: int, kingside_castling_passed_square:int, queenside_castling_passed_square:int):
    king = None
    kingside_rook = None
    queenside_rook = None
    all_pieces = 0
    
    for piece in pieces:
        all_pieces |= piece.location
        if piece.color == color:
            if piece.type == PieceTypeEnum.KING:
                king = piece
            elif piece.type == PieceTypeEnum.KINGSIDE_ROOK:
                kingside_rook = piece
            elif piece.type == PieceTypeEnum.QUEENSIDE_ROOK:
                queenside_rook = piece
    
    castling_bitboard = 0
    if king.has_moved == False:
        if kingside_rook and kingside_rook.has_moved == False and all_pieces & kingside_castling_lane == 0 and not square_is_attacked(square = kingside_castling_passed_square, pieces=pieces, color=color):
            castling_bitboard |= (KINGSIDE_CASTLING_KING_END_SQUARES & kingside_castling_lane)
            
        elif queenside_rook and queenside_rook.has_moved == False and all_pieces & queenside_castling_lane == 0 and not square_is_attacked(square = queenside_castling_passed_square, pieces=pieces, color=color):
            castling_bitboard |= (QUEENSIDE_CASTLING_KING_END_SQUARES & queenside_castling_lane)
            
    return castling_bitboard

@lru_cache
def compute_rook_move_if_castling(start_bitboard: int, end_bitboard: int, piece_type: PieceTypeEnum, color: ColorEnum):
    if piece_type != PieceTypeEnum.KING:
        return None
    
    rook_start_bitboard = 0
    if (start_bitboard & KING_STARTING_POSITIONS) != 0:
        if (end_bitboard & KINGSIDE_CASTLING_KING_END_SQUARES) != 0:
            rook_start_bitboard = end_bitboard << 1
            rook_end_bitboard = end_bitboard >> 1
                
        elif (end_bitboard & QUEENSIDE_CASTLING_KING_END_SQUARES) != 0:    
            rook_start_bitboard = end_bitboard >> 2
            rook_end_bitboard = end_bitboard << 1

    
    if rook_start_bitboard != 0:
        return rook_start_bitboard, rook_end_bitboard
    else:
        return None


def get_psuedo_legal_moves(piece: Piece, pieces: Iterable[Piece], white_bitboard: int, black_bitboard: int, enpassant_bitboard:int) -> int:
    if piece.color == ColorEnum.WHITE:
        own_color_bitboard = white_bitboard
        opposing_color_bitboard = black_bitboard
    else: 
        own_color_bitboard = black_bitboard
        opposing_color_bitboard = white_bitboard
        
    piece_type = piece.type
    
    if piece_type == PieceTypeEnum.PAWN:
        return get_pawn_psuedo_legal_moves(
            start_bitboard = piece.location, 
            white_bitboard = white_bitboard, 
            black_bitboard = black_bitboard, 
            color = piece.color, 
            has_moved = piece.has_moved,
            enpassant_bitboard = enpassant_bitboard
            )
        
    elif piece_type == PieceTypeEnum.KNIGHT:
        return get_knight_psuedo_legal_moves(
            start_bitboard = piece.location, 
            own_color_bitboard = own_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.BISHOP:
        return get_bishop_psuedo_legal_moves(
            start_bitboard = piece.location, 
            own_color_bitboard = own_color_bitboard, 
            opposing_color_bitboard = opposing_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.KINGSIDE_ROOK or piece_type == PieceTypeEnum.QUEENSIDE_ROOK:
        return get_rook_psuedo_legal_moves(
            start_bitboard = piece.location,  
            own_color_bitboard = own_color_bitboard, 
            opposing_color_bitboard = opposing_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.QUEEN:
        return get_queen_psuedo_legal_moves(
            start_bitboard = piece.location,  
            own_color_bitboard = own_color_bitboard, 
            opposing_color_bitboard = opposing_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.KING:
        if piece.color == ColorEnum.WHITE:
            kingside_castling_lane = WHITE_KINGSIDE_CASTLING_LANE
            kingside_castling_passed_square = WHITE_KINGSIDE_CASTLING_PASSED_SQUARE
            queenside_castling_lane = WHITE_QUEENSIDE_CASTLING_LANE
            queenside_castling_passed_square = WHITE_QUEENSIDE_CASTLING_PASSED_SQUARE
        else:
            kingside_castling_lane = BLACK_KINGSIDE_CASTLING_LANE
            kingside_castling_passed_square = BLACK_KINGSIDE_CASTLING_PASSED_SQUARE
            queenside_castling_lane = BLACK_QUEENSIDE_CASTLING_LANE
            queenside_castling_passed_square = BLACK_QUEENSIDE_CASTLING_PASSED_SQUARE
        castling_bitboard = compute_castling_position(
            pieces = pieces, 
            color = piece.color, 
            kingside_castling_lane=kingside_castling_lane, 
            kingside_castling_passed_square=kingside_castling_passed_square,
            queenside_castling_lane=queenside_castling_lane,
            queenside_castling_passed_square=queenside_castling_passed_square
            )
                
        return get_king_psuedo_legal_moves(
            start_bitboard = piece.location,  
            own_color_bitboard = own_color_bitboard,
            castling_bitboard = castling_bitboard
            )
