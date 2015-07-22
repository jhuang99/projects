import pokemon_classes
import re
import unittest
import sys


def read_body(filename):
	log_file = open(filename, "r") #opens the text_file
	battle = pokemon_classes.Battle() 
	start = [] #the lines associated before the first turn
	middle = []	#lines associated with each turn
	end = [] #lines associated after the battle is over
	turnsStarted = False
	battleOver = False
	for line in log_file: #splits the lines into start, middle, end
		if not turnsStarted:
			if  "Go!" not in line:
		   		start.append(line)
		   		continue
			else:
		   		turnsStarted = True
		if not battleOver:
			if "won" not in line and "lost due to inactivity" not in line and "forfeited" not in line:
				middle.append(line)
				continue
			else:
				end.append(line)
				battleOver = True
		else:
			end.append(line)
	analyze_start(start, battle)
	string_turns = split_turns(middle)
	for turn in string_turns:
		analyze_turn(turn, string_turns[turn], battle)
	analyze_end(end, battle)

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
				player1 = pokemon_classes.Player(matchPlayer.group(1), 1)
			else:
				player2 = pokemon_classes.Player(matchPlayer.group(1), 2)
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
				pokemon_object = pokemon_classes.Pokemon(pokemon, player1)
				battle.player1.team.append(pokemon_object)
			player1Team = False
		elif battle.player2 and battle.player2.name + "'s team" in line:
			player2Team = True
		elif player2Team:
			team = line.split(" / ")
			for pokemon in team:
				pokemon_object = pokemon_classes.Pokemon(pokemon, player2)
				battle.player2.team.append(pokemon_object)
			player2Team = False

		
		

def split_turns(middle): 
	#returns a dictionary of number to Turn, starting at 0
	turn_num = 0
	new_turn = ""
	string_turns = {}
	for line in middle:
		if "Turn" not in line:
			new_turn += line
		else:
			string_turns[turn_num] = new_turn
			new_turn = ""
			turn_num += 1
	string_turns[turn_num] = new_turn
	return string_turns

def analyze_turn(number, turn, battle):
	pokemon_classes.Action.reset()
	switch = False
	this_turn = pokemon_classes.Turn(number)
	battle.all_turns.append(this_turn)
	battle.turn_number = number
	if number != 0:
		for pokemon in battle.all_turns[number - 1].p1_pokemon: 
			this_turn.p1_pokemon.append(pokemon.copy(this_turn)) #should deep copy pokemon from previous turn
		for pokemon in battle.all_turns[number - 1].p2_pokemon:
			this_turn.p2_pokemon.append(pokemon.copy(this_turn))
	else: #for turn 0, copies pokemon from starting team
		for pokemon in battle.player1.team:
			this_turn.p1_pokemon.append(pokemon.copy(this_turn))
		for pokemon in battle.player2.team:
			this_turn.p2_pokemon.append(pokemon.copy(this_turn))
	divided_turn = re.split("\n\n", turn) #splits each turn into each action
	for line in divided_turn: 
		match_p1_send_out = re.finditer( r'Go! ([^\(\n]*)(\s)?(\((.*)\))?!', line) #sending out pokemon player 1
		match_p2_send_out = re.finditer( r'(.*) sent out ([^\(\n]*)(\s)?(\((.*)\))?!', line)
		match_mega = re.finditer( r'(.*) has Mega Evolved into Mega (.*)!', line)
		match_attack = re.finditer( r'((.*) used (.*)!)((\n(.*)!)+)', line) #matches the attack and all the consequences
		match_pokemon_fainted = re.finditer(r'(.*) fainted', line)
		match_p1_withdraw = re.finditer(r'([^\(]*)(\s)?(\((.*)\))?, come back!', line)
		match_p2_withdraw = re.finditer( r'(.*) withdrew ([^\(]*)(\s)?(\((.*)\))?!', line)
		match_u_turn = re.finditer(r'(The opposing)?(\s)?(.*) went back to (.*)!', line)
		for match in match_mega:
			match_mega_pokemon = match.group(2)
			match_pokemon = this_turn.get_pokemon(match_mega_pokemon)
			match_pokemon.mega_evolved = True

		for match in match_pokemon_fainted:
			fainted_pokemon = match.group(1)
			if fainted_pokemon.startswith("The opposing "):
				fainted_pokemon = fainted_pokemon.split("opposing ")[1]
				match_pokemon = this_turn.get_pokemon(fainted_pokemon, 2)
				match_pokemon.faint(this_turn)
			else:
				match_pokemon = this_turn.get_pokemon(fainted_pokemon, 1)
				match_pokemon.faint(this_turn)

		for match in match_p1_withdraw: 
			nickname = match.group(1).strip()
			pokemon_name = match.group(4)
			if pokemon_name: 
				nickname = nickname.rstrip()
				this_turn.get_pokemon(pokemon_name, 1).nickname = nickname
				pokemon_name = nickname
			switch = True
			switched_poke = this_turn.get_pokemon(nickname, 1)
			switched_poke.in_play = False
		for match in match_p2_withdraw:
			nickname = match.group(2)
			pokemon_name = match.group(5)
			if pokemon_name: 
				nickname = nickname.rstrip()
				this_turn.get_pokemon(pokemon_name, 2).nickname = nickname
				pokemon_name = nickname
			switch = True
			switched_poke = this_turn.get_pokemon(nickname, 2)
			switched_poke.in_play = False
		for match in match_p1_send_out:
			nickname = match.group(1)
			send_pokemon = match.group(4)
			if send_pokemon:
				nickname = nickname.rstrip()
				this_turn.get_pokemon(send_pokemon, 1).nickname = nickname
			pokemon = this_turn.get_pokemon(nickname, 1)
			if switch:
				switch_action = pokemon_classes.Switch(battle, this_turn, battle.player2, switched_poke, pokemon)
				add_action(switch_action, this_turn, battle.player2)
				switch = False
			else:
				pokemon.in_play = True

			
		for match in match_p2_send_out:

			nickname = match.group(2)
			send_pokemon = match.group(5)
			if send_pokemon:
				nickname = nickname.rstrip() #gets rid of space at end if there is one
				this_turn.get_pokemon(send_pokemon, 2).nickname = nickname
			pokemon = this_turn.get_pokemon(nickname, 2)
			if switch:
				switch_action = pokemon_classes.Switch(battle, this_turn, battle.player1, switched_poke, pokemon)
				# print(s)
				add_action(switch_action, this_turn, battle.player2)
				switch = False
			else:
				pokemon.in_play = True
			
		

		for match in match_attack:
			#create a new Action
			entire_attack = match.group(1)
			pokemon_name = match.group(2)
			attack = match.group(3)
			consequences = match.group(4).strip()
			if pokemon_name.startswith("The opposing "):
				attacking_pokemon = pokemon_name.split("opposing ")[1]
				attacking_pokemon = this_turn.get_pokemon(attacking_pokemon, 2)
				attack_action = pokemon_classes.Attack(battle, this_turn, battle.player2, attacking_pokemon, attack, consequences)
				add_action(attack_action, this_turn, battle.player2, attacking_pokemon)
			else:
				attacking_pokemon = this_turn.get_pokemon(pokemon_name, 1)
				attack_action = pokemon_classes.Attack(battle, this_turn, battle.player1, attacking_pokemon, attack, consequences)
				add_action(attack_action, this_turn, battle.player1, attacking_pokemon)
		
		for match in match_u_turn:
			pokemon_name = match.group(3)
			pokemon = this_turn.get_pokemon(pokemon_name)
			pokemon.in_play = False


def analyze_end(end, battle):
	for line in end:
		match_inactivity = re.match( r'(.*) lost due to inactivity.', line)
		match_forfeit = re.match( r'(.*) forfeited.', line)
		match_won = re.match( r'(.*) won the battle!', line)
		if match_inactivity:
			battle.end_result = "inactivity"
			if match_inactivity.group(1) == battle.player1.name:
				battle.winner = battle.player2
			else:
				battle.winner = battle.player1
		elif match_forfeit:
			battle.end_result = "forfeit"
			if match_inactivity.group(1) == battle.player1.name:
				battle.winner = battle.player2
			else:
				battle.winner = battle.player1

def add_action(action, turn, player, pokemon = None):
	turn.add_action(action)
	player.add_action(action)
	if pokemon:
		pokemon.add_action(action)


class Test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.battle = read_body('Example_Battle_Format.txt')
		cls.battle2 = read_body( 'Sample_Battle_with_Nicknames.txt')
		cls.battle3 = read_body( 'Example_Battle_3.txt')
		# cls.battle4 = read_body('Battle_4.txt')
		cls.battle5 = read_body('Battle 5.txt')

	def test_both_players(self):
		self.assertEqual(self.battle.player1.name, "redfor")
		self.assertEqual(self.battle.player2.name, "BOON305")
		self.assertEqual(self.battle2.player1.name, "E4 Landorus")
		self.assertEqual(self.battle2.player2.name, "Meganium Trainor")

	def test_pokemon_team(self):
		self.assertEqual((len(self.battle.player1.team)), 6)
		self.assertEqual(self.battle.player2.team[1].name, "Charizard")
		self.assertEqual(self.battle.player2.team[5].name, "Clefairy")
		self.assertEqual(self.battle.player1.team[5].name, "Gourgeist-Super")
		self.assertEqual(self.battle2.player1.team[0].name, "Swampert")
		self.assertEqual(self.battle2.player1.team[5].name, "Excadrill")
		self.assertEqual(self.battle2.player2.team[3].name, "Gardevoir")


	def test_clauses(self):
		self.assertTrue(self.battle.conditions)

	def test_mega(self):
		self.assertTrue(self.battle.get_turn(1).get_pokemon("Kangaskhan", 1).mega_evolved) #make sure Kanghaskan mega_evolved
		self.assertTrue(self.battle.get_turn(2).get_pokemon("Kangaskhan", 1).mega_evolved)
		self.assertFalse(self.battle.get_turn(0).get_pokemon("Kangaskhan", 1).mega_evolved)

	def test_print_turn_actions(self):
		for turn in self.battle3.all_turns:
			print("Turn: " + str(turn.number) + "\n") 
			for action in turn.actions:
				print(action)
	
	def test_fainted(self):
		self.assertTrue(self.battle.get_turn(2).get_pokemon("Kangaskhan", 1).fainted)
		self.assertFalse(self.battle.get_turn(2).get_pokemon("Kangaskhan", 1).in_play)
		self.assertTrue(self.battle.get_turn(3).get_pokemon("Kangaskhan", 1).fainted)
		self.assertFalse(self.battle.get_turn(2).get_pokemon("Meowstic", 2).fainted)
		# self.assertEqual(self.battle.get_turn(2).get_action(2).defeated.name, "Kangaskhan") 
		# self.assertEqual(self.battle.get_turn(2).get_action(3).defeated, "") 
		# self.assertTrue(self.battle.get_turn(3).get_pokemon("Charizard", 2).fainted)
		
	def test_switch(self):
		self.assertFalse(self.battle.get_turn(2).get_pokemon("Meowstic", 2).in_play)
		self.assertTrue(self.battle.get_turn(2).get_pokemon("Clefairy", 2).in_play)
		self.assertFalse(self.battle.get_turn(3).get_pokemon("Meowstic", 2).in_play)
		self.assertTrue(self.battle.get_turn(3).get_pokemon("Clefairy", 2).in_play)
		self.assertTrue(self.battle.get_turn(0).get_pokemon("Kangaskhan", 1).in_play)

	def test_winner(self):
		self.assertEqual(self.battle.winner.name, "BOON305")
		self.assertEqual(self.battle.end_result, "inactivity")

	def test_pokemon_copies(self):
		self.assertEqual(self.battle.get_turn(2).get_pokemon("Meowstic", 2), self.battle.get_turn(3).get_pokemon("Meowstic", 2).prev_copy)
		self.assertEqual(self.battle.player2.team[1].prev_copy, None)

	def test_action(self):
		self.assertEqual(len(self.battle.get_turn(1).actions), 4)
		self.assertEqual(self.battle.get_turn(1).get_action(4).pokemon.name, "Gourgeist-Super") 
		self.assertEqual(len(self.battle.get_turn(3).get_pokemon("Charizard", 2).actions), 2)
		self.assertEqual(len(self.battle.get_turn(1).get_pokemon("Charizard", 2).actions), 1)
		self.assertEqual(len(self.battle2.get_turn(1).actions), 2)
		# self.assertEqual(self.battle.get_turn(1).get_pokemon("Charizard", 2).actions[0].consequence, "Kangaskhan lost 60.5–62.5% of its health!\nGourgeist-Super avoided the attack!")

	def test_damage(self):
		self.assertEqual(self.battle.get_turn(3).get_pokemon("Charizard", 2).health, [68.7, 66.7])
		self.assertEqual(self.battle.get_turn(1).get_pokemon("Charizard", 2).health, 100)
		self.assertEqual(self.battle.get_turn(3).get_pokemon("Kangaskhan", 1).health, 0)
		self.assertEqual(self.battle.get_turn(1).get_pokemon("Kangaskhan", 1).health, [39.5, 37.5])

	# def test_player_actions(self):
	# 	for action in self.battle2.player1.actions:
	# 		print(action)
	# 	for action in self.battle2.player2.actions:
	# 		print(action)

	def test_pokemon_actions(self):
		pass

#should match attack that led to a faint





if __name__ == "__main__":
	unittest.main()
