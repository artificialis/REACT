# Othello Tools

This directory contains tools related to the Othello game.

## Generate Othello Games

The `generate_othello_games.py` script generates valid Othello games and outputs them to a text file.

### Usage

```bash
python generate_othello_games.py [--num-games NUM_GAMES] [--output OUTPUT_FILE]
```

### Arguments

- `--num-games`: Number of games to generate (default: 10)
- `--output`: Output file path (default: othello_games.txt)

### Output Format

The script generates a text file with one game per line. Each game is represented as a comma-separated list of moves in standard Othello notation:

- Columns are labeled a through h (from left to right)
- Rows are labeled 1 through 8 (from top to bottom)
- Moves are represented as column+row (e.g., "d3", "e6")

Example output line:
```
e6,f4,c3,c4,f3,f6,c5,b6,b5,e3,e2,b4,d3,f5,b3,e7,a5,a2,e8,g3,f2,g1,c6,f1,e1,a3,h3,d1,d2,a6,a4,h2,c2,f7,a1,b1,g8,c1,g5,f8,d6,h4,c7,c8,g4,d8,g2,a7,g6,b2,d7,h8,h1,h5,a8,b7,g7,h7,b8,h6
```

### Examples

Generate 10 games with default output file:
```bash
python generate_othello_games.py
```

Generate 100 games with a custom output file:
```bash
python generate_othello_games.py --num-games 100 --output my_games.txt
```

### Implementation Details

The script implements the standard Othello/Reversi rules:

1. The game is played on an 8×8 board
2. Initial setup has four pieces in the center (black at e4 and d5, white at d4 and e5)
3. Black moves first
4. A valid move must capture at least one opponent's piece
5. Captured pieces are flipped to the current player's color
6. If a player has no valid moves, their turn is skipped
7. The game ends when neither player has valid moves

The script generates random but valid games by choosing random moves from the set of valid moves at each step.