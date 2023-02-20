import socket, pickle, subprocess, time
from constants import *
from boardgamestuff import *
clientcounter = 0
#we use this to connect each time we want to send or receive something
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

def hostServerInitConnect(gs):
	global clientcounter	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('', SERVER_PORT))
	sock.listen(5)
	
	sock, conn_info = sock.accept()
	p = Player()
	p.ip_addr, p.port = conn_info
	p_id = str(clientcounter)
	sock.send(str.encode(p_id))
	sock.close()
	clientcounter += 1

	gs.players[p]
	return p_id, gs

def clientServerInitConnect(dest_ip):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((dest_ip, SERVER_PORT))
	recv = sock.recv(PACKET_SIZE)
	our_id = bytes.decode(recv)
	
	print('connected')

def getIPaddr():
	try:
		return socket.gethostbyname(socket.gethostname())
	except Exception:
		out = subprocess.check_output(['ifconfig'])

		i = 0
		ip_addr = ''
		blobs = str(out).split(' ')
		for blob in blobs:
			if 'en0' in blob:
				ip_addr = blobs[i+7]
			i += 1

		return ip_addr


#use to send game state to server
def sendGameState(dest_ip, dest_port, pack_size, gs):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((dest_ip, dest_port))

	sock.send(pickle.dumps(gs))
	sock.recv(pack_size)

	sock.close()

#use to get the game state for each payer even when it is not their turn
def recvGameState(source_ip, source_port, pack_size):
	sock = socket.socket(socket.AF_INSET, socket.SOCK_STREAM)
	sock.bind((source_ip, source_port))
	socket.listen(5)
	socket.accept()

	recv_gs = pickle.loads(sock.recv(pack_size))
	sock.send('Receive successful')

	sock.close()


if __name__ == '__main__':
	print(getIPaddr())
