import random
from constants import *
from networking import *

'''
This module contains classes and functions comprising the "backend" of the "Super Set Me!" video game's program. That is, the stuff relating to the actual board game being played. This is the "business" logic, if you will.
'''

class Player():
	# is a string (need to change name to reflect this)
	id_num = None
	username = None
	# tuple of length 3
	initial_numbers = None
	# list with 0 to 20 inclusive elements. Only applies to the current round.
	guessed_numbers = None
	# integer between 0 and 10 inclusive
	rounds_won = None
	# integer. Applies throughout all 10 rounds in the game. 
	points = None


class GameState():
	# dictionary of player objects
	players = None
	# tuple of length 4 containing Player objects
	player_turn_order = None 
	# index refering to a plyer object in player_turn_order whose turn it currently is. Its "their turn" while we're waiting for them to guess a number.
	turn = None
	# integer between 1 and 10 inclusive (or 0 and 9 inclusive)
	current_round = None

	def printIt(self):
		print()
		print('turn: ' + str(self.turn))
		print('current round: ' + str(self.current_round))
		print('players: ' + ''.join([p.username + ', ' for p in self.players.values()]))
		print()


available_nums = [n+1 for n in range(MAX_NUM)]
random.shuffle(available_nums)

def getUniqueRandNums():
	global available_nums

	to_return = available_nums[:NUM_OF_NUMS]
	available_nums = available_nums[NUM_OF_NUMS:]

	return to_return


def getGuessFromPlayer(p_obj, available_nums):
	# Make a deep copy of available_nums
	guessable_nums = [n for n in available_nums]
	for n in p_obj.initial_numbers:
		# Players aren't allowed to guess their own numbers. That wouldn't make sense and would screw up the game.
		if n in guessable_nums:
			guessable_nums.remove(n)

	print(f"\nNumbers to choose from: {guessable_nums}")

	guess = -1

	while guess == -1 or guess not in available_nums or guess not in guessable_nums:
		guess = int(input(f"Enter your guess {p_obj.username}: "))

	return guess


# returns true if a is a superset of b
def isSupersetOf(a, b):
	for n in b:
		if not n in a:
			return False

	return True


def playerXHasWon(gs, x):
	for p in gs.players:
		if p.username != x.username and not isSupersetOf(x.guessed_numbers, p.initial_numbers):
			return False

	return True
		

def playRound(gs):
	print(f"------ STARTING ROUND {gs.current_round} ------")
	
	for p in gs.players:
		s = ''.join((f"{n}, " for n in p.initial_numbers))
		print(f"{p.username}'s nums: {s}")
	
	unguessed_nums = [i+1 for i in range(MAX_NUM)]

	winner = None
	round_over = False
	while not round_over:
		p_obj = gs.player_turn_order[gs.turn]
		guess = getGuessFromPlayer(p_obj, unguessed_nums)

		for q_obj in gs.players:
			if q_obj.username != p_obj.username and guess in q_obj.initial_numbers:
				print(f"You got a number in {q_obj.username}'s set!")

		unguessed_nums.remove(guess)
		p_obj.guessed_numbers.append(guess)

		if playerXHasWon(gs, x=p_obj):
			round_over = True
			winner = p_obj

		# Wrap around to the first player if necessary
		gs.turn = (gs.turn + 1) % len(gs.players)

	print(f"\n{winner.username} has won the round. Congratulations to played who played and gave it their all! Until next time...")
	print(f"{winner.username} gets {sum(winner.guessed_numbers)} points (Awesome!). Everyone else gets 10 points (Sad!).")
	winner.points += sum(winner.guessed_numbers)

	# Everyone gets some points because everyone is a winner!
	for p in gs.players:
		if p.username != winner.username:
			p.points += 10

