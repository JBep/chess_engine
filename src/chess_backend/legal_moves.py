from typing import List, Tuple, Set
from src.constants import BOARD_START_IDX
from src.chess_backend.move import Move, MoveTypeEnum
from src.chess_backend.chess_utils import count_attackers, get_king_squares, get_knight_squares, king_in_check



#@log_execution_time
def legal_moves_pawn(grid:List[List[int]], color: int, start_square: Tuple[int], enpassant_pos: Tuple[int]| None) -> Set[Move]:
    start_row, start_col = start_square
    first_row = BOARD_START_IDX+int((5/2)*color + 7/2) # 1 => 6, -1 => 1 
    legal_moves = set()
    
    # Normal pawn moves
    if grid[start_row-color][start_col] == 0:
        move_type = MoveTypeEnum.NORMAL
        if start_row-color == BOARD_START_IDX or start_row-color == BOARD_START_IDX + 7:
            move_type = MoveTypeEnum.PAWN_PROMOTION
        legal_moves.add(Move(
                start_square = start_square,
                end_square = (start_row-color, start_col),
                piece = color,
                move_type = move_type
            ))
        if start_row == first_row and grid[start_row-(color*2)][start_col] == 0:
            legal_moves.add(Move(
                start_square = start_square,
                end_square = (start_row-(color*2), start_col),
                piece = color,
                move_type = MoveTypeEnum.PAWN_DOUBLE_STEP
            ))
            
    # Captures & Enpassant
    left_col = start_col-1
    right_col = start_col+1
    
    for col in [left_col, right_col]:
        if grid[start_row-color][col] != 99: 
            if grid[start_row-color][col]*color < 0: # Opponent present
                legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (start_row-color, col),
                        piece = color,
                        move_type = MoveTypeEnum.CAPTURE,
                        captured_piece = grid[start_row-color][col]
                    ))    
            elif enpassant_pos and enpassant_pos == (start_row-color, col):
                legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (start_row-color, col),
                        piece = color,
                        move_type = MoveTypeEnum.ENPASSANT,
                        enpassant_capture_square = (start_row, col)
                        
                    ))   
    
    return legal_moves

#@log_execution_time
def legal_moves_knight(grid:List[List[int]], color: int, start_square: Tuple[int]) -> Set[Move]:
    legal_moves = set()

    for square in get_knight_squares(start_square):
        row, col = square
        piece = grid[row][col]
        if piece != 99  and piece*color <=0: 
            if piece *color < 0:
                legal_moves.add(Move(
                    start_square=start_square,
                    end_square = square,
                    piece = 2*color,
                    move_type = MoveTypeEnum.CAPTURE,
                    captured_piece= piece
                ))
            else:
                legal_moves.add(Move(
                    start_square=start_square,
                    end_square = square,
                    piece = 2*color,
                    move_type = MoveTypeEnum.NORMAL
                ))
             
                
        
    return legal_moves

#@log_execution_time
def legal_moves_bishop(grid:List[List[int]], color: int, start_square: Tuple[int]) -> Set[Move]:
    legal_moves = set()
    start_row, start_col = start_square
    
    for row_increment, col_increment in zip([1,1,-1,-1],[1,-1,1,-1]):
        cur_row = start_row + row_increment
        cur_col = start_col + col_increment
        cur_selection = grid[cur_row][cur_col]
        while cur_selection != 99:
            if cur_selection*color <= 0:
                if cur_selection *color < 0:
                    legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (cur_row, cur_col),
                        piece = 3*color,
                        move_type = MoveTypeEnum.CAPTURE,
                        captured_piece= cur_selection
                    ))
                else:
                    legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (cur_row, cur_col),
                        piece = 3*color,
                        move_type = MoveTypeEnum.NORMAL
                    ))
                
                if cur_selection*color < 0:
                    break
            else:
                break  # Friendly piece
            cur_row = cur_row + row_increment
            cur_col = cur_col + col_increment
            cur_selection = grid[cur_row][cur_col]
        
    return legal_moves

#@log_execution_time
def legal_moves_rook(grid:List[List[int]], color: int, start_square: Tuple[int]) -> Set[Move]:
    legal_moves = set()
    start_row, start_col = start_square
    
    for increment in [1,-1]:
        # Verticals
        cur_row = start_row + increment
        cur_selection = grid[cur_row][start_col]
        while cur_selection != 99:
            if cur_selection*color <= 0:
                if cur_selection *color < 0:
                    legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (cur_row, start_col),
                        piece = 4*color,
                        move_type = MoveTypeEnum.CAPTURE,
                        captured_piece=cur_selection
                    ))
                else:
                    legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (cur_row, start_col),
                        piece = 4*color,
                        move_type = MoveTypeEnum.NORMAL
                        ))
                if cur_selection*color < 0:
                    break
            else:
                break # Friendly piece          
            cur_row = cur_row + increment
            cur_selection = grid[cur_row][start_col]
        
        # Horizontals
        cur_col = start_col - increment
        cur_selection = grid[start_row][cur_col]
        while cur_selection != 99:
            if cur_selection*color <= 0:
                if cur_selection *color < 0:
                    legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (cur_row, start_col),
                        piece = 4*color,
                        move_type = MoveTypeEnum.CAPTURE,
                        captured_piece=cur_selection
                    ))
                else:
                    legal_moves.add(Move(
                        start_square = start_square,
                        end_square = (cur_row, start_col),
                        piece = 4*color,
                        move_type = MoveTypeEnum.NORMAL
                        ))
                if cur_selection*color < 0:
                    break
            else:
                break # Friendly piece    
            cur_col = cur_col - increment
            cur_selection = grid[start_row][cur_col]
       
    return legal_moves

#@log_execution_time
def legal_moves_queen(grid:List[List[int]], color: int, start_square: Tuple[int]) -> Set[Move]:
    legal_moves = set()
    
    for move in legal_moves_bishop(grid, color, start_square):
        move.piece = 5*color
        legal_moves.add(move)
        
    for move in legal_moves_rook(grid, color, start_square):
        move.piece = 5*color
        legal_moves.add(move)
    
    return legal_moves

#@log_execution_time
def legal_moves_king(grid: List[List[int]], color: int, start_square: Tuple[int], kingside_castling_possible: bool, queenside_castling_possible: bool) -> set:
    potential_squares = get_king_squares(start_square)
    
    legal_moves = set()
    for square in potential_squares:
        row, col = square
        selection = grid[row][col]
        if selection != 99 and selection*color <= 0:
            if selection *color < 0:
                legal_moves.add(Move(
                    start_square = start_square,
                    end_square =square,
                    piece = 6*color,
                    move_type = MoveTypeEnum.CAPTURE,
                    captured_piece=selection
                ))
            else:
                legal_moves.add(Move(
                    start_square = start_square,
                    end_square =square,
                    piece = 6*color,
                    move_type = MoveTypeEnum.NORMAL
                    ))
    
    # Castling
    # Rules are: 
    # 1. King or rook hasn't move (checked by the "castling_possible")
    # 2. No pieces between rook and king
    # 3. King not in check
    # 4. King does not pass throguh or finish on a square attacked by enemy piece
    if not king_in_check(grid, color): # TODO add that king cannot pass through check
        king_row = BOARD_START_IDX+int(7/2*color + 7/2)
        if kingside_castling_possible:
            if grid[king_row][BOARD_START_IDX+5] == 0 and grid[king_row][BOARD_START_IDX+6] == 0 and count_attackers(grid, (king_row, BOARD_START_IDX+5),color*-1) == 0:
                legal_moves.add(Move(
                    start_square = start_square,
                    end_square = (king_row, BOARD_START_IDX+6),
                    piece = 6*color,
                    move_type = MoveTypeEnum.KINGSIDE_CASTLING,
                    rook_start_square = (king_row, BOARD_START_IDX+7),
                    rook_end_square = (king_row, BOARD_START_IDX+5)
                ))
                
        if queenside_castling_possible:
            if grid[king_row][BOARD_START_IDX+1] == 0 and grid[king_row][BOARD_START_IDX+2] == grid[king_row][BOARD_START_IDX+3] == 0 and count_attackers(grid, (king_row, BOARD_START_IDX+3),color*-1) == 0:
                legal_moves.add(Move(
                    start_square = start_square,
                    end_square = (king_row, BOARD_START_IDX+2),
                    piece = 6*color,
                    move_type = MoveTypeEnum.QUEENSIDE_CASTLING,
                    rook_start_square = (king_row, BOARD_START_IDX),
                    rook_end_square = (king_row, BOARD_START_IDX+3)
                ))
    
    return legal_moves