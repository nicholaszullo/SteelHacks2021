import chess
import torch
import engine.mcts as mcts
from game.application import Application
import engine.neural_net as net

board = chess.Board()

nn = net.NeuralNet(lr=.01,device="cuda:0")
nn.load_state_dict(torch.load("network.dat"))
nn.eval()

game = mcts.MCTS(board, net=nn)
game.run(iters=500)
print(list(nn.parameters()))
torch.save(nn.state_dict(), "network.dat")
app = Application(game)
app.mainloop()
