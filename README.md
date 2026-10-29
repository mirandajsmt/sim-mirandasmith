# Sim: Optimal Strategy Implementation

## Overview

This project implements the game of **Sim**, a two-player graph-based game in which players take turns coloring edges between six vertices. The objective is to avoid forming a triangle consisting entirely of edges in a player's own color; the first player to complete such a triangle loses.

The project focuses on implementing an optimal strategy for Player 2, who can guarantee victory by following the game's winning strategy.

## Features

- **Game board representation:** Model the game state using an adjacency matrix.
- **Edge management:** Track edge colors and update the board as players make moves.
- **Triangle detection:** Determine whether a player has formed a monochromatic triangle.
- **Allowed move generation:** Identify moves that do not immediately cause a player to lose.
- **Miniboard identification:** Find minimal complete subgraphs that contain all colored edges and at least one allowed move for Player 2.
- **Optimal move selection:** Implement the prescribed strategy for Player 2 using maximal allowed sets.

## Algorithms and Data Structures

The implementation explores several graph-theoretic concepts:

- **Adjacency matrices:** Represent vertices, edges, and edge colors.
- **Graph traversal and subgraphs:** Identify valid miniboards within the current game state.
- **Combinatorial search:** Enumerate allowed moves and maximal allowed sets for each player.
- **Strategy optimization:** Select moves by considering their frequency across maximal allowed sets, applying successive tie-breaking rules to determine Player 2's move.

## Technologies

- Python 3
- Python standard library
- Pytest

## Project Structure

- `sim_board.py` — Manages the game board, edge coloring, and winner detection.
- `player2.py` — Implements the optimal strategy for Player 2.
- Additional files may provide interfaces, supporting game logic, and tests.

## Key Methods

The assignment centers on the following methods:

- `get_move(board)` — Selects an optimal move for Player 2.
- `get_miniboard(board)` — Identifies a valid miniboard for the current game state.
- `get_maximal_allowed_sets(...)` — Finds the distinct maximal allowed sets for a player.
- `get_allowed_moves(...)` — Returns the distinct moves that do not immediately cause a player to lose.

## Learning Objectives

This project provides experience with graph representations, combinatorial algorithms, constraint-based search, and strategic decision-making. It also emphasizes decomposing a complex algorithm into smaller methods with clearly defined responsibilities.

## References

- DSC 395T: Algorithms and Data Structures, Programming Assignment #4 — Sim.
