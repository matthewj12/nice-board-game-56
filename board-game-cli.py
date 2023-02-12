import random, socket, threading, pickle
import time


# ---------------- Constants ---------------

# This can be any port over 1024 that's available on the the server computer and isn't blocked by the network's firewall.
SERVER_PORT = 6100
PACKET_SIZE = 99999 # bytes

# should be 4 as per Iyengar's specification
PLAYER_COUNT = 2
# should be set to 10 as per Iyengar's specification
ROUNDS_PER_GAME = 1
# how many secret numbers each player is given
# should be 3 as per Iyengar's specification
NUM_OF_NUMS = 3
# MAX_NUM is inclsuve. The minimum number is 1.
# should be 20 as per Iyengar's specification
MAX_NUM = 20

assert MAX_NUM >= PLAYER_COUNT * NUM_OF_NUMS, 'bruh'

# ------------------------------------------

class Connection():
	# string representing an IPv4 address (e.g., '10.34.1.203')
	ip_addr = None
	# integer
	port = None
	# the Python Socket object used to send/receive data to/from this player
	sock = None

	def __init__(self, ip_addr, port, sock):
		self.ip_addr = ip_addr
		self.port = port
		self.sock = sock


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



def main():
	# This function is called by each client.
	# ip_addr is None for players who aren't playing as the server. For the server player, it is set to their IP address since we already know it.
	def clientThread(server_ip_addr):
		if server_ip_addr == None:
			server_ip_addr = input("Enter the server's IP address: ")

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((server_ip_addr, SERVER_PORT))

		# Get our id from the server. This is the only time we send data that isn't a serialized GameState object. The reason we're sending/receiving only the username is because sending the game state would be pointless as the client would have no way to know which player object belongs to it.
		our_id = bytes.decode(sock.recv(PACKET_SIZE))
		# This is discarded by the server
		sock.send(str.encode('I received my id. Thanks.'))

		# change the username of the Player object corresponding to us.
		recv_data = sock.recv(PACKET_SIZE)
		gs = pickle.loads(recv_data)
		gs.players[our_id].username = input('tell me username now: ')
		sock.send(pickle.dumps(gs))

		# the rest of the code in this function is just for testing purposes.
		us = gs.players[our_id]
		print(f"{us.username}'s numbers: {''.join([str(n) + ', ' for n in us.initial_numbers])}")

		while True:
			pass




	# Only one of these threads runs on the server.
	def serverParentThread():
		# gs stands for "game state"
		gs = GameState()
		gs.turn = 0
		gs.current_round = 1
		gs.players = {}
		client_counter = 0

		# serverMainThread() spawns one of these threads for each new client.
		def serverChildThread(conn, player_id): # conn = Connection object
			nonlocal gs

			conn.sock.send(str.encode(player_id))
			# The return value of recv() is unused. We need to call it anyways for synchronization purposes.
			conn.sock.recv(PACKET_SIZE)
			conn.sock.send(pickle.dumps(gs))
			updated_gs = conn.sock.recv(PACKET_SIZE)
			time.sleep(0.1)
			print('server received updated game state')
			gs = pickle.loads(updated_gs)

			# the rest of the code in this function is just for testing purposes.
			while True:
				pass
		
		# This is the socket that listens for incoming connections from clients. This is NOT the socket that sends/receives data to/from clients.
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# The empty string is a symbolic placeholder value representing the IP address of the current machine.
		server_socket.bind(('', SERVER_PORT))
		server_socket.listen(5)

		while len(gs.players) < PLAYER_COUNT:
			sock, conn_info = server_socket.accept()
			c = Connection(ip_addr=conn_info[0], port=conn_info[1], sock=sock)

			p = Player()
			p.initial_numbers = getUniqueRandNums()
			client_id = str(client_counter)
			client_counter += 1

			gs.players[client_id] = p

			t = threading.Thread(target=serverChildThread, args=(c, client_id))
			t.start()

		def playersWithNoUsername():
			count = 0

			for p in gs.players.values():
				if p.username == None:
					count += 1
			
			return count

		# wait until every player has entered their username
		while playersWithNoUsername() > 0:
			pass


		# the rest of the code in this function is just for testing purposes.
		gs.printIt()


	our_ip_addr = socket.gethostbyname(socket.gethostname())
	is_server = input('Do you want to play as the server? (y/n): ') == 'y'

	if is_server:
		print(f"server's IP address: {our_ip_addr}")
		t = threading.Thread(target=serverParentThread, args=())
		t.start()

	clientThread(our_ip_addr if is_server else None)


	# Terminate early because I don't know what will happen if we don't because I haven't modified the rest of the code for networked multiplayer.
	quit()


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
	main()
