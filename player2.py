from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES
from itertools import combinations


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim
    """

    @staticmethod
    def get_move(board: Board) -> Edge:
        """
        Return a possible move for the second player (blue) that follows the optimal strategy laid out in the handout,
        given the input board state. If multiple moves are viable, this method can return any of them.
        """
        moves = Player2.get_allowed_moves(Color.P2, board) # get all available moves
        if not moves:
            raise ValueError("No valid moves available for Player 2")
        
        safe_moves = []
        for move in moves:
            # Simulate the move
            new_board = [row[:] for row in board]  # Deep copy of the board
            new_board[move[0]][move[1]] = Color.P2
            new_board[move[1]][move[0]] = Color.P2
            
            # Check if this move creates a miniboard for Player 1
            if Player2.get_miniboard(new_board) is None:
                safe_moves.append(move)
        return safe_moves[0] if safe_moves else moves[0]
        

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        n = len(board)
        for i, j, k in combinations(range(n), 3):
            c1 = board[i][j]
            c2 = board[i][k]
            c3 = board[j][k]

            # only consider edges that are colored
            if c1 in (Color.P1, Color.P2) and c1 == c2 == c3:
                # Create a 3x3 miniboard for these nodes
                nodes = [i, j, k]
                miniboard = [[board[a][b] for b in nodes] for a in nodes]
                return miniboard
        return None

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """
        allowed_moves = Player2.get_allowed_moves(player, board)
        maximal_sets = set()

        # Try starting from each allowed move
        for start_move in allowed_moves:
            current_set = {start_move}
            remaining_moves = [m for m in allowed_moves if m != start_move]

            changed = True
            while changed:
                changed = False
                for move in remaining_moves:
                    test_set = current_set | {move}
                    if Player2.is_allowed_set(player, test_set, board):
                        current_set.add(move)
                        changed = True
                # Remove already added moves from remaining
                remaining_moves = [m for m in remaining_moves if m not in current_set]

            # Add the maximal set as frozenset
            maximal_sets.add(frozenset(current_set))

        return maximal_sets

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.
        """
        allowed_moves = []
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                if board[i][j] == Color.UNCOLORED:
                    allowed_moves.append((i, j))
        return allowed_moves
