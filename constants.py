# This can be any port over 1024 that's available on the the server computer and isn't blocked by the network's firewall.
SERVER_PORT = 6100
PACKET_SIZE = 99999 # bytes

# should be 4 as per Iyengar's specification
PLAYER_COUNT = 4
# should be set to 10 as per Iyengar's specification
ROUNDS_PER_GAME = 10
# how many secret numbers each player is given
# should be 3 as per Iyengar's specification
NUM_OF_NUMS = 3
# MAX_NUM is inclsuve. The minimum number is 1.
# should be 20 as per Iyengar's specification
MAX_NUM = 20

assert MAX_NUM >= PLAYER_COUNT * NUM_OF_NUMS, 'bruh'
