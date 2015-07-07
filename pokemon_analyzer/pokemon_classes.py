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
		self.actions = {}
		self.p1_pokemon = []
		self.p2_pokemon = []



	def pokemonStatus(self, battle):
		"""displays the status of each player's pokemon at the end of each turn"""
		print(battle.player1 + "'s pokemon alive:" + player1.team)

	def get_pokemon(self, player, name):
		if player == 1:
			for pokemon in self.p1_pokemon:
				if pokemon.name == name:
					return pokemon
			print("Pokemon not found")
		else:
			for pokemon in self.p2_pokemon:
				if pokemon.name == name:
					return pokemon
			print("Pokemon not found")


class Action:
	"""The Action that occurs in a turn"""
	def __init__(self, turn, player, action, *args):
		#attack--args = (pokemon, attack, consequences)
		#switch--args = (withdraw_poke, send_poke)
		this.turn = turn
		self.player = player
		self.order = 0
		self.consequences = None
		self.type = action
		if action == "attack":
			self.attack(*args)

		elif action == "switch":
			self.withdraw_poke = args[0]
			self.send_poke = args[1]

	def attack(pokemon, pokemon_directed_at, attack, consequence):
		damage_match = re.finditer('(.*) lost (.*)% of its health', consequence)
		for match in damage_match:
			pokemon_affected = match.group(1) 
			damage = match.group(2)
			for pokemon in self.turn.p1_pokemon + self.turn.p2_pokemon:
				if pokemon_affected == pokemon.name:
					pokemon.take_damage(damage)
					#need to figureout how to subtract damage, tuples?



		process_consequences(consequence)


	def process_consequence(consequence):
		pass
		#deal with damage
	def update_order():
		self.order += 1


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
		self.fainted = True
		self.turn_fainted = turn.number
		self.health = 0
		self.in_play = False

	def take_damage(self, damage):
		self.health -= damage


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