import math
import random
from tqdm import tqdm

class Node:
	"""
	A Node in the MCTS tree.
	Must have a state, ways to update, ways to chose next state
	Uses UCB1 to make decisions 
	"""

	def __init__(self, move = None, parent = None, state = None):
		self.move = move		#Previously made move
		self.parent = parent	#Parent node of state
		self.untried = list(state.generate_legal_moves())	#State of game at Node
		self.wins = 0			#Wins following this move path
		self.visits = 0			#Visits down this move path
		self.children = []		#States after taking a legal move
		self.color = state.turn #Record color for update
		self.state = state

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
	
	def update_state(self, val):
		self.visits += 1
		self.wins += val

	def chose_path(self):
		max = 0
		choice = None
		for child in self.children:
			val = (child.wins / child.visits) + math.sqrt(2*math.log(self.visits)/child.visits)	#UCB1 Selection of node
			if max < val:
				choice = child
				max = val
		return choice

def run(start, iters):
	root = Node(state = start)

	for i in tqdm(range(iters)):
		curr = root
		state = start.copy()	#Create copy of board state for each new iteration so original is preserved
		"""
		MCTS has 4 components, selction, expansion, simulation, backpropogation
		"""
		#Select
		while curr.untried == [] and curr.children != []:	#Stop leaf node
			curr = curr.chose_path()	#determine child to move to
			state.push(curr.move)	#move state to curr's state

		#Expand
		if curr.untried != []:	#Generate children for state
			move = random.choice(curr.untried)	#chose random move to make child of 
			state.push(move)
			curr = curr.create_child(move, state)

		
		#Simulation, play game
		legal_moves = list(state.generate_legal_moves())
		while not state.is_game_over():		#No moves means game is over
			state.push(random.choice(legal_moves))
			legal_moves = list(state.generate_legal_moves())
		#	print(state.fen())
		
		white_val = 0
		black_val = 0
		if state.result() == "1-0":
			white_val = 1
			black_val = 0
		elif state.result == "0-1":
			black_val = 1
			white_val = 0
		else: 
			white_val = 1/2
			black_val = 1/2
	

		#Backprop
		while curr != None:
			if (curr.color):	#white is true
				curr.update_state(white_val)	#change wins at node based on result of game
			else:
				curr.update_state(black_val)		
			curr = curr.parent		#Recurse up tree
	return root
	
		