from state import State
from player import Player
from DQLAgent import DQLAgent

ROWS = 8
COLUMNS = 8
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

p1 = Player("p1")
p2 = Player("p2")
state_shape = (ROWS, COLUMNS, 3)  # Three channels for empty spaces, player 1, and player 2
action_size = COLUMNS  # Number of possible columns to drop a piece
agent = DQLAgent(state_shape, action_size)

st = State(p1, p2)
print("training...")

st.play()

p1.savePolicy()

print(p1.states_value)
print(p2.states_value)


