from typing import List


def activate_position(bitboard:int, position: int) -> int:
    # Creates a mask with 0's everywhere except in position, then does bitwise or.
    return bitboard | (1 << position)

def activate_positions(bitboard:int, positions: List[int]):
    for pos in positions:
        bitboard = activate_position(bitboard, pos)
    return bitboard

def is_active(bitboard:int, position: int) -> bool:
    # Creates a mask with 0's everywhere except in position, then does bitwise and. If result is non-zero, position is active.
    return (bitboard & (1 << position)) != 0

def deactivate_position(bitboard:int, position: int)-> int:
    # Creates a mask with 1's everywhere except in position, then does bitwise and.
    return bitboard & ~(1 << position)

def deactivate_positions(bitboard:int, positions: List[int]):
    for pos in positions:
        bitboard = deactivate_position(bitboard, pos)
    return bitboard

def bitboard_to_str(bitboard:int) -> str:
    return bin(bitboard)[2:]

def get_active_positions(bitboard:int) -> List[int]:
    active_positions = []
    position = 0
    while bitboard:
        if bitboard & 1:
            active_positions.append(position)
        bitboard >>= 1 #Shift bits to check the next
        position += 1
    return active_positions
    
def index_to_chess_notation(idx:int) -> str:
    ranks = [1,2,3,4,5,6,7,8]
    files = ['a','b','c','d','e','f','g','h']
    return f"{files[idx%8]}{ranks[idx//8]}"