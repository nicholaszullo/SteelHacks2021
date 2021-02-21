import math
import random
import torch
import time
from tqdm import tqdm

class Node:
	"""
	A Node in the MCTS tree.
	Must have a state, ways to update, ways to chose next state
	Uses UCB1 to make decisions 
	"""

	def __init__(self, move = None, parent = None, state = None):
		self.move = move		#Previously made move
		self.parent = parent	#Parent node of state, used for backprop
		self.untried = list(state.generate_legal_moves())	#State of game at Node
		self.wins = 0			#Wins following this move path
		self.visits = 0			#Visits down this move path
		self.children = []		#States after taking a legal move
		self.color = state.turn #Record color for update
		self.state = state
		self.y_pred = None

	def __repr__(self) -> str:
		return f"State is {self.state}"


	def create_child(self, move, state):
		"""
		Create a new child node with a given state and the current move to make this state
		"""
		child = Node(move = move, parent = self, state = state)
		self.untried.remove(move)			#Test with list and move implementaion
		self.children.append(child)
		return child
	
	def predict(self, nn):
		key = [.01, 1, 2.9, 3, 5, 9, 1.5]	#Empty, Pawn, Knight, Bishop, Rook, Queen, King
		x = torch.zeros(size=(1,64), requires_grad=True).to(nn.device)
		for i in range(64):				#Create flat board whre each piece is represented by its value
			piece = self.state.piece_at(i)
			if piece == None:
				x[0,i] = key[0]

		self.y_pred = nn(x)

	def update_state(self, val):
		self.visits += 1
		self.wins += val

	def chose_path(self,nn):
		max = float("-inf")
		choice = None
		for child in self.children:
			child.predict(nn)
			val = ((child.wins / child.visits) + math.sqrt(2*math.log(self.visits)/child.visits))*child.y_pred	#UCB1 Selection of node
			if max < val:
				choice = child
				max = val
		return choice

class MCTS():

	def __init__(self, start, net) -> None:
		self.root = Node(state=start)
		self.white_wins = 0
		self.black_wins = 0
		self.draws = 0
		self.last_win = None
		self.nn = net

	def run(self, iters):
		for _ in tqdm(range(iters)):
			curr = self.root
			state = self.root.state.copy()	#Create copy of board state for each new iteration so original is preserved
			"""
			MCTS has 4 components, selction, expansion, simulation, backpropogation
			"""
			#Select
			while curr.untried == [] and curr.children != []:	#Stop leaf node
				curr = curr.chose_path(self.nn)	#determine child to move to
				state.push(curr.move)	#move state to curr's state

			#Expand
			if curr.untried != []:	#Generate a child for state
				move = random.choice(curr.untried)	
				state.push(move)
				curr = curr.create_child(move, state)

			
			#Simulation, play game
			legal_moves = list(state.generate_legal_moves())
			while not state.is_game_over() and len(state.move_stack) < 100:		#Stop when game is over or move limit exceeded
				state.push(random.choice(legal_moves))
				legal_moves = list(state.generate_legal_moves())
				
				"""max = float("-inf")
				choice = None
				for move in curr.untried:
					curr.predict(self.nn)
					if curr.y_pred > max:
						max = curr.y_pred
						choice = move

				state.push(choice)
				curr = curr.create_child(choice, state)"""
				

			
			white_val = 0
			black_val = 0
			if state.result() == "1-0":
				white_val = 1
				black_val = -1
				self.last_win = state
				self.white_wins += 1
			elif state.result() == "0-1":
				black_val = 1
				white_val = -1
				self.last_win = state
				self.black_wins += 1
			else:
				white_val = 1/2
				black_val = 1/2
				self.draws += 1

			#Backprop
			while curr != None:
				if (curr.color):	#white is true
					curr.update_state(white_val)	#change wins at node based on result of game
					if not curr.y_pred == None:
						self.nn.backward(curr.y_pred, white_val)
				else:
					curr.update_state(black_val)
					if not curr.y_pred == None:
						self.nn.backward(curr.y_pred, black_val)	
				curr = curr.parent		#Recurse up tree

		
			