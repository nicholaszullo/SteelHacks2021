import chess
import chess.svg
import sys

# Make a new game
board = chess.Board()

# get fen string
print(f"New game fen string: {board.fen()}")

# List legal moves

legal_first_moves = list(board.generate_legal_moves())
print(f"Legal first moves: {legal_first_moves}")

# Play e4
board.push_uci("e2e4")

# make svg
board_svg = chess.svg.board(board=board)
f = open("PlayedE4.svg", "w")
f.write(board_svg)
f.close()

