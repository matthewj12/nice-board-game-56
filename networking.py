import socket, pickle


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

def getIPaddr():
	return socket.gethostbyname(socket.gethostname())


def sendGameState(dest_ip, dest_port, pack_size, gs):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((dest_ip, dest_port))

	sock.send(pickle.dumps(gs))
	sock.recv(pack_size)

	sock.close()

def recvGameState(source_ip, source_port, pack_size):
	sock = socket.socket(socket.AF_INSET, socket.SOCK_STREAM)
	sock.bind((source_ip, source_port))
	socket.listen(5)
	socket.accept()

	recv_gs = pickle.loads(sock.recv(pack_size))
	sock.send('Receive successful')

	sock.close()