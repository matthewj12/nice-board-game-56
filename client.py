import socket


def setupClientAndConnectToServer(ip_addr, port):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((ip_addr, port))

	print('Client has successfully connected to the server :)')

	while True:
		data_to_send = input('gimme some data: ')
		client_socket.send(str.encode(data_to_send))

		data_from_server = bytes.decode(client_socket.recv(1024))
		print(f"Received from server: {data_from_server}")


if __name__ == '__main__':
	setupClientAndConnectToServer('192.168.0.101', 6100)

