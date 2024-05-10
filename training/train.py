from core.state import State
from core.player import Player


num_episodes = 100000

# Creating players
p1 = Player("p1")
p2 = Player("policy")

# Initializing state
st = State(p1, p2)

# Training model
print("training...")
st.play(num_episodes)

# Saving new policy
p2.savePolicy()

print('saved policy')