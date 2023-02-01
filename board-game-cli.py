import random


# ---------------- Constants ---------------

# should be 4 as per Iyengar's specification
PLAYER_COUNT = 2
# should be set to 10 as per Iyengar's specification
ROUNDS_PER_GAME = 1
# how many secret numbers each player is given
# should be 3 as per Iyengar's specification
NUM_OF_NUMS = 1
# inclusive. Minimum number is 1.
# must be >= PLAYER_COUNT * NUM_OF_NUMS
# should be 20 as per Iyengar's specification
MAX_NUM = 2

# ------------------------------------------

class Player():
	# string representing an IPv4 address (e.g., '10.34.1.203')
	player_ip_addr = None
	# the Python Socket object used to send data to and receive data from this player
	sock = None
	# string uniquely identifying a Player object that the player enters (if they enter a username that's already being used by another player, they will get an error message)
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
	# tuple of Player objects
	players = None
	# tuple of length 4 containing Player objects
	player_turn_order = None 
	# index refering to a plyer object in player_turn_order whose turn it currently is. Its "their turn" while we're waiting for them to guess a number.
	turn = None
	# integer between 1 and 10 inclusive (or 0 and 9 inclusive)
	current_round = None


def getUniqueRandNums():
	nums = [n+1 for n in range(MAX_NUM)]
	random.shuffle(nums)
	
	return tuple([nums[i] for i in range(NUM_OF_NUMS)])


def getGuessFromPlayer(p_obj, available_nums):
	# Make a deep copy of available_nums
	guessable_nums = [n for n in available_nums]
	for n in p_obj.initial_numbers:
		# Players aren't allowed to guess their own numbers. That wouldn't make sense and would screw up the game and would probably also be pretty cringe 🤢.
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
	# Counting needs to start at one for non computer science plebeian simpletons. 😈
	print(f"------ STARTING ROUND {gs.current_round+1} ------")
	
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

			
def playGame():
	indx = 0
	
	p1 = Player()
	p1.username = 'Matthew T.'
	p1.points = 0

	p2 = Player()
	p2.username = 'Jordan Z.'
	p2.points = 0

	# p3 = Player()
	# p3.username = 'Lindsey C.'
	# p3.initial_numbers = get3RandNums()
	# p3.points = 0
	# p3.guessed_numbers = []

	# p4 = Player()
	# p4.username = 'Daniel M.'
	# p4.initial_numbers = get3RandNums()
	# p4.points = 0
	# p4.guessed_numbers = []

	gs = GameState()
	gs.turn = 0
	gs.current_round = 0
	gs.players = (p1, p2)
	gs.player_turn_order = (p1, p2)


	while gs.current_round < ROUNDS_PER_GAME:
		rand_nums = getUniqueRandNums()

		p1.guessed_numbers = []
		p1.initial_numbers = rand_nums[indx:indx+NUM_OF_NUMS]
		indx += NUM_OF_NUMS

		p2.guessed_numbers = []
		p2.initial_numbers = rand_nums[indx:indx+NUM_OF_NUMS]
		indx += NUM_OF_NUMS
		
		playRound(gs)
	
		gs.current_round += 1


	winner = None
	for p in gs.players:
		if winner == None or p.points > winner.points:
			winner = p


	print("\nGame is finished (Sad!). ")
	print(f"{winner.username} wins with a score of {winner.points} points. Nice job buddy. Keep up the good work!\n")

	print('------ Final results: ------\n')
	print('_____Player_____|_____Score_____')
	for p in gs.players:
		padded_uname = p.username + ' ' * (15 - len(str(p.username)))
		padded_score = ' ' * (14 - len(str(p.points))) + str(p.points)
		print(f"{padded_uname} | {padded_score}")


if __name__ == '__main__':
	playGame()