import log_analyzer
import sys
import pokemon_classes
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches



def import_file(filename):
	battle = log_analyzer.read_body(filename)
	while True:
		command = input('Command: (type help to see all possible commands) ')
		if command == "help":
			print("All Commands\nprint all actions: Print's all the actions taken in a battle\nprint p1 actions: Print's all of player 1's actions taken in a battle\nprint p2 actions: Print's all of player 2's actions taken in a battle\nprint pokemon actions: Print's all of a pokemon's actions taken in a battle\nall damage: Shows all the damage dealt by each pokemon\npokemon in play: Plots how many pokemon each player has at each turn\nturn actions: Prints the actions of a turn\nplot in battle: Plots how many turns a pokemon is in a battle\nexit")
		elif command == "print all actions":
			print_all_actions(battle)
		elif command == "print p1 actions" or command == "print p2 actions":
			if "p1" in command:
				print_players_actions(battle, battle.player1)
			else:
				print_players_actions(battle, battle.player2)
		elif command == "print pokemon actions":
			pokemon_name = input('Which pokemon? ')
			pokemon = battle.get_pokemon(pokemon_name)
			if not pokemon:
				break
			else:
				print_pokemon_actions(battle, pokemon)
		elif command == "all damage":
			total_damage(battle)
		elif command == "pokemon in play":
			pokemon_in_play(battle)
		elif command == "turn actions":
			turn = input("Which turn: ")
			try:
				turn_int = int(turn)
			except ValueError:
				print("Must input a number")
				break
			if turn_int > battle.turn_number or turn_int < 0:
				print("Invalid turn number")
			else:
				turn_obj = battle.get_turn(turn_int)
				for action in turn_obj.actions:
					print(action)
		elif command == "plot in battle":
			plot_in_play(battle)
		elif command == "exit":
			return
		else:
			print("Invalid Command")




def print_all_actions(battle):
	for turn in battle.all_turns:
		print("Turn: " + str(turn.number) + "\n") 
		for action in turn.actions:
			print(action)

def print_players_actions(battle, player):
	for action in player.actions:
		print(action)

def print_pokemon_actions(battle, pokemon):
	for action in pokemon.actions:
		print(action)
def total_damage(battle):
	all_damage = {}
	to_print = {}
	for pokemon in battle.player1.team + battle.player2.team:
		current_pokemon = battle.get_pokemon(pokemon.name)
		total_damage = 0
		for action in current_pokemon.actions:
			if type(action) == pokemon_classes.Attack:
				for consequence in action.consequences:
					if type(consequence) == pokemon_classes.Damage:
						if type(consequence.damage) == list: #if dmaage is a range ie (34-36)
							if total_damage == 0:
								total_damage = [0, 0]
							total_damage = [current + damage for current, damage in zip(total_damage, range_damage)]
						else:
							total_damage += consequence.damage
		all_damage[pokemon] = total_damage
		to_print[pokemon.name] = total_damage
	
	print(to_print)
	plot = input("Plot? (Y/N)")
	if plot == "Y":
		plot_damage(battle, all_damage)


def plot_damage(battle, damage):
	damage_values = list(damage.values())
	N = len(damage)
	ind = np.arange(N)
	width = 0.35 
	fig = plt.figure()
	fig, ax = plt.subplots()
	barlist = ax.bar(ind, damage_values, width, color = 'r')
	plt.xlabel('Pokemon')
	plt.ylabel('Damage Dealt')
	plt.title('Total damage dealt by each pokemon')
	def autolabel(rects):
    # attach some text labels
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')
	names = [pokemon.name for pokemon in damage.keys()]
	plt.xticks(ind + width / 2, names)
	fig.autofmt_xdate()
	autolabel(barlist)
	index = 0
	for pokemon in damage.keys():
		if pokemon.trainer.number == 1:
			barlist[index].set_color('y')
		index +=1
	p1_patch = mpatches.Patch(color='y', label=battle.player1.name + "'s team")
	
	p2_patch = mpatches.Patch(color='r', label=battle.player2.name + "'s team")
	plt.legend(handles=[p1_patch, p2_patch])
	plt.show()




def pokemon_in_play(battle):
	turns = range(0, battle.turn_number + 1) #x -axis
	p1_team = [0] * len(turns)
	p2_team = [0] * len(turns)
	for turn_num in turns:
		p1_alive = 0
		p2_alive = 0
		turn = battle.get_turn(turn_num)
		for pokemon in battle.player1.team:
			if not turn.get_pokemon(pokemon.name).fainted:
				p1_alive +=1
		for pokemon in battle.player2.team:
			if not turn.get_pokemon(pokemon.name).fainted:
				p2_alive +=1
		p1_team[turn_num] = p1_alive
		p2_team[turn_num] = p2_alive
	p1_line = plt.plot(turns, p1_team, label = battle.player1)
	p2_line = plt.plot(turns, p2_team, label = battle.player2)
	plt.legend()
	plt.axis([0, battle.turn_number + 1, 0, 7])
	plt.ylabel('Number of pokemon in play')
	plt.xlabel('Turn Number')
	plt.show()


def in_play(battle):
	in_play_dict = {}
	total_in_play = {}
	length = len(battle.all_turns)
	for pokemon in battle.player1.team + battle.player2.team:
		i = 0
		count = 0
		for turn in battle.all_turns:
			lst = [0] * length
			if turn.get_pokemon(pokemon.name).in_play:
				lst[i] = True
				count +=1
			else:
				lst[i] = False
			i+=1
		in_play_dict[pokemon] = lst
		total_in_play[pokemon] = count
	return (in_play_dict, total_in_play)

def plot_in_play(battle):
	count_dict = in_play(battle)[1]
	N = len(count_dict)
	ind = np.arange(N)
	width = 0.35 
	fig = plt.figure()
	fig, ax = plt.subplots()
	barlist = ax.bar(ind, count_dict.values(), width, color = 'r')
	plt.xlabel('Pokemon')
	plt.ylabel('Number of turns')
	plt.title('Number of turns in battle')
	x1,x2,y1,y2 = plt.axis()
	plt.axis((x1,x2,y1,len(battle.all_turns)))
	def autolabel(rects):
    # attach some text labels
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')
	names = [pokemon.name for pokemon in count_dict.keys()]
	plt.xticks(ind + width / 2, names)
	fig.autofmt_xdate()
	autolabel(barlist)
	index = 0
	for pokemon in count_dict.keys():
		if pokemon.trainer.number == 1:
			barlist[index].set_color('y')
		index +=1
	p1_patch = mpatches.Patch(color='y', label=battle.player1.name + "'s team")
	
	p2_patch = mpatches.Patch(color='r', label=battle.player2.name + "'s team")
	plt.legend(handles=[p1_patch, p2_patch])
	plt.show()



if __name__ == "__main__":
	filename = input('Filename: ')
	import_file(filename)

