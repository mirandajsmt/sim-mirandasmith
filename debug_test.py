from tests.test_helpers import generate_fig4_board
from player2 import Player2
from consts import Color

miniboard = generate_fig4_board("b")
allowed = Player2.get_allowed_moves(Color.P2, miniboard.board)
print("Allowed moves:", allowed)

# Test the smaller set
small_set = {(0, 2), (0, 4)}
print("\nTesting set {(0,2), (0,4)}:")
for move in allowed:
    if move not in small_set:
        extended = small_set | {move}
        is_allowed = Player2.is_allowed_set(Color.P2, extended, miniboard.board)
        print(f"  Can add {move}? {is_allowed}")

# Test the larger set  
large_set = {(0, 1), (0, 3), (0, 4)}
print("\nTesting set {(0,1), (0,3), (0,4)}:")
for move in allowed:
    if move not in large_set:
        extended = large_set | {move}
        is_allowed = Player2.is_allowed_set(Color.P2, extended, miniboard.board)
        print(f"  Can add {move}? {is_allowed}")