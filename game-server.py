import socket, threading, selectors, os, random,time
from _thread import *


# game stuff
# game description a 1 match, 10 games, rounds based on how many guesses it takes to win
def start_numbers():  # creates the 3 random numbers for each players
    randlist = random.sample(range(1, 20), 12)
    return [[randlist[0], randlist[1], randlist[2]], [randlist[3], randlist[4], randlist[5]],
            [randlist[6], randlist[7], randlist[8]], [randlist[9], randlist[10], randlist[11]]]


wins = [0, 0, 0, 0]  # keeps track of each players amount of wins
score = [0, 0, 0, 0]  # keeps track of each players score
matched = [['t', 'f', 'f', 'f'], ['f', 't', 'f', 'f'], ['f', 'f', 't', 'f'],
           ['f', 'f', 'f', 't']]  # who each player has guesse 0,1,2,3
guesses = [[], [], [], []]  # guesses each player has entered


def matches_found(guesses, startNums):  # checks after each round if any player has guessed another players number then sets matched to
    # t if player has guessed
    for x in range(4):
        for y in range(4):
            if all(z in guesses[x] for z in startNums[y]):
                matched[x][y] = 't'
    return matched  # set the new matched to this


def winnerCheck(matched):  # go through all and count to see if anyone has 4 t's for a win
    counter = 0
    for x in range(1):#1
        for y in range(1):
            if matched[x][y] == 't':
                counter += 1
        if counter == 1:
            return True
        counter = 0


def totalWinCheck():  # see who the overall winner is
    min_val = min(score)
    score_indices = []
    win_indices = []
    for x in  range(4):# go through scores and add the min value to this list
        if score[x] == min_val:
            score_indices.append(x)
    if len(score_indices) <= 1:
        return score_indices[0]  # winner winner chicken dinner
    else:
        max_win = max(wins)
        for index in len(score_indices):  # go through scores and add the min value to this list
            if wins[index] == max_win:  # keep track of max winner
                win_indices.append(index)
        if len(score_indices) <= 1:  # return max winner index
            return score_indices[0]
        else:
            return "tie"


# socket set up stuff#################################################################################################
host = ''  # local ipv4
port = 2004
PACKET_SIZE = 1024  # bytes
client_counter = 0
# key = IPv4 address string, value = (IPv4 address string, socket.Socket() object) tuple
clients = {}  # dictionary


def findFreePort():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1] + 1


def multi_threaded_client(connection):  # used?
    global client_ids
    connection.send(str.encode('Server is working:'))

    while True:
        data = connection.recv(2048)
        print(data.decode('utf-8'))
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()


def talkToClientForAWhile(client_sock, client_id):  # where the client is talking to server
    while True:
        clients[client_id][1].send(str.encode("Welcome player" + client_id))
        data_from_client = bytes.decode(client_sock.recv(PACKET_SIZE))
        d = input('gimme some data to send to a client in the format "client_id text_to_send": ')
        dest_id, message = d.split(' ')
        print(dest_id)
        print(message)
        print(d)
        print('sending: ' + message)
        clients[dest_id][1].send(str.encode(message))  # format id

        # the recv() function returns empty strings after the client disconnects
        if data_from_client == '':
            client_ids.remove(client_id)
            # Terminate the thread
            return


def multiplayergame(client_sock, client_id):
    games = 1
    win = False
    while client_counter < 4:#4 # wait for 4 players
        pass

    while games <= 2:  # match ending
        # set up for each game
        # sending stuff to fast and it gets lost!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        startNums = start_numbers()  # gives starting nums
        turn = 0 # whose turn it is
        rounds = 1
        for x in range(1): # 4
            strstart  = str(startNums[x])
            clients[str(x)][1].send(str.encode("SN " + strstart)) # starting numbers
            time.sleep(1) #try and slow down so it doesn't send sg right away
        while not win:  # while a game is still going
            clients[str(turn)][1].send(str.encode("SG"))  # send guess request to current players turn
            guess = bytes.decode(client_sock.recv(PACKET_SIZE))  # the users guess
            #second run through goes to fast and doesn't allow for user to enter
            guesses[turn].append(int(guess))  # add users guess to their spot in list guesses
            matched = matches_found(guesses, startNums)  # check if anyone has matches
            matchedstr = str(matched)  # matches gets turn into string
            for x in range(4):#4
                clients[str(x)][1].send(str.encode("BS " + matchedstr))  # send board state to all players
            win = winnerCheck(matched)  # if winnner end this game winner is determined on their turn
            if turn < 4 and not win:  # if not gone through whole round increase player
                turn += 1
            else:
                if not win:
                    rounds += 1
                    turn = 0
        # send points for all, send wins for all
        score[turn] += rounds # the score of the winner is how many rounds it took
        wins[turn] += 1  # increase wins for winner of game
        for z in range(4):#4  # for all other players give them the turn amount + 10
            if not z == turn:
                score[z] += turn + 10
        games += 1  # one more games been played
        win = False  # reset the win condition
        strscore = str(score)  # turn keeps track of who won that game, score, and wins
        for x in range(4):#4
            clients[str(x)][1].send(str.encode("SC " + strscore)) # send score
            time.sleep(1)
            #end game  send score and wins to all players client will split into a list to read
        for x in range(4):#4
            time.sleep(1)
            clients[str(x)][1].send(str.encode("GW " + str(wins))) # send games won
    # send winner of games to all
    for x in range(4):#4
        winner = str(totalWinCheck())
        clients[str(x)][1].send(str.encode("W " + winner))  # winnner of all send current winner to all


# global client_counter, client_ids, running, server_running, client_socks
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# The empty string is a symbolic placeholder value representing the IP address of the current machine.
server_socket.bind(('', port))
server_socket.listen(5)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
# print ip_address
print(f"IP Address: {ip_address}")
while True:  # accept clients to connect and generate unique id and add to client{}
    if client_counter < 4:  # NEED TO ADD CHECK for 4 players
        client_sock, conn_info = server_socket.accept()
        client_ip_addr, client_port = conn_info
        next_id = str(client_counter)
        client_counter += 1

        clients[next_id] = (client_ip_addr, client_sock,)
        print(f"Server has successfully connected to a client at {client_ip_addr} and assigned it an id of {next_id}")
        # Create a new thread to send data to and receive data from the client for as long as the client keeps the
        # connection open. Using multithreading allows the server to talk to multiple clients simultaneously
        t = threading.Thread(target=multiplayergame, args=(client_sock, next_id))
        t.start()
