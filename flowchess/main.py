import chess
import engine.mcts as mcts
from game.application import Application
import engine.neural_net as net

board = chess.Board()
nn = net.NeuralNet(lr=.01,device="cuda:0")

game = mcts.MCTS(board, net=nn)
game.run(iters=1000)
print(game.last_win.move_stack)
app = Application(game)
app.mainloop()
