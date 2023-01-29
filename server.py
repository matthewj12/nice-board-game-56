import socket, threading, time

# This can be any port over 1024 that's available on the the server computer and isn't blocked by the network's firewall.
SERVER_PORT = 6100
PACKET_SIZE = 1024 # bytes

# This goes up by one every time a new client connects.
client_counter = 0
# key = IPv4 address string, value = (IPv4 address string, socket.Socket() object) tuple
clients = {}


def findFreePort():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1] + 1


def talkToClientForAWhile(client_sock, client_id):
	global client_ids, server_running

	while True:
		data_from_client = bytes.decode(client_sock.recv(PACKET_SIZE))
		print(f"Client {client_id} sent: {data_from_client}")

		d = input('gimme some data to send to a client in the format "client_id text_to_send": ')
		dest_id, message = d.split(' ')
		print('sending: ' + message)
		clients[dest_id][1].send(str.encode(message))

		# the recv() function returns empty strings after the client disconnects
		if data_from_client == '':
			client_ids.remove(client_id)
			# Terminate the thread
			return


def setupServerAndConnectToClients():
	global client_counter, client_ids, running, server_running, client_socks

	# This is the "daemon" socket that listens for incomming connections from clients. When a client connects to it, a new socket will be created just for that client.
	# AF_INET specifies that we're using IPv4 addresses. 
	# SOCK_STREAM specifies that we want an acknowledge but connectionless 2-way stream of bits to be created and left open indefinitely (e.g., by using TCP).
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# The empty string is a symbolic placeholder value representing the IP address of the current machine.
	server_socket.bind(('', SERVER_PORT))
	server_socket.listen(5)

	while True:
		# Create a new socket just for this client. The accept() function is blocking, meaning that the program will wait here until a new client connects.
		client_sock, conn_info = server_socket.accept()
		client_ip_addr, client_port = conn_info

		next_id = str(client_counter)
		client_counter += 1
		clients[next_id] = (client_ip_addr, client_sock)

		# You can "len(client_ids)"" or "threading.active_count() - 1" to find the number of clients that are currently connected
		print(f"Server has successfully connected to a client at {client_ip_addr} and assigned it an id of {next_id}")

		# Create a new thread to send data to and receive data from the client for as long as the client keeps the connection open. Using multithreading allows the server to talk to multiple clients simultaneously
		t = threading.Thread(target=talkToClientForAWhile, args=(client_sock, next_id))
		t.start()

if __name__ == '__main__':
	setupServerAndConnectToClients()
