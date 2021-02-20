import chess
import engine.mcts as mcts

board = chess.Board()

node = mcts.run(board, 100)
print(f"{node.children[1].wins}")