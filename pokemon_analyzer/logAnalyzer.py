import sys

filename = str(sys.argv[1])
logFile = open(filename, "r")
for line in logFile:
    print(line)
class Battle:
	"""The overall condition of the entire Battle"""
	def __init__(self, gameType):
		self.battleType = battleType
		self.turn = 0
		self.gameOver = false
		self.player1 = none
		self.player2 = none

	def addPlayers(self, player1, player2):
		self.player1 = player1
		self.player2 = player2



class Turn:
	"""What number turn"""
	def __init__(self, number):
		self.number = number

	def add_action(self, pokemon, action):
		pokemon.player.actions.append(action)
		pokemon.actions.append(action)

	def pokemonStatus(self, battle):
		"""displays the status of each player's pokemon at the end of each turn"""
		print(battle.player1 + "'s pokemon alive:" + player1.team)



class Player:
	"""The Player"""
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.team = []
		self.win = false
		self.actions = []

	def pokemon_team(self, team):
		"""Adds a pokemon team to a player"""
		self.team = team

	def remove_pokemon(self, pokemon):
		"""Removes a pokemon from a team after it has fainted"""
		if pokemon not in self.team:
			raise NameError("Pokemon not on team")
		else:
			self.team.remove(pokemon)

	def hasWon(self, won):
		"""Checks to see if player has won"""
		if won:
			self.win = true

	
class Pokemon:
	"""Each pokemon"""
	def __init__(self, species, name, player):
		self.type = species
		self.name = name
		self.player = player
		self.item = none
		self.fainted = false
		self.turnFainted = false
		self.actions = []






# can organize by player, by turn, by pokemon 
# what would someone want to know after a game
# which pokemon did the most damage in general
# which pokemon finished off the most other pokemon
# which pokemon had the most gameplay/ lasted the most turns
# which pokemon each pokemon defeated and the pokemon it had lost to
# most used move
# most effective 