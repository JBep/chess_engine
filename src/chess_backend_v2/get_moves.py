


from functools import lru_cache
from operator import index
from tracemalloc import start
from src.chess_backend_v2.move import MoveTypeEnum
from src.chess_backend_v2.bitboard_utils import activate_position, activate_positions
from src.chess_backend_v2.move import Move
from src.chess_backend_v2.piece import ColorEnum, Piece, PieceTypeEnum
from src.chess_backend_v2.bitboard_constants import ALL_ACTIVE_BITBOARD, RANK_A_BITBOARD, RANK_H_BITBOARD, RANK_B_BITBOARD, RANK_G_BITBOARD, FILE_1_BITBOARD, FILE_2_BITBOARD, FILE_7_BITBOARD, FILE_8_BITBOARD

def get_psuedo_legal_moves(piece: Piece, white_bitboard: int, black_bitboard: int, enpassant_bitboard:int, castling_bitboard:int) -> int:
    if piece.color == ColorEnum.WHITE:
        own_color_bitboard = white_bitboard
        opposing_color_bitboard = black_bitboard
    else: 
        own_color_bitboard = black_bitboard
        opposing_color_bitboard = white_bitboard
        
    piece_type = piece.type
    
    if piece_type == PieceTypeEnum.PAWN:
        return get_pawn_psuedo_legal_moves(
            start_bitboard = piece.placement_bitboard, 
            white_bitboard = white_bitboard, 
            black_bitboard = black_bitboard, 
            color = piece.color, 
            has_moved = piece.has_moved,
            enpassant_bitboard = enpassant_bitboard
            )
        
    elif piece_type == PieceTypeEnum.KNIGHT:
        return get_knight_psuedo_legal_moves(
            start_bitboard = piece.placement_bitboard, 
            own_color_bitboard = own_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.BISHOP:
        return get_bishop_psuedo_legal_moves(
            start_bitboard = piece.placement_bitboard, 
            own_color_bitboard = own_color_bitboard, 
            opposing_color_bitboard = opposing_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.KINGSIDE_ROOK or piece_type == PieceTypeEnum.QUEENSIDE_ROOK:
        return get_rook_psuedo_legal_moves(
            start_bitboard = piece.placement_bitboard,  
            own_color_bitboard = own_color_bitboard, 
            opposing_color_bitboard = opposing_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.QUEEN:
        return get_queen_psuedo_legal_moves(
            start_bitboard = piece.placement_bitboard,  
            own_color_bitboard = own_color_bitboard, 
            opposing_color_bitboard = opposing_color_bitboard
            )
        
    elif piece_type == PieceTypeEnum.KING:
        return get_king_psuedo_legal_moves(
            start_bitboard = piece.placement_bitboard,  
            own_color_bitboard = own_color_bitboard,
            castling_bitboard = castling_bitboard
            )
    

# TODO can I change this to only use relevant parts ot the board and thus make it cacheable?
@lru_cache
def get_pawn_psuedo_legal_moves(start_bitboard:int, white_bitboard:int, black_bitboard: int,  color: ColorEnum, has_moved: bool, enpassant_bitboard: int) -> int:
    end_bitboard = 0
    if color == ColorEnum.WHITE:
        own_color_bitboard = white_bitboard
        opposing_color_bitboard = black_bitboard
        one_step_forward_bitboard = start_bitboard<<8
        two_step_forward_bitboard = start_bitboard<<16
        west_capture_bitboard = start_bitboard<<7
        east_capture_bitboard = start_bitboard<<9
    else:
        own_color_bitboard = black_bitboard
        opposing_color_bitboard = white_bitboard
        one_step_forward_bitboard = start_bitboard>>8
        two_step_forward_bitboard = start_bitboard>>16
        west_capture_bitboard = start_bitboard>>9
        east_capture_bitboard = start_bitboard>>7

    end_bitboard |= (one_step_forward_bitboard & ~(own_color_bitboard | opposing_color_bitboard)) # Straight ahead
    if not has_moved and end_bitboard != 0:
        end_bitboard |= (two_step_forward_bitboard & ~(own_color_bitboard | opposing_color_bitboard)) # Two steps ahead
            
    # If pawn not in rank A, and there's an opposing piece in the left forward diagonal.
    if (start_bitboard & RANK_A_BITBOARD) == 0:
        end_bitboard |= (west_capture_bitboard & (opposing_color_bitboard|enpassant_bitboard))
        
    # If pawn not in rank H, and there's an opposing piece in the right forward diagonal.
    if (start_bitboard & RANK_H_BITBOARD) == 0:
        end_bitboard |= (east_capture_bitboard & (opposing_color_bitboard|enpassant_bitboard))
        
    return end_bitboard

@lru_cache
def get_knight_psuedo_legal_moves(start_bitboard: int, own_color_bitboard:int ):
    end_bitboard = (
        (start_bitboard << 17) & ~(RANK_A_BITBOARD) |  # 2 up, 1 right (from white's perspective)
        (start_bitboard << 15) & ~(RANK_H_BITBOARD) |  # 2 up, 1 left
        (start_bitboard >> 17) & ~(RANK_H_BITBOARD) |  # 2 down, 1 left
        (start_bitboard >> 15) & ~(RANK_A_BITBOARD) |  # 2 down, 1 right
        (start_bitboard << 10) & ~(RANK_A_BITBOARD | RANK_B_BITBOARD) |  # 1 up, 2 right
        (start_bitboard << 6) & ~(RANK_G_BITBOARD | RANK_H_BITBOARD) |   # 1 up, 2 left
        (start_bitboard >> 10) & ~(RANK_G_BITBOARD | RANK_H_BITBOARD) |  # 1 down, 2 left
        (start_bitboard >> 6) & ~(RANK_A_BITBOARD | RANK_B_BITBOARD)     # 1 down, 2 right
    )
    end_bitboard &= ALL_ACTIVE_BITBOARD
    end_bitboard &= ~own_color_bitboard
    return end_bitboard

@lru_cache
def slide_moves(start_bitboard: int, board_end_mask: int, own_color_bitboard: int, opposing_color_bitboard:int, shift: int):
    moves = 0
    pos = start_bitboard
    while True:
        pos = (pos << shift) if shift > 0 else (pos >> -shift) 
        pos &= ~board_end_mask
        pos &= ALL_ACTIVE_BITBOARD
        if pos == 0 or (pos & own_color_bitboard) != 0: # Outside of board or at pwn piece
            break
        elif pos & opposing_color_bitboard:
            moves |= pos 
            break
        else:
            moves |= pos
    return moves

@lru_cache
def get_bishop_psuedo_legal_moves(start_bitboard:int, own_color_bitboard:int, opposing_color_bitboard:int):
    directions = [
        (9, RANK_A_BITBOARD | FILE_1_BITBOARD),   # North-East (left-shift by 9 bits)
        (7, RANK_H_BITBOARD | FILE_1_BITBOARD),   # North-West (left-shift by 7 bits)
        (-9, RANK_H_BITBOARD | FILE_8_BITBOARD),  # South-West (right-shift by 9 bits)
        (-7, RANK_A_BITBOARD | FILE_8_BITBOARD)   # South-East (right-shift by 7 bits)
    ]

    end_bitboard = 0
    for shift, board_end_mask in directions:
        end_bitboard |= slide_moves(start_bitboard, board_end_mask, own_color_bitboard, opposing_color_bitboard, shift)

    return end_bitboard

@lru_cache
def get_rook_psuedo_legal_moves(start_bitboard:int, own_color_bitboard:int, opposing_color_bitboard:int):
    directions = [
        (8,FILE_1_BITBOARD),   # North (left-shift by 8 bits)
        (1,RANK_A_BITBOARD),   # East (left-shift by 1 bits)
        (-8,FILE_8_BITBOARD),  # South (right-shift by 8 bits)
        (-1,RANK_H_BITBOARD)   # West (right-shift by 1 bits))
    ]

    end_bitboard = 0
    for shift, board_end_mask in directions:
        end_bitboard |= slide_moves(start_bitboard, board_end_mask, own_color_bitboard, opposing_color_bitboard, shift)

    return end_bitboard

@lru_cache
def get_queen_psuedo_legal_moves(start_bitboard:int, own_color_bitboard:int, opposing_color_bitboard:int):
    end_bitboard = get_bishop_psuedo_legal_moves(start_bitboard, own_color_bitboard, opposing_color_bitboard) | get_rook_psuedo_legal_moves(start_bitboard, own_color_bitboard, opposing_color_bitboard)
    return end_bitboard

@lru_cache
def get_king_psuedo_legal_moves(start_bitboard:int, own_color_bitboard:int, castling_bitboard:int) -> int:
    end_bitboard = (
        (start_bitboard << 1) & ~RANK_A_BITBOARD | # East
        (start_bitboard << 7) & ~(FILE_1_BITBOARD | RANK_H_BITBOARD)| # North - west
        (start_bitboard << 8) & ~FILE_1_BITBOARD | # North
        (start_bitboard << 9) & ~(FILE_1_BITBOARD | RANK_A_BITBOARD) |# North - east
        (start_bitboard >> 1) & ~RANK_H_BITBOARD | # west
        (start_bitboard >> 7) & ~(FILE_8_BITBOARD | RANK_A_BITBOARD) |# south - east
        (start_bitboard >> 8) & ~FILE_8_BITBOARD | # south
        (start_bitboard >> 9) & ~RANK_H_BITBOARD # south - west
    )
    end_bitboard &= ALL_ACTIVE_BITBOARD
    end_bitboard &= ~own_color_bitboard
    
    end_bitboard |= castling_bitboard
    return end_bitboard