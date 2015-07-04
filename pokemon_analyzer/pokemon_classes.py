import copy
class Battle:
	"""The overall condition of the entire Battle
	Contains all the information about the general """

	def __init__(self):
		self.battleType = None
		self.turn_number = 0
		self.game_over = False
		self.player1 = None
		self.player2 = None
		self.conditions = []
		self.rated = False
		self.doubles = False
		self.string_turns = []
		self.winner = None
		self.all_turns = []


	def add_players(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

	def define_battle(self, battleType):
		self.battleType = battleType
		if "Doubles" in battleType:
			self.doubles = True




class Turn:
	"""Each Turn"""
	def __init__(self, number):
		self.number = number
		self.actions = {}
		self.all_pokemon = [] #all pokemon present in this round
		self.fainted_pokemon = [] #all the pokemon who fainted in this turn
		self.p1_pokemon = []
		self.p2_pokemon = []



	def pokemonStatus(self, battle):
		"""displays the status of each player's pokemon at the end of each turn"""
		print(battle.player1 + "'s pokemon alive:" + player1.team)



class Player:
	"""The Player"""
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.team = []
		self.win = False
		self.actions = {}

	def has_won(self):
		"""Checks to see if player has won"""
		if won:
			self.win = true


	
class Pokemon:
	"""Each pokemon"""
	def __init__(self, species, trainer):
		self.turn = 0
		self.type = species
		self.name = self.type
		self.trainer = trainer
		self.item = None
		self.fainted = False
		self.turn_fainted = False
		self.actions = {} # map action to the effect
		self.mega_evolved = False
		self.status_condition = []
		self.health = 100
		self.prev_copy = None
		self.in_play = False

	def copy(self, turn):
		poke_copy = copy.deepcopy(self)
		poke_copy.turn = turn.number
		poke_copy.prev_copy = self
		return poke_copy

	def faint(self, turn):
		self.faint = True
		self.turn_fainted = turn.number
		self.health = 0
		self.in_play = False



# class Node:
# 	"""A single node for a linked list"""
# 	def __init__(self, value=None, prev=None, next=None):
# 		self.value = value
# 		self.prev = prev
# 		self.next = next
# 	def get_value(self):
# 		return self.value
# 	def get_prev(self):
# 		return self.prev
# 	def get_next(self):
# 		return self.next
# 	def set_next(self, new_next):
#     	self.next = new_next
#     def set_prev(self, new_prev):
#     	self.prev = new_prev

# class LinkedList(object):

# 	def __init__(self, head=None):
# 		self.head = head
# 		if not head:
# 			self.size = 0
# 		else:
# 			self.size = 1

# 	def insert(self, value):
# 		new_node = Node(value)
# 		new_node.set_prev(self.head)
# 		self.set_next(new_node)
# 		self.head = new_node
# 		self.size += 1





#Organize each Text into different Blocks 
#Block 1: Beginning up till turn 1
#Each Turn is a block


# can organize by player, by turn, by pokemon 
# what would someone want to know after a game
# which pokemon did the most damage in general
# which pokemon finished off the most other pokemon
# which pokemon had the most gameplay/ lasted the most turns
# which pokemon each pokemon defeated and the pokemon it had lost to
# most used move
# most effective 