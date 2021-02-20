import chess
import engine.mcts as mcts
from game.application import Application

board = chess.Board()

game = mcts.MCTS(board)
game.run(iters=10000)

app = Application(game)
app.mainloop()