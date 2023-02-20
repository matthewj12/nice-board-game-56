import socket, pickle, subprocess, time
from constants import *
import boardgamestuff


def hostServerInitConnect(gs, connected):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('192.168.1.201', SERVER_PORT))
	sock.listen(5)
	
	sock, conn_info = sock.accept()
	p = boardgamestuff.Player()
	p.ip_addr, p.port = conn_info
	p_id = str(connected)
	sock.send(str.encode(p_id))
	sock.close()

	gs.players[p_id] = p
	return gs

def clientServerInitConnect(dest_ip):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((dest_ip, SERVER_PORT))
	recv = sock.recv(PACKET_SIZE)
	sock.close()
	our_id = bytes.decode(recv)
	return our_id

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
	sock.close()

#use to get the game state for each payer even when it is not their turn
def recvGameState(source_ip, source_port, pack_size):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((source_ip, source_port))
	sock.listen(5)
	sock, conn_info = sock.accept()

	recv_gs = pickle.loads(sock.recv(pack_size))

	sock.close()
	return recv_gs
