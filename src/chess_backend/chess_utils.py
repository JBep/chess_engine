import logging
from typing import List, Tuple
from src.constants import BOARD_START_IDX, HEIGHT, SQUARE_SIZE, TEXT_AREA_WIDTH, WIDTH, IMAGE_DIR

def algebraic_move(move):
    move_algebraic = coord_to_algebraic(move.end_square)
    piece = piece_to_algebraic(move.piece)

    if move.captured_piece:
        capture = 'x'
    else:
        capture = ''
    return f"{piece}{capture}{move_algebraic}"

def algebraic(move_record):
    if move_record.game_state.king_in_check[move_record.game_state.turn]:
        suffix = "+"
        if move_record.game_state.game_is_over:
            suffix = "#"
    else:
        suffix = ""
        
    note = f"{algebraic_move(move_record.move)}{suffix}"
    return note

def coord_to_algebraic(square) -> str:
    """Assumes a 8x8 grid, i.e., (0,0) -> a8 """
    row, col = square
    files =     ['a','b','c','d','e','f','g','h']
    file = files[col-BOARD_START_IDX]
    rank = 8-(row-BOARD_START_IDX) 
    return f"{file}{rank}"

def algebraic_to_coord(algebraic) -> Tuple[int]:
    """Assumes a 8x8 grid, i.e., a8 -> (0,0) """
    file, rank = algebraic
    files =     ['a','b','c','d','e','f','g','h']
    col = files.index(file)
    row = 8-int(rank)
    return row, col
    
def piece_to_algebraic(piece:int) -> str:
    notation = ['','N','B','R','Q','K']
    return notation[abs(piece)-1]

def compute_material_score(grid, color:int):
    scores = [0,1,3,3,5,9,0] # King is 0
    score = 0
    for rank in grid:
        for piece in rank:
            if piece != 99 and piece*color > 0:
                score += scores[piece*color]
    return score

def get_knight_squares(square: Tuple[int]) -> List[Tuple[int]]:
    row, col = square
    return {
        (-1+row,2+col),
        (-1+row,-2+col),
        (1+row,2+col),
        (1+row,-2+col),
        (2+row,1+col),
        (2+row,-1+col),
        (-2+row,1+col),
        (-2+row,-1+col)
    }

def get_king_squares(square: Tuple[int]):
    squares = []
    start_row, start_col = square
    for i in [1, -1]:
        squares.extend([
            (start_row + i, start_col),
            (start_row + i, start_col + i),
            (start_row + i, start_col - i),
            (start_row, start_col + i)
        ]) 
    return squares

def king_in_check(grid: List[List[int]], color: int):
    king_row, king_col = get_king_pos(grid, color)
    return count_attackers(grid, (king_row, king_col), color*-1)
    
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



def draw_by_insufficient_material(grid: List[List[int]]):
    #king vs king
    #king and bishop vs king
    #king and knight vs king
    #king and bishop vs king and bishop, bishops same color.
    pass