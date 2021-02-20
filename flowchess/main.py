import chess
import engine.mcts as mcts

board = chess.Board()

game = mcts.MCTS(board)
game.run(iters=1000)

print(f"{game.white_wins} {game.black_wins}")
print(game.last_win.move_stack)