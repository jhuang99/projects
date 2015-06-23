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
		self.current_pokemon = []
		self.all_turns = []
		self.winner = None


	def add_players(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

	def define_battle(self, battleType):
		self.battleType = battleType
		if "Doubles" in battleType:
			self.doubles = True




class Turn:
	"""What number turn"""
	def __init__(self, number, current_pokemon):
		self.number = number
		self.actions = {}
		self.current_pokemon = []

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

	def remove_pokemon(self, pokemon):
		"""Removes a pokemon from a team after it has fainted"""
		if pokemon not in self.team:
			raise NameError("Pokemon not on team")
		else:
			self.team.remove(pokemon)

	def has_won(self):
		"""Checks to see if player has won"""
		if won:
			self.win = true

	
class Pokemon:
	"""Each pokemon"""
	def __init__(self, species, trainer):
		self.type = species
		self.name = self.type
		self.trainer = trainer
		self.item = None
		self.fainted = False
		self.turnFainted = False
		self.actions = {} # map action to the effect
		self.mega_evolved = False
		self.status_condition = []
		self.health = 100




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