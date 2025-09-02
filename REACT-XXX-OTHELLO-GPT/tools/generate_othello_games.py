#!/usr/bin/env python3
"""
Generate valid Othello games.

This script generates valid Othello games and outputs them to a text file.
Each line in the output file represents one game, with moves separated by commas.
Moves are represented as column (a-h) + row (1-8), e.g., "d3", "e6".
"""

import argparse
import random
from typing import List, Tuple, Set


class OthelloBoard:
    """Represents an Othello game board and implements game rules."""
    
    # Board size
    SIZE = 8
    
    # Player constants
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    # Directions for checking valid moves
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    def __init__(self):
        """Initialize a new Othello board with the standard starting position."""
        # Create an empty board
        self.board = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        
        # Set up the initial four pieces in the center
        self.board[3][3] = self.WHITE
        self.board[3][4] = self.BLACK
        self.board[4][3] = self.BLACK
        self.board[4][4] = self.WHITE
        
        # Black moves first
        self.current_player = self.BLACK
        
        # Keep track of moves made
        self.moves = []
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Return a list of valid moves for the current player."""
        valid_moves = []
        
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if placing a piece at (row, col) is a valid move for the current player."""
        # The cell must be empty
        if self.board[row][col] != self.EMPTY:
            return False
        
        # The move must flip at least one opponent's piece
        opponent = self.WHITE if self.current_player == self.BLACK else self.BLACK
        
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            # Check if we have at least one opponent's piece in this direction
            if (0 <= r < self.SIZE and 0 <= c < self.SIZE and 
                self.board[r][c] == opponent):
                # Continue in this direction
                r += dr
                c += dc
                while 0 <= r < self.SIZE and 0 <= c < self.SIZE:
                    if self.board[r][c] == self.EMPTY:
                        # Empty cell, no flip in this direction
                        break
                    if self.board[r][c] == self.current_player:
                        # Found our own piece, this is a valid move
                        return True
                    # Continue in this direction
                    r += dr
                    c += dc
        
        return False
    
    def make_move(self, row: int, col: int) -> bool:
        """Make a move at (row, col) for the current player. Return True if successful."""
        if not self.is_valid_move(row, col):
            return False
        
        # Place the piece
        self.board[row][col] = self.current_player
        
        # Flip opponent's pieces
        opponent = self.WHITE if self.current_player == self.BLACK else self.BLACK
        
        for dr, dc in self.DIRECTIONS:
            # Pieces to flip in this direction
            to_flip = []
            
            r, c = row + dr, col + dc
            # Check if we have at least one opponent's piece in this direction
            while (0 <= r < self.SIZE and 0 <= c < self.SIZE and 
                   self.board[r][c] == opponent):
                to_flip.append((r, c))
                r += dr
                c += dc
                
                # If we reach the edge or an empty cell, no flip in this direction
                if not (0 <= r < self.SIZE and 0 <= c < self.SIZE) or self.board[r][c] == self.EMPTY:
                    to_flip = []
                    break
                
                # If we reach our own piece, flip all pieces in between
                if self.board[r][c] == self.current_player:
                    break
            
            # Flip pieces
            for flip_r, flip_c in to_flip:
                self.board[flip_r][flip_c] = self.current_player
        
        # Record the move
        move_notation = self.coords_to_notation(row, col)
        self.moves.append(move_notation)
        
        # Switch player
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK
        
        return True
    
    def has_valid_moves(self) -> bool:
        """Check if the current player has any valid moves."""
        return len(self.get_valid_moves()) > 0
    
    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK
    
    def is_game_over(self) -> bool:
        """Check if the game is over (no valid moves for either player)."""
        # Check if current player has valid moves
        if self.has_valid_moves():
            return False
        
        # Switch player and check if they have valid moves
        self.switch_player()
        has_moves = self.has_valid_moves()
        self.switch_player()  # Switch back
        
        return not has_moves
    
    def coords_to_notation(self, row: int, col: int) -> str:
        """Convert board coordinates to standard notation (e.g., (3,4) -> 'e4')."""
        return chr(97 + col) + str(row + 1)
    
    def notation_to_coords(self, notation: str) -> Tuple[int, int]:
        """Convert standard notation to board coordinates (e.g., 'e4' -> (3,4))."""
        col = ord(notation[0]) - 97
        row = int(notation[1]) - 1
        return row, col
    
    def get_moves_notation(self) -> List[str]:
        """Return the list of moves in standard notation."""
        return self.moves


def generate_game() -> List[str]:
    """Generate a single valid Othello game and return the list of moves."""
    board = OthelloBoard()
    
    while not board.is_game_over():
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            # No valid moves for current player, switch to other player
            board.switch_player()
            continue
        
        # Choose a random valid move
        row, col = random.choice(valid_moves)
        board.make_move(row, col)
    
    return board.get_moves_notation()


def generate_games(num_games: int) -> List[List[str]]:
    """Generate multiple Othello games."""
    games = []
    for _ in range(num_games):
        game = generate_game()
        games.append(game)
    return games


def save_games(games: List[List[str]], output_file: str) -> None:
    """Save games to a text file, one game per line."""
    with open(output_file, 'w') as f:
        for game in games:
            f.write(','.join(game) + '\n')


def main():
    """Main function to parse arguments and generate games."""
    parser = argparse.ArgumentParser(description='Generate valid Othello games.')
    parser.add_argument('--num-games', type=int, default=10,
                        help='Number of games to generate (default: 10)')
    parser.add_argument('--output', type=str, default='othello_games.txt',
                        help='Output file path (default: othello_games.txt)')
    
    args = parser.parse_args()
    
    print(f"Generating {args.num_games} Othello games...")
    games = generate_games(args.num_games)
    
    save_games(games, args.output)
    print(f"Games saved to {args.output}")


if __name__ == '__main__':
    main()