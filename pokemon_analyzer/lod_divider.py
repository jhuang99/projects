import log_analyzer
import re
import unittest
import sys


def read_body(filename):
	log_file = open(filename, "r") #opens the text_file
	battle = log_analyzer.Battle() 
	start = [] #the lines associated before the first turn
	middle = ""	#lines associated with each turn
	end = "" #lines associated after the battle is over
	turnsStarted = False
	battleOver = False
	for line in log_file: #splits the lines into start, middle, end
		if not turnsStarted:
			if  "Go" not in line:
		   		start.append(line)
		   		continue
			else:
		   		turnsStarted = True
		if not battleOver:
			if "won" not in line and "lost due to inactivity" not in line and "forfeited" not in line:
				middle += line
				continue
			else:
				battleOver = True
		else:
			end.append(line)
	analyze_start(start, battle)

	all_turns = split_turns(middle)
	for number in all_turns:
		analyze_turn(number, all_turns[number], battle)
	analyze_end(end, battle)
	

	# print(battle.player1.team[4].mega_evolved)
	log_file.close()
	return battle

def analyze_start(start, battle):
	numOfPlayers = 0
	format = False
	player1Team = False
	player2Team = False
	for line in start:
		line = line.rstrip('\n')

		matchPlayer = re.match( r'(.*) joined.', line)
		
		if matchPlayer and numOfPlayers < 2:
			if numOfPlayers == 0:
				player1 = log_analyzer.Player(matchPlayer.group(1), 1)
			else:
				player2 = log_analyzer.Player(matchPlayer.group(1), 2)
				battle.add_players(player1, player2)
			numOfPlayers = numOfPlayers + 1
		
		elif "Format:" in line:
			format = True
		elif format:
			battle.define_battle(line)
			format = False
		elif "rated Battle" in line:
			battle.rated = True
		elif "Clause:" in line or "Mod:" in line:
			battle.conditions.append(line)
		elif battle.player1 and battle.player1.name + "'s team" in line:
			player1Team = True
		elif player1Team:
			team = line.split(" / ")
			for pokemon in team:
				battle.player1.start_team.append(log_analyzer.Pokemon(pokemon, player1))
				battle.player1.current_pokemon.append(log_analyzer.Pokemon(pokemon, player1))
				battle.all_pokemon.append(log_analyzer.Pokemon(pokemon, player1))
			player1Team = False
		elif battle.player2 and battle.player2.name + "'s team" in line:
			player2Team = True
		elif player2Team:
			team = line.split(" / ")
			for pokemon in team:
				battle.player2.start_team.append(log_analyzer.Pokemon(pokemon, player2))
				battle.player2.current_pokemon.append(log_analyzer.Pokemon(pokemon, player2))
				battle.all_pokemon.append(log_analyzer.Pokemon(pokemon, player2))
			player2Team = False

		
		

def split_turns(middle): 
	#returns a dictionary of number to Turn, starting at 0
	turn_num = 1
	new_turn = ""
	all_turns = {}
	for line in middle:
		if "Turn" not in line:
			new_turn += line
		else:
			all_turns[turn_num] = new_turn
			new_turn = ""
			turn_num += 1
	all_turns[turn_num] = new_turn
	return all_turns

def analyze_turn(number, turn, battle):
	this_turn = log_analyzer.Turn(number, battle.current_pokemon)
	battle.all_turns.append(this_turn)
	battle.turn_number = number
	match_p1_send_out = re.search( r'Go! (.*)!', turn) #This is turn0
	match_p2_send_out = re.search( r'(.*) sent out (.*)!', turn)
	match_mega = re.search( r'(.*) has Mega Evolved into Mega (.*)!', turn)
	match_attack = re.search( r'((.*) used (.*)!)(\n(.*)!)*', turn) #matches the attack and all the consequences
	match_pokemon_fainted = re.search(r'(.*) fainted', turn)
	match_p1_withdraw = re.search(r'(.*), come back!')
	match_p2_withdraw = re.search( r'(.*) withdrew (.*)!', turn)
	if match_p1_send_out:
		for pokemon in battle.player1.team:
			if pokemon.name = match_p1_send_out.group(1):
				this_turn.current_pokemon.append(pokemon)
				this_turn.all_pokemon.append(pokemon)
				break
	if match_p2_send_out:
		for pokemon in battle.player2.team:
			if pokemon.name = match_p2_send_out.group(2):
				this_turn.current_pokemon.append(pokemon)
				this_turn.all_pokemon.append(pokemon)
				break
	if match_mega:
		match_mega_pokemon = match_mega.group(2)
			for pokemon in battle.all_pokemon:
				if pokemon.name == match_mega_pokemon:
					pokemon.mega_evolved = True
					break
	if match_attack:
		entire_attack = match_attack.group(1)
		pokemon_name = match_attack.group(2)
		attack = match_attack.group(3)
		consequences = match_attack.group(4)
		this_turn.actions[entire_attack] = consequences
		if "opposing" in pokemon_name:
			for pokemon in battle.player2.team:
				if pokemon.name == "The opposing" + pokemon_name:
					pokemon.actions[attack] = consequences
					battle.player2.actions[attack] = consequences
					break
		else:
			for pokemon in battle.player1.team:
				if pokemon.name == pokemon_name:
					pokemon.actions[attack] = consequences
					battle.player1.actions[attack] = consequences
					break
	if match_pokemon_fainted:
		fainted_pokemon = match_pokemon_fainted.group(1)
		if "opposing" in fainted_pokemon:
			for pokemon in battle.player2.current_pokemon:
				if "The opposing" + pokemon.name == fainted_pokemon:
					battle.player2.current_pokemon.remove(pokemon)
					this_turn.fainted_pokemon.append(pokemon)
					break
		else:
			or pokemon in battle.player1.current_pokemon:
				if pokemon.name == fainted_pokemon:
					battle.player1.current_pokemon.remove(pokemon)
					this_turn.fainted_pokemon.append(pokemon)
					break






		












def analyze_turn(number, turn, battle):
	part_of_action = False
	current_action = None
	this_turn = log_analyzer.Turn(number, battle.current_pokemon)
	battle.all_turns.append(this_turn)
	battle.turn_number = number
	for line in turn:
		if not line.strip():
			part_of_action = False
		line = line.rstrip('\n')
		matchPlayer1Pokemon = re.match( r'Go! (.*)!', line) #This is turn0
		matchPlayer2Pokemon = re.match( r'(.*) sent out (.*)!', line)
		match_mega = re.match( r'(.*) has Mega Evolved into Mega (.*)!', line)
		if part_of_action:
			create_consequence(current_action, line, current_pokemon, this_turn)
			continue
		for pokemon in battle.current_pokemon:
			match_pokemon_action = re.match( '(The opposing )?' + re.escape(pokemon.name) + ' used (.*)!', line)
			if match_pokemon_action:
				create_action(line, pokemon, this_turn)
				current_action = line
				part_of_action = True
				current_pokemon = pokemon
		if matchPlayer1Pokemon:
			poke_name = matchPlayer1Pokemon.group(1)
			for each_pokemon in battle.player1.team:
				if each_pokemon.name == poke_name:
					battle.current_pokemon.append(each_pokemon)
					break
		elif matchPlayer2Pokemon:
			poke_name = matchPlayer2Pokemon.group(2)
			for each_pokemon in battle.player2.team:
				if each_pokemon.name == poke_name:
					battle.current_pokemon.append(each_pokemon)
					break
		elif match_mega:
			match_mega_pokemon = match_mega.group(2)
			for pokemon in battle.current_pokemon:
				if pokemon.name == match_mega_pokemon:
					pokemon.mega_evolved = True
		# else:
		# 	prev_blank_line = False

#Need a way to add turns efficiently to battle, player and pokemon all at once
#Record the conditions of the battle

# def analyze_turn(number, turn, battle):
# 	part_of_action = False
# 	current_action = None
# 	this_turn = log_analyzer.Turn(number, battle.current_pokemon)
# 	battle.all_turns.append(this_turn)
# 	battle.turn_number = number
# 	matchPlayer1Pokemon = re.match( r'Go! (.*)!', line) #This is turn0
# 	matchPlayer2Pokemon = re.match( r'(.*) sent out (.*)!', line)
# 	match_mega = re.match( r'(.*) has Mega Evolved into Mega (.*)!', line)
# 	if part_of_action:
# 		create_consequence(current_action, line, current_pokemon, this_turn)
# 	for pokemon in battle.current_pokemon:
# 		match_pokemon_action = re.match( '(The opposing )?' + re.escape(pokemon.name) + ' used (.*)!', line)
# 		if match_pokemon_action:
# 			create_action(line, pokemon, this_turn)
# 			current_action = line
# 			part_of_action = True
# 			current_pokemon = pokemon
# 	if matchPlayer1Pokemon:
# 		poke_name = matchPlayer1Pokemon.group(1)
# 		for each_pokemon in battle.player1.team:
# 			if each_pokemon.name == poke_name:
# 				battle.current_pokemon.append(each_pokemon)
# 				break
# 	elif matchPlayer2Pokemon:
# 		poke_name = matchPlayer2Pokemon.group(2)
# 		for each_pokemon in battle.player2.team:
# 			if each_pokemon.name == poke_name:
# 				battle.current_pokemon.append(each_pokemon)
# 				break
# 	elif match_mega:
# 		match_mega_pokemon = match_mega.group(2)
# 		for pokemon in battle.current_pokemon:
# 			if pokemon.name == match_mega_pokemon:
# 				pokemon.mega_evolved = True



def create_action(action, pokemon, turn):
	#records the action of a pokemon and adds to a trainer's and turns
	pokemon.actions[action] = None
	pokemon.trainer.actions[action] = None
	turn.actions[action] = None
def create_consequence(action, consequence, pokemon, turn):
	#records the consequence corresponding to the action and adds to a trainer's and turn's actions
	pokemon.actions[action] = consequence
	pokemon.trainer.actions[action] = consequence
	turn.actions[action] = consequence

def analyze_end(end, battle):
	for line in end:
		pass

class Test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.battle = read_body('Example_Battle_Format.txt')

	def test_both_players(self):
		self.assertEqual(self.battle.player1.name, "redfor")
		self.assertEqual(self.battle.player2.name, "BOON305")
	def test_pokemon_team(self):
		self.assertEqual(self.battle.player2.team[1].name, "Charizard")
		self.assertEqual(self.battle.player2.team[5].name, "Clefairy")
		self.assertEqual(self.battle.player1.team[5].name, "Gourgeist-*")
	def test_clauses(self):
		self.assertTrue(self.battle.conditions)
	def test_mega(self):
		self.assertTrue(self.battle.player2.team[1].mega_evolved)
		self.assertTrue(self.battle.player1.team[4].mega_evolved)
	def test_actions(self):
		print(self.battle.player2.team[1].actions)
		self.assertEqual(self.battle.player2.team[2].actions["The opposing Meowstic used Quick Guard!"], "Quick Guard protected the opposing team!")
		self.assertEqual(self.battle.player1.team[4].actions["Kangaskhan used Fake Out!"], "Quick Guard protected the opposing Meowstic!")
		self.assertEqual(self.battle.player2.team[1].actions)
		#need to fix multiple consequences to one action
		#need to fix multiples of the same actin by the same move and not replacing from a previous turn


read_body('Example_Battle_Format.txt')

	# def testError(self):
	# 	raise RuntimeError('Test error!')

# if __name__ == "__main__":
	# battle = read_body(sys.argv[1])
	# battle = read_body('Example_Battle_Format')
	# unittest.main()



#divide into description, intro, turns, after_battle
#return a Dictionary?
#.... joined
#___________
#Battle between _____ and ____ started!
#___________
#Turn 1
#___________
# redfor lost due to inactivity.
# or 
# BOON305 won the battle!