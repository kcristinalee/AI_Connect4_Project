from state import State
from player import Player

p1 = Player("p1")
p2 = Player("p2")

st = State(p1, p2)
print("training...")

st.play()


