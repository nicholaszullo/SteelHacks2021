import torch
from torch import nn
import math

"""
Given a state of the board, return the probability it is a good position
"""

class NeuralNet(nn.Module):
	def __init__(self, lr=.01, device="cpu"):
		super().__init__()

		self.device = device
		self.input = nn.Linear(64,20,bias=True)
		self.hidden = nn.Linear(20,10,bias=True)
		self.output = nn.Linear(10,1,bias=True)
		self.optim = torch.optim.Adam(self.parameters(), lr=lr)
		self.to(device)

	def forward(self, x):
		x = nn.functional.leaky_relu(self.input(x))		#ReLU activation
		x = nn.functional.leaky_relu(self.hidden(x))
		x = torch.tanh(self.output(x))			#Sigmoid activation
		return x

	def backward(self, y_pred, y):
		loss_fn = nn.MSELoss()
		boxed_y_pred = torch.tensor(y_pred).to(self.device)
		boxed_y = torch.tensor(y).to(self.device)
		loss = loss_fn(boxed_y_pred, boxed_y)
		loss.requires_grad = True
		self.optim.zero_grad()
		loss.backward()
		self.optim.step()