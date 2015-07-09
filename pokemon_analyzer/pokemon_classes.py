import copy
import re

class Battle:
	"""The overall condition of the entire Battle
	Contains all the information about the general """

	def __init__(self):
		self.battleType = None
		self.turn_number = 0
		self.player1 = None
		self.player2 = None
		self.conditions = []
		self.rated = False
		self.doubles = False
		self.string_turns = []
		self.winner = None
		self.all_turns = []
		self.end_result = None


	def add_players(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

	def define_battle(self, battleType):
		self.battleType = battleType
		if "Doubles" in battleType:
			self.doubles = True
	def get_turn(self, number):
		return self.all_turns[number]




class Turn:
	"""Each Turn"""
	def __init__(self, number):
		self.number = number
		self.actions = []
		self.p1_pokemon = []
		self.p2_pokemon = []


	def add_action(self, action):
		self.actions.append(action)
	def pokemonStatus(self, battle):
		"""displays the status of each player's pokemon at the end of each turn"""
		print(battle.player1 + "'s pokemon alive:" + player1.team)

	def get_pokemon(self, name, player = None):
		if player == 1:
			for pokemon in self.p1_pokemon:
				if pokemon.name == name:
					return pokemon
			print("pokemon not found")
		elif player == 2:
			for pokemon in self.p2_pokemon:
				if pokemon.name == name:
					return pokemon
			print("pokemon not found")
		else:
			for pokemon in self.p1_pokemon + self.p2_pokemon:

				if pokemon.name == name:
					# print(pokemon.name)
					return pokemon
			print("pokemon not found")
	def get_action(self, number):
		return self.actions[number - 1]


class Action:
	"""The Action that occurs in a turn"""
	order = 0
	def __init__(self, turn, player, action, *args):
		Action.update_order()
		self.turn = turn
		self.player = player
		self.type = action
		
	def process_consequence(consequence):
		pass
		#deal with damage
	def update_order():
		Action.order += 1
	def reset():
		Action.order = 0

class Attack(Action):

	def __init__(self, turn, player, pokemon, move, consequence):
		Action.__init__(self, turn, player, "attack")
		self.pokemon = pokemon
		self.move = move
		self.consequence = consequence
		self.order = Action.order
		self.analyze_consequence()
		self.damage = None

	def analyze_consequence(self):
		damage_match = re.finditer('(The opposing )?(.*) lost (.*)% of its health!', self.consequence)
		for match in damage_match:
			pokemon_effected = match.group(2)
			pokemon = self.turn.get_pokemon(pokemon_effected)
			self.effected_pokemon = pokemon
			damage = match.group(3)
			if '–' in damage:
				
				range_damage = damage.split("–")
				range_damage = [float(number) for number in range_damage]
				self.damage = range_damage
				if pokemon.health == 100:
					pokemon.health = [100, 100]
				pokemon.health = [health - damage for health, damage in zip(pokemon.health, range_damage)]
			else:
				damage = float(damage)
				self.damage = damage
				pokemon.health -= damage

			# for pokemon in self.turn.p1_pokemon + self.turn.p2_pokemon:
			# 	if pokemon_effected == pokemon.name:
			# 		pokemon.take_damage(damage)

class Switch(Action):
	def __init__(self, turn, player, withdraw_poke, send_poke):
		Action.__init__(self, turn, player, "switch")
		self.order = Action.order
		self.withdraw_poke = withdraw_poke
		self.send_poke = send_poke
		withdraw_poke.in_play = False
		send_poke.in_play = True


class Player:
	"""The Player"""
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.team = []
		self.win = False
		self.actions = []

	def has_won(self):
		"""Checks to see if player has won"""
		if won:
			self.win = true

	def add_action(self, action):
		self.actions.append(action)

	
class Pokemon:
	"""Each pokemon"""
	def __init__(self, pokemon, trainer):
		self.turn = 0
		self.name = pokemon
		self.nickname = None
		if "*" in pokemon:
			self.name = "Gourgeist-Super"
		#cheat mode to get around * marked pokemon
		self.trainer = trainer
		self.item = None
		self.fainted = False
		self.turn_fainted = False
		self.actions = [] # list of action objects
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
		self.fainted = True
		self.turn_fainted = turn.number
		self.health = 0
		self.in_play = False

	def take_damage(self, damage):
		self.health -= damage

	def add_action(self, action):
		self.actions.append(action)
	


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