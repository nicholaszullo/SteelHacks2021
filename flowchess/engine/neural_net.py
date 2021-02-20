import torch
from torch import nn
import mcts
import math

class NeuralNet(nn.Module):
	def __init__(self):
		super().__init__()

		self.input = nn.Linear(64,32)
		self.hidden = nn.Linear(32,20)
		self.output = nn.Linear(20,1)

	def forward(self, x):
		x = nn.functional.relu(self.input(x))		#ReLU activation
		x = nn.functional.relu(self.hidden(x))
		x = torch.sigmoid(self.output(x))							#Sigmoid activation





weight = torch.rand(1, requires_grad=True) 
bias = torch.rand(1, requires_grad=True)
learning_rate = .01

