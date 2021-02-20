import chess
import engine.mcts as mcts

board = chess.Board()

node = mcts.run(board, 5000)
print(f"{node.wins}")