import socket
#game stuff
wins = [0,0,0,0]
score = [0,0,0,0]
myNumbers = []



#socket stuff
ClientMultiSocket = socket.socket()
#host = '127.0.0.1'
host = '192.168.1.117' # local ipv4
port = 2004
print('Waiting for connection response')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

print('Client has successfully connected to the server :)')
while True:
    # check each string to see what server is trying to do
    #if statements
    data_from_server = bytes.decode(client_socket.recv(1024))
    print(data_from_server)
    split_data = data_from_server.split(" ")
    if split_data[0] == 'SN': # if the data is SN a starting number
        snlist = data_from_server.strip('SN [').strip(']').split(', ') # get all numbers from data from server turn to int list
        myNumbers = [eval(i) for i in snlist] # turn prior list all into int
        print("My numbers are " + str(myNumbers))
    elif split_data[0] == 'SG': #allow user to send their guess of other players
        data_to_send = input('Send your guess!')
        client_socket.send(str.encode(data_to_send))
    elif split_data[0] == 'BS': # if the data is  BSboard state
        bslist = data_from_server.strip('BS [').strip(']').split(', ') # get all numbers from data from server turn to 2d list
        print(bslist)
        bslist = str(bslist).replace('"', '')
        bslist = eval(bslist) # becomes tuple now but kinda works
        print(f"Received from server: {data_from_server}")
    elif split_data[0] == 'SC': # if data is SC send scores of all
        sclist = data_from_server.strip('SC [').strip(']').split(', ')
        sclist = str(sclist).replace('"', '')
        score = eval(sclist) # becomes tuple now but kinda works
        print(f"Received from server: {data_from_server}")
    elif split_data[0] == 'GW': # if data is GW sends games won for all
        gwlist = data_from_server.strip('GW [').strip(']').split(', ')
        gwlist = str(gwlist).replace('"', '')
        wins = eval(gwlist) # becomes tuple now but kinda works
    elif split_data[0] == 'W': # find out who won the match
        print(f"Received from server: {data_from_server}")
        print("Winner is player " + split_data[1] + "!" )