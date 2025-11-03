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
        Return a possible move for the second player (blue) that follows the optimal strategy.
        Strategy:
        1. Select a miniboard M
        2. If only one P2-allowed move in M, select it
        3. Otherwise, select move in most maximal P2-allowed sets
        4. Otherwise, select move in most maximal P1-allowed sets
        """
        # Step 1: Get miniboard
        miniboard = Player2.get_miniboard(board)
        if miniboard is None:
            # No miniboard exists, just pick any allowed move
            moves = Player2.get_allowed_moves(Color.P2, board)
            return moves[0] if moves else None
        
        # Step 2: Get P2-allowed moves on the miniboard
        p2_moves = Player2.get_allowed_moves(Color.P2, miniboard)
        
        if len(p2_moves) == 1:
            return p2_moves[0]
        
        # Step 3: Find moves in most maximal P2-allowed sets
        p2_maximal_sets = Player2.get_maximal_allowed_sets(Color.P2, miniboard)
        move_counts_p2 = {}
        for move in p2_moves:
            count = sum(1 for s in p2_maximal_sets if move in s or (move[1], move[0]) in s)
            move_counts_p2[move] = count
        
        max_count_p2 = max(move_counts_p2.values())
        best_moves_p2 = [m for m, c in move_counts_p2.items() if c == max_count_p2]
        
        if len(best_moves_p2) == 1:
            return best_moves_p2[0]
        
        # Step 4: Find moves in most maximal P1-allowed sets
        p1_maximal_sets = Player2.get_maximal_allowed_sets(Color.P1, miniboard)
        move_counts_p1 = {}
        for move in best_moves_p2:
            count = sum(1 for s in p1_maximal_sets if move in s or (move[1], move[0]) in s)
            move_counts_p1[move] = count
        
        max_count_p1 = max(move_counts_p1.values())
        best_moves_p1 = [m for m, c in move_counts_p1.items() if c == max_count_p1]
        
        return best_moves_p1[0]

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state.
        A miniboard must:
        - Contain all colored edges (and their nodes)
        - Be complete (all nodes connected to each other)
        - Have at least one P2-allowed move
        - Be minimal (can't remove any node while satisfying above)
        
        Returns a full-sized board with excluded nodes set to Color.NONE
        """
        n = len(board)
        
        # Find all nodes involved in colored edges
        colored_nodes = set()
        for i in range(n):
            for j in range(i + 1, n):
                if board[i][j] in (Color.P1, Color.P2):
                    colored_nodes.add(i)
                    colored_nodes.add(j)
        
        # Try all subsets that contain colored nodes, starting from smallest
        for size in range(len(colored_nodes), n + 1):
            for nodes in combinations(range(n), size):
                nodes_set = set(nodes)
                
                # Must contain all colored nodes
                if not colored_nodes.issubset(nodes_set):
                    continue
                
                # Check if complete graph (all edges between nodes exist and aren't NONE)
                is_complete = True
                for i in nodes:
                    for j in nodes:
                        if i < j:
                            # Edge must not be NONE (removed from board)
                            if board[i][j] == Color.NONE:
                                is_complete = False
                                break
                    if not is_complete:
                        break
                
                if not is_complete:
                    continue
                
                # Check for at least one P2-allowed move
                has_p2_move = False
                for i in nodes:
                    for j in nodes:
                        if i < j and board[i][j] == Color.UNCOLORED:
                            # Check if this move doesn't create a P2 triangle
                            if Player2.is_allowed_set(Color.P2, {(i, j)}, board):
                                has_p2_move = True
                                break
                    if has_p2_move:
                        break
                
                if not has_p2_move:
                    continue
                
                # Check minimality: try removing each node
                is_minimal = True
                for node_to_remove in nodes:
                    smaller_nodes = [nd for nd in nodes if nd != node_to_remove]
                    smaller_set = set(smaller_nodes)
                    
                    # Check if smaller graph still satisfies all conditions
                    if not colored_nodes.issubset(smaller_set):
                        continue
                    
                    # Check completeness
                    still_complete = True
                    for i in smaller_nodes:
                        for j in smaller_nodes:
                            if i < j and board[i][j] == Color.NONE:
                                still_complete = False
                                break
                        if not still_complete:
                            break
                    
                    if not still_complete:
                        continue
                    
                    # Check for P2-allowed move
                    has_move = False
                    for i in smaller_nodes:
                        for j in smaller_nodes:
                            if i < j and board[i][j] == Color.UNCOLORED:
                                if Player2.is_allowed_set(Color.P2, {(i, j)}, board):
                                    has_move = True
                                    break
                        if has_move:
                            break
                    
                    if has_move:
                        # Smaller graph satisfies all conditions, not minimal
                        is_minimal = False
                        break
                
                if is_minimal:
                    # Create miniboard: copy board and set non-miniboard nodes to NONE
                    miniboard = [row[:] for row in board]
                    excluded_nodes = [i for i in range(n) if i not in nodes_set]
                    
                    for excluded in excluded_nodes:
                        # Set entire row and column to NONE
                        for j in range(n):
                            miniboard[excluded][j] = Color.NONE
                            miniboard[j][excluded] = Color.NONE
                    
                    return miniboard
        
        return None

    @staticmethod
    def is_allowed_set(player: Color, edge_set: set[Edge], board: Board) -> bool:
        """
        Return True if coloring all edges in edge_set for player
        does not create a monochromatic triangle.
        """
        n = len(board)
        # Create simulated board
        simulated = [row[:] for row in board]
        
        for edge in edge_set:
            i, j = edge
            simulated[i][j] = player
            simulated[j][i] = player
        
        # Check all possible triangles
        for a, b, c in combinations(range(n), 3):
            if (simulated[a][b] == simulated[b][c] == simulated[a][c] == player):
                return False
        
        return True

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return all distinct maximal allowed sets for the given player.
        A maximal allowed set is an allowed set that cannot be extended with any other allowed move.
        """
        allowed_moves = Player2.get_allowed_moves(player, board)
        
        if not allowed_moves:
            return set()
        
        # Normalize moves to avoid duplicates like (0,1) and (1,0)
        normalized_moves = []
        seen = set()
        for move in allowed_moves:
            normalized = tuple(sorted(move))
            if normalized not in seen:
                seen.add(normalized)
                normalized_moves.append(move)
        
        # Build all possible allowed sets
        all_allowed_sets = []
        
        for r in range(1, len(normalized_moves) + 1):
            for subset in combinations(normalized_moves, r):
                if Player2.is_allowed_set(player, set(subset), board):
                    all_allowed_sets.append(frozenset(subset))
        
        # Filter to only maximal sets: cannot add any more moves
        maximal_sets = []
        for candidate in all_allowed_sets:
            is_maximal = True
            # Try to add each move not in candidate
            for move in normalized_moves:
                if move not in candidate:
                    # Check if we can extend this set
                    extended = candidate | {move}
                    if Player2.is_allowed_set(player, set(extended), board):
                        is_maximal = False
                        break
            
            if is_maximal:
                maximal_sets.append(candidate)
        
        # Return only the maximal sets with the largest size
        if not maximal_sets:
            return set()
        
        max_size = max(len(s) for s in maximal_sets)
        return {s for s in maximal_sets if len(s) == max_size}

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return all distinct valid moves for the given player.
        A valid move is an uncolored edge that doesn't create a triangle.
        """
        n = len(board)
        allowed = []
        
        for i in range(n):
            for j in range(i + 1, n):
                if board[i][j] == Color.UNCOLORED:
                    # Check if coloring this edge creates a triangle
                    if Player2.is_allowed_set(player, {(i, j)}, board):
                        allowed.append((i, j))
        
        return allowed