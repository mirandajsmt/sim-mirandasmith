from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES
from itertools import combinations


class GameBoard:
    """
    Game board manager class. Encapsulates behaviors concerning the state of the board.
    """

    def __init__(self):
        """
        Initialize `board` as the adjacency matrix for the starting board.
        Use `Color.NONE` for edges that do not exist, and `Color.UNCOLORED` for the other edges.
        """
        self.board : Board = [[Color.UNCOLORED for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
        for i in range(NUM_NODES):
            self.board[i][i] = Color.NONE

    def color_edge(self, edge: Edge, color: Color) -> None:
        """
        Update `board` to reflect coloring the given edge.
        """
        i, j = edge
        if i == j:
            raise ValueError('Cannot color a self-edge.')
        if self.board[i][j] == Color.NONE:
            raise ValueError(f"Edge {edge} does not exist.")
        if self.board[i][j] != Color.UNCOLORED:
            raise ValueError(f"Edge {edge} is already colored.")

        # Color both directions to maintain symmetry
        self.board[i][j] = color
        self.board[j][i] = color

    def get_winner(self) -> Color | None:
        """
        Return the color of the player that has won (Color.P1 or Color.P2).
        If the game is still in progress (no one has won yet), return None.
        """
        n = len(self.board)
        for i, j, k in combinations(range(n), 3):
            c1, c2, c3 = self.board[i][j], self.board[i][k], self.board[j][k]
            if c1 != Color.UNCOLORED and c1 == c2 == c3:
                # The player who formed this triangle loses,
                # so the other player wins.
                return Color.P1 if c1 == Color.P2 else Color.P2
        return None

    def __str__(self):
        """
        Formats the board as a string. Provided for your convenience while debugging.
        """
        string = ""
        for row in self.board:
            for item in row:
                string += "{edge:<10}".format(edge=item.name)
            string += "\n"
        return string
