

from src.chess_backend_v2.bitboard_constants import BLACK_BITBOARD_STARTING_POSITION, WHITE_BITBOARD_STARTING_POSITION
from src.bitboard_utils import activate_position, activate_positions, deactivate_position, deactivate_positions, get_active_positions
from chess_backend_v2.psuedo_legal_moves import get_bishop_psuedo_legal_moves, get_king_psuedo_legal_moves, get_knight_psuedo_legal_moves, get_pawn_psuedo_legal_moves, get_rook_psuedo_legal_moves
from src.chess_backend_v2.piece import ColorEnum
def test_result_string(test: str, moves_bitboard:int, expected_bitboard:int) -> str:
    return f"""{test} failed:
    Got {moves_bitboard}: {get_active_positions(moves_bitboard)}
    Expected {expected_bitboard}: {get_active_positions(expected_bitboard)}"""
    

def test_get_pawn_psuedo_legal_moves():
    ## Test 1: a2
    w_bitboard = WHITE_BITBOARD_STARTING_POSITION   # Bits in position 0-15 are active. 
    b_bitboard = BLACK_BITBOARD_STARTING_POSITION 
    moves_bitboard = get_pawn_psuedo_legal_moves(activate_position(0,8),w_bitboard, b_bitboard,ColorEnum.WHITE, False) # b2
    expected_bitboard = activate_positions(0,[16,24]) #b3. b4 
    assert moves_bitboard == expected_bitboard, test_result_string("Pawn test 1",moves_bitboard, expected_bitboard)
    
    ## Test 2: Black pawn a7
    w_bitboard = WHITE_BITBOARD_STARTING_POSITION   # Bits in position 0-15 are active. 
    b_bitboard = BLACK_BITBOARD_STARTING_POSITION 
    moves_bitboard = get_pawn_psuedo_legal_moves(activate_position(0,48),w_bitboard, b_bitboard,ColorEnum.BLACK, False)
    expected_bitboard = activate_positions(0,[40,32])
    assert moves_bitboard == expected_bitboard, test_result_string("Pawn test 2",moves_bitboard, expected_bitboard)
    
    ## Test 3: White pawn, d5 Captures available
    w_bitboard = WHITE_BITBOARD_STARTING_POSITION   # Bits in position 0-15 are active. 
    b_bitboard = BLACK_BITBOARD_STARTING_POSITION 
    w_bitboard = activate_position(w_bitboard, 27)
    w_bitboard = deactivate_position(w_bitboard, 1)
    
    b_bitboard = activate_position(b_bitboard, 34) # This should be captureable
    b_bitboard = deactivate_position(b_bitboard, 50)
    
    moves_bitboard = get_pawn_psuedo_legal_moves(activate_position(0,27),w_bitboard, b_bitboard,ColorEnum.WHITE, True)
    expected_bitboard = activate_positions(0,[34,35])
    assert moves_bitboard == expected_bitboard, test_result_string("Pawn test 3",moves_bitboard, expected_bitboard)    
    
    ## Test 4: Blackl pawn d7, captures available
    w_bitboard = WHITE_BITBOARD_STARTING_POSITION   # Bits in position 0-15 are active. 
    b_bitboard = BLACK_BITBOARD_STARTING_POSITION 
    w_bitboard = activate_positions(w_bitboard, [42,44])
    w_bitboard = deactivate_positions(w_bitboard, [11,12])
    
    
    moves_bitboard = get_pawn_psuedo_legal_moves(activate_position(0,51),w_bitboard, b_bitboard,ColorEnum.BLACK, False)
    expected_bitboard = activate_positions(0,[42,43,44,35])
    assert moves_bitboard == expected_bitboard, test_result_string("Pawn test 3",moves_bitboard, expected_bitboard)    


def test_get_knight_psuedo_legal_moves():
    # White knight at d4
    w_bitboard  = activate_position(WHITE_BITBOARD_STARTING_POSITION,27)
    w_bitboard  = deactivate_position(w_bitboard,1)
    moves_bitboard = get_knight_psuedo_legal_moves(activate_position(0,27), w_bitboard)
    expected_bitboard = activate_positions(0,[17,21,33,37,42,44])
    assert moves_bitboard == expected_bitboard, test_result_string("Knight test 1",moves_bitboard, expected_bitboard)    
    
    # Black knight b8
    moves_bitboard = get_knight_psuedo_legal_moves(activate_position(0,57), BLACK_BITBOARD_STARTING_POSITION)
    expected_bitboard = activate_positions(0,[40,42])
    assert moves_bitboard == expected_bitboard, test_result_string("Knight test 2",moves_bitboard, expected_bitboard)
    
    # Black knight h7
    moves_bitboard = get_knight_psuedo_legal_moves(activate_position(0,7), BLACK_BITBOARD_STARTING_POSITION )
    expected_bitboard = activate_positions(0,[13,22])
    assert moves_bitboard == expected_bitboard, test_result_string("Knight test 3",moves_bitboard, expected_bitboard)   
    
    
    # Black knight h7, other black piece at f2
    moves_bitboard = get_knight_psuedo_legal_moves(activate_position(0,7), activate_position(BLACK_BITBOARD_STARTING_POSITION,13))
    expected_bitboard = activate_position(0,22)
    assert moves_bitboard == expected_bitboard, test_result_string("Knight test 4",moves_bitboard, expected_bitboard)     
    
def test_get_bishop_psuedo_legal_moves():
    moves_bitboard = get_bishop_psuedo_legal_moves(activate_position(0,2), WHITE_BITBOARD_STARTING_POSITION, BLACK_BITBOARD_STARTING_POSITION)
    expected_bitboard = 0
    assert moves_bitboard == expected_bitboard, test_result_string("Bishop test 1",moves_bitboard, expected_bitboard)    
    
    moves_bitboard = get_bishop_psuedo_legal_moves(activate_position(0,27), activate_position(WHITE_BITBOARD_STARTING_POSITION,27), BLACK_BITBOARD_STARTING_POSITION)
    expected_bitboard = activate_positions(0,[18,20,34,41,48,36,45,54])
    assert moves_bitboard == expected_bitboard, test_result_string("Bishop test 2",moves_bitboard, expected_bitboard)  
    
    b_bitboard = activate_positions(BLACK_BITBOARD_STARTING_POSITION,[32,42])
    b_bitboard = deactivate_positions(b_bitboard,[57,50])
    moves_bitboard = get_bishop_psuedo_legal_moves(activate_position(0,32), b_bitboard, WHITE_BITBOARD_STARTING_POSITION)
    expected_bitboard = activate_positions(0,[41,50,25,18,11])
    assert moves_bitboard == expected_bitboard, test_result_string("Bishop test 3",moves_bitboard, expected_bitboard)  
    
def test_get_rook_psuedo_legal_moves():
    moves_bitboard = get_rook_psuedo_legal_moves(activate_position(0,0), WHITE_BITBOARD_STARTING_POSITION, BLACK_BITBOARD_STARTING_POSITION)
    expected_bitboard = 0
    assert moves_bitboard == expected_bitboard, test_result_string("Rook test 1",moves_bitboard, expected_bitboard)    
    
    w_bitboard = activate_position(WHITE_BITBOARD_STARTING_POSITION,27)
    w_bitboard = deactivate_position(w_bitboard, 7)
    moves_bitboard = get_rook_psuedo_legal_moves(activate_position(0,27), w_bitboard, BLACK_BITBOARD_STARTING_POSITION)
    expected_bitboard = activate_positions(0,[24,25,26,28,29,30,31,19,35,43,51])
    assert moves_bitboard == expected_bitboard, test_result_string("Rook test 1",moves_bitboard, expected_bitboard)    
    
def test_get_king_psuedo_legal_moves():
    moves_bitboard = get_king_psuedo_legal_moves(activate_position(0,4), WHITE_BITBOARD_STARTING_POSITION)
    expected_bitboard = 0
    assert moves_bitboard == expected_bitboard, test_result_string("King test 1",moves_bitboard, expected_bitboard)    
    
    w_bitboard = activate_position(WHITE_BITBOARD_STARTING_POSITION,27)
    w_bitboard = deactivate_position(w_bitboard, 3)
    moves_bitboard = get_king_psuedo_legal_moves(activate_position(0,27), w_bitboard)
    expected_bitboard = activate_positions(0,[18,19,20,26,28,34,35,36])
    assert moves_bitboard == expected_bitboard, test_result_string("King test 1",moves_bitboard, expected_bitboard)    
    
    w_bitboard = activate_position(WHITE_BITBOARD_STARTING_POSITION,31)
    w_bitboard = deactivate_position(w_bitboard, 3)
    moves_bitboard = get_king_psuedo_legal_moves(activate_position(0,31), w_bitboard)
    expected_bitboard = activate_positions(0,[22,23,30,38,39])
    assert moves_bitboard == expected_bitboard, test_result_string("King test 1",moves_bitboard, expected_bitboard)    
    