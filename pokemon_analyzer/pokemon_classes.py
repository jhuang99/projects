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
	def get_pokemon(self, pokemon):
		last_turn = self.get_turn(self.turn_number)
		return last_turn.get_pokemon(pokemon)




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

				if pokemon.name == name or pokemon.nickname == name or (type(name) == Pokemon and name == pokemon):
					return pokemon
				elif pokemon.mega_evolved and pokemon.name + "-Mega" == name:
					return pokemon
			print(str(name) + " not found in Player's 1 team")
		elif player == 2:
			for pokemon in self.p2_pokemon:
				if pokemon.name == name or pokemon.nickname == name or (type(name) == Pokemon and name == pokemon):
					return pokemon
				elif pokemon.mega_evolved and pokemon.name + "-Mega" == name:
					return pokemon
			print(str(name) + " not found in Player's 2 team")
		else:
			for pokemon in self.p1_pokemon + self.p2_pokemon:
				if pokemon.name == name or pokemon.nickname == name or (type(name) == Pokemon and name == pokemon):
					return pokemon
				elif pokemon.mega_evolved and pokemon.name + "-Mega" == name:
					return pokemon
			print( str(name) + " not found in the battle")

	def get_action(self, number):
		return self.actions[number - 1]

	def __str__(self):
		return "Turn {self.number}".format(self = self)

class Pokemon:
	"""Each pokemon"""
	def __init__(self, species, trainer):
		self.turn = 0
		self.name = species
		self.nickname = None
		if "*" in species:
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
		self.defeated_action = None
		self.stat_changes = []

		#each turn, has a list of things that happened to it: damage, stats effected, fainted? by who




	def copy(self, turn):
		poke_copy = copy.copy(self)
		poke_copy.turn = turn.number
		poke_copy.actions = copy.copy(self.actions)
		poke_copy.status_condition = copy.copy(self.status_condition)
		poke_copy.prev_copy = self
		return poke_copy

	def faint(self, turn):
		self.fainted = True
		self.turn_fainted = turn.number
		self.health = 0
		self.in_play = False
		turn.get_action(len(turn.actions)).defeated = self
		# turn.get_action(len(turn.actions)).consequence += " " + self.name + " fainted."
		self.defeated_action = turn.get_action(len(turn.actions))


	def take_damage(self, damage):
		self.health -= damage

	def add_action(self, action):
		self.actions.append(action)

	def __str__(self):
		return self.name




class Action:
	"""The Action that occurs in a turn"""
	order = 0
	def __init__(self, battle, turn, player, action, *args):
		Action.update_order()
		self.battle = battle
		self.turn = turn
		self.player = player
		self.type = action
		
	def update_order():
		Action.order += 1
	def reset():
		Action.order = 0

	def __str__(self):
		# return "cat"
		pass

class Attack(Action):

	def __init__(self, battle, turn, player, pokemon, move, consequence):
		Action.__init__(self, battle, turn, player, "attack")
		self.pokemon = pokemon
		self.move = move
		self.consequence_string = consequence
		self.consequences = []
		self.order = Action.order
		self.analyze_consequence()


	def analyze_consequence(self):
		damage_match = re.finditer('((A critical hit!)?(\s)?(It\'s (.*) effective(!|\.\.\.))?(\s)?(The opposing)?(\s)?([^!.]*) lost (.*)% of its health!)', self.consequence_string)
		
		stats_move_match = re.finditer('(.*) (raised|lowered) (the opposing|your) team\'s (.*)!', self.consequence_string)
		stats_match = re.finditer('(The opposing )?(.*)\'s (.*) (sharply)?(\s)?(rose|fell)!', self.consequence_string)
		status = {"poisoned": "(The opposing )?(.*) was badly poisoned!", "paralyzed": "(The opposing )?(.*) is paralyzed!", "burned": "(The opposing )?(.*) was burned!", "sleep": "(The opposing )?(.*) fell asleep!"}
		dictionary = {}
		for status_condition, wording in status.items():
			dictionary[re.finditer(wording, self.consequence_string)] = status_condition

		for match in damage_match:

			critical_hit = match.group(2)
			effectiveness = match.group(5)
			pokemon_target_name = match.group(10)
			pokemon_targeted = self.turn.get_pokemon(pokemon_target_name)
			damage = match.group(11)
			self.consequences.append(Damage(self.pokemon, pokemon_targeted, damage, effectiveness, critical_hit))

		for match in stats_move_match:
			# print(self.consequence_string)
			effect = match.group(2)
			team = match.group(3)
			stat_effected = match.group(4)
			if team == "your":
				for pokemon in self.turn.p1_pokemon:
					if pokemon.in_play:
						self.consequences.append(Stat_Changes(self.pokemon, pokemon, stat_effected, effect))
			else:
				for pokemon in self.turn.p2_pokemon:
					if pokemon.in_play:
						self.consequences.append(Stat_Changes(self.pokemon, pokemon, stat_effected, effect))
		for match in stats_match:
			opposing = match.group(1)
			effected_pokemon = match.group(2)
			stat_effected = match.group(3)
			effect = match.group(6)
			pokemon = self.turn.get_pokemon(effected_pokemon)
			self.consequences.append(Stat_Changes(self.pokemon, pokemon, stat_effected, effect))

		for match_iter, status in dictionary.items():
			for match in match_iter:
				opposing = match.group(1)
				pokemon_name = match.group(2)
				if opposing:
					pokemon = self.turn.get_pokemon(pokemon_name, 2)
				else:
					pokemon = self.turn.get_pokemon(pokemon_name, 1)
				self.consequences.append(Status_Effects(self.pokemon, pokemon, status))

	def return_consequences(self):
		to_return = ""
		for x in self.consequences:
			to_return += str(x)
		return to_return 

	def __str__(self):
		return "Pokemon: " + self.pokemon.name + "\nAttack: " + self.move + self.return_consequences() + "\n"


class Consequences:
	def __init__(self, type, acting_pokemon, target_pokemon):
		self.type = type
		self.acting_pokemon = acting_pokemon
		self.target_pokemon = target_pokemon

	def __str__(self):
		pass

class Damage(Consequences):
	def __init__(self, acting_pokemon, target_pokemon, damage, effectiveness, critical_hit):
		Consequences.__init__(self, "damage", acting_pokemon, target_pokemon)
		self.damage = damage
		self.effectiveness = effectiveness
		self.critical_hit = critical_hit
		self.take_damage()
		
	def take_damage(self):
		if '–' in self.damage:
			range_damage = self.damage.split("–")
			range_damage = [float(number) for number in range_damage]
			self.damage = range_damage
			if self.target_pokemon.health == 100:
				self.target_pokemon.health = [100, 100]
			self.target_pokemon.health = [health - damage for health, damage in zip(self.target_pokemon.health, range_damage)]
		else:
			self.damage = float(self.damage)
			self.target_pokemon.health -= self.damage
	def __str__(self):
		if not self.effectiveness:
			self.effectiveness = "normal"
		return "\nEffected: " + str(self.target_pokemon) + "\nDamage: " + str(self.damage) + "\nEffectiveness: " + self.effectiveness + "\nCritical: " + str(self.critical_hit)

class Status_Effects(Consequences):
	def __init__(self, acting_pokemon, target_pokemon, status_change):
		Consequences.__init__(self, "status_effect", acting_pokemon, target_pokemon)
		self.status = status_change
		target_pokemon.status_condition += self.status
	def __str__(self):
		return "\nEffected: " + str(self.target_pokemon) + "\nStatus Condition: " + self.status

class Stat_Changes(Consequences):
	def __init__(self, acting_pokemon, target_pokemon, stat, change):
		Consequences.__init__(self, "stat_change", acting_pokemon, target_pokemon)
		self.stat = stat
		self.change = change
		self.target_pokemon.stat_changes.append(stat + " " + change)
	
	def __str__(self):
		return "\nEffected: " + str(self.target_pokemon) + "\nStats: " + self.stat + " " + self.change



class Switch(Action):
	def __init__(self, battle, turn, player, withdraw_poke, send_poke):
		Action.__init__(self, battle, turn, player, "switch")
		self.order = Action.order
		self.withdraw_poke = withdraw_poke
		self.send_poke = send_poke
		withdraw_poke.in_play = False
		send_poke.in_play = True
	def __str__(self):
		return  "\nPlayer: " + self.player.name + "\nWithdrew: " + self.withdraw_poke.name + "\nSent: " + self.send_poke.name


class Player:
	"""The Player"""
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.team = []
		self.win = False
		self.actions = [] #list of action objects 

	def has_won(self):
		"""Checks to see if player has won"""
		if won:
			self.win = true

	def add_action(self, action):
		self.actions.append(action)

	def __str__(self):
		return self.name



# can organize by player, by turn, by pokemon 
# what would someone want to know after a game
# which pokemon did the most damage in general
# which pokemon finished off the most other pokemon
# which pokemon had the most gameplay/ lasted the most turns
# which pokemon each pokemon defeated and the pokemon it had lost to
# most used move
# most effective 