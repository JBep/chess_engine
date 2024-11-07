import logging
from typing import List, Tuple

from src.constants import BOARD_START_IDX
from src.utils import get_king_squares, get_knight_squares

def king_in_check(grid: List[List[int]], color: int):
    king_row, king_col = get_king_pos(grid, color)
    return count_attackers(grid, (king_row, king_col), color*-1)
    
def count_attackers(grid: List[List[int]], square: Tuple[int], color: int) -> int:
    """Counts attackers of player [color] that attacks a specific square"""
    row, col = square
    attacking_pieces = 0
    diagonal_attackers = [3,5] # Pawns & king handled separately
    straight_attackers = [4,5]
    
    # King
    for king_square in get_king_squares(square):
        king_row, king_col = king_square
        if grid[king_row][king_col]*color == 6:
            attacking_pieces +=1
    
    # Pawns
    pawn_squares = [(row+color,col-color),(row+color,col+color)]
    for pawn_square in pawn_squares:
        pawn_row, pawn_col = pawn_square
        if grid[pawn_row][pawn_col]*color == 1:
            attacking_pieces +=1
                
    # Diagonals
    for row_increment, col_increment in zip([1,1,-1,-1],[1,-1,1,-1]):
        row_temp = row
        col_temp = col
        cur_selection = 0
        while cur_selection != 99:
            row_temp += row_increment
            col_temp += col_increment
            cur_selection = grid[row_temp][col_temp]
            if cur_selection != 0:
                if cur_selection*color in diagonal_attackers:
                    attacking_pieces += 1 
                break
            
    # Verticals
    for increment in [1,-1]:
        row_temp = row
        cur_selection = 0
        while cur_selection != 99:
            row_temp += increment
            cur_selection = grid[row_temp][col]
            if cur_selection != 0:
                if cur_selection*color in straight_attackers:
                    attacking_pieces += 1 
                break

    # Horizontals
    for increment in [1,-1]:
        col_temp = col
        cur_selection = 0
        while cur_selection != 99:
            col_temp += increment
            cur_selection = grid[row][col_temp]
            if cur_selection != 0:
                if cur_selection*color in straight_attackers:
                    attacking_pieces += 1 
                break
            
    # Knights
    for knight_square in get_knight_squares(square):
        row, col = knight_square
        if grid[row][col]*color == 2: 
                attacking_pieces += 1 

    return attacking_pieces
    
def get_king_pos(grid: List[List[int]], color: int):
    """White = 1, Black = -1"""
    
    for row in range(BOARD_START_IDX, BOARD_START_IDX+8):
        for col in range(BOARD_START_IDX, BOARD_START_IDX+8):
            if grid[row][col] == 6*color:
                return row, col
    else:
        for rank in grid:
            logging.log(level = logging.DEBUG, msg = rank)
        logging.log(level = logging.DEBUG, msg = f"Looking for {color*6}")
        raise ValueError("This game should be over, there's no king...")
            
