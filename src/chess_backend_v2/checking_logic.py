from functools import lru_cache
from typing import Iterable
from src.chess_backend_v2.psuedo_legal_moves import get_king_psuedo_legal_moves, get_knight_psuedo_legal_moves
from src.chess_backend_v2.piece import ColorEnum, Piece, PieceTypeEnum
from src.chess_backend_v2.bitboard_constants import ALL_ACTIVE_BITBOARD, FILE_A_BITBOARD, FILE_H_BITBOARD

def king_is_in_check(pieces: Iterable[Piece], color: ColorEnum):
        square, opponent_pawns, opponent_knights, opponent_bishops, opponent_rooks, opponent_queens, opponent_king, all_pieces = 0,0,0,0,0,0,0,0
        for piece in pieces:
            all_pieces |= piece.location
            if piece.color != color:
                if piece.type == PieceTypeEnum.PAWN:
                    opponent_pawns |= piece.location
                elif piece.type == PieceTypeEnum.KNIGHT:
                    opponent_knights |= piece.location
                elif piece.type == PieceTypeEnum.BISHOP:
                    opponent_bishops |= piece.location
                elif piece.type in [PieceTypeEnum.KINGSIDE_ROOK, PieceTypeEnum.QUEENSIDE_ROOK]:
                    opponent_rooks |= piece.location
                elif piece.type == PieceTypeEnum.QUEEN:
                    opponent_queens |= piece.location
                elif piece.type == PieceTypeEnum.KING:
                    opponent_king |= piece.location
            else:
                if piece.type == PieceTypeEnum.KING:
                    square |= piece.location
        
        return _square_is_attacked(
            square=square,
            opponent_pawns=opponent_pawns,
            opponent_knights=opponent_knights,
            opponent_bishops=opponent_bishops,
            opponent_rooks=opponent_rooks,
            opponent_queens=opponent_queens,
            opponent_king=opponent_king,
            all_pieces=all_pieces,
            color=color
        )
  
def squares_are_attacked(squares:int, pieces: Iterable[Piece], color: ColorEnum):
    while squares:
        lsb = squares & -squares  # Isolate the least significant bit (LSB)
        position = (lsb).bit_length() - 1  # Find the index of the LSB (0-based)
        square_attacked = square_is_attacked(position, pieces, color)
        if square_attacked:
            return True
        squares &= squares - 1  # Clear the least significant bit
    return False

def square_is_attacked(square: int, pieces: Iterable[Piece], color: ColorEnum): 
        opponent_pawns, opponent_knights, opponent_bishops, opponent_rooks, opponent_queens, opponent_king, all_pieces = 0,0,0,0,0,0,0
        for piece in pieces:
            all_pieces |= piece.location
            if piece.color != color:
                if piece.type == PieceTypeEnum.PAWN:
                    opponent_pawns |= piece.location
                elif piece.type == PieceTypeEnum.KNIGHT:
                    opponent_knights |= piece.location
                elif piece.type == PieceTypeEnum.BISHOP:
                    opponent_bishops |= piece.location
                elif piece.type in [PieceTypeEnum.KINGSIDE_ROOK, PieceTypeEnum.QUEENSIDE_ROOK]:
                    opponent_rooks |= piece.location
                elif piece.type == PieceTypeEnum.QUEEN:
                    opponent_queens |= piece.location
                elif piece.type == PieceTypeEnum.KING:
                    opponent_king |= piece.location
        
        return _square_is_attacked(
            square=square,
            opponent_pawns=opponent_pawns,
            opponent_knights=opponent_knights,
            opponent_bishops=opponent_bishops,
            opponent_rooks=opponent_rooks,
            opponent_queens=opponent_queens,
            opponent_king=opponent_king,
            all_pieces=all_pieces,
            color=color
        )
        
@lru_cache
def _square_is_attacked(square:int, opponent_pawns:int, opponent_knights:int, opponent_bishops:int,
                     opponent_rooks:int, opponent_queens:int, opponent_king:int, all_pieces:int, 
                     color: ColorEnum):
    

    # Knight Attacks
    knight_attacks = get_knight_psuedo_legal_moves(
        start_bitboard = square,
        own_color_bitboard = 0
    )
    if opponent_knights & knight_attacks:
        return True
    
    def shift(bitboard, direction):
        if direction == 'northwest':
            return (bitboard << 7) & ~(FILE_H_BITBOARD) & (ALL_ACTIVE_BITBOARD)
        elif direction == 'northeast':
            return (bitboard << 9) & ~(FILE_A_BITBOARD) & (ALL_ACTIVE_BITBOARD)
        elif direction == 'southwest':
            return (bitboard >> 9) & ~(FILE_H_BITBOARD)
        elif direction == 'southeast':
            return (bitboard >> 7) & ~(FILE_A_BITBOARD)
        elif direction == 'north':
            return (bitboard << 8) & (ALL_ACTIVE_BITBOARD)
        elif direction == 'south':
            return (bitboard >> 8)
        elif direction == 'east':
            return (bitboard << 1) & (FILE_A_BITBOARD) & (ALL_ACTIVE_BITBOARD)
        elif direction == 'west':
            return (bitboard >> 1) & ~(FILE_H_BITBOARD)
        

    # King Attacks (used for adjacent squares)
    king_attacks = get_king_psuedo_legal_moves(square, 0, 0)
    if opponent_king & king_attacks:
        return True

    # Pawn Attacks
    if color == ColorEnum.WHITE:
        pawn_attacks = shift(square, 'northwest') | shift(square, 'northeast')
    else:
        pawn_attacks = shift(square, 'southwest') | shift(square, 'southeast')

    if opponent_pawns & pawn_attacks:
        return True

    # Sliding Pieces (Bishops/Queens)
    directions = ['northeast', 'northwest', 'southeast', 'southwest']
    for direction in directions:
        attack_path = shift(square, direction)
        while attack_path:
            if attack_path & all_pieces:
                if attack_path & (opponent_bishops | opponent_queens):
                    return True
                break
            attack_path = shift(attack_path, direction)

    # Sliding Pieces (Rooks/Queens)
    directions = ['north', 'south', 'east', 'west']
    for direction in directions:
        attack_path = shift(square, direction)
        while attack_path:
            if attack_path & all_pieces:
                if attack_path & (opponent_rooks | opponent_queens):
                    return True
                break
            attack_path = shift(attack_path, direction)

    return False