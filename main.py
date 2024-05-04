from state import State
from player import Player
from DQLAgent import DQLAgent

# Defining game parameters
ROWS = 8
COLUMNS = 8
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

# Creating players
p1 = Player("p1")
p2 = Player("p2")

# Initializing DQL agent
state_shape = (ROWS, COLUMNS, 3)  # Three channels for empty spaces, player 1, and player 2
action_size = COLUMNS  # Number of possible columns to drop a piece
agent = DQLAgent(state_shape, action_size)

# Initializing state
st = State(p1, p2)

# Training model
print("training...")
st.play()

# Saving new policy
p1.savePolicy()

# Printing final state values
print(p1.states_value)
print(p2.states_value)