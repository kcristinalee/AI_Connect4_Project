from state import State
from player import Player

class HumanPlayer:

    def __init__(self, name, player_num=1):
        self.name = name
        self.player_num = player_num

    def chooseAction(self, actions, board):

        while True:
            col = int(input("Input your action col:"))

            if any(col == a[1] for a in actions):
                return self.player_num, col
            else:
                print('Try again')

    # functions so we can call players equally - may not need these?

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    policy = 'policy_p1'

    p1 = HumanPlayer('human')

    p2 = Player('ai', exp_rate=0)
    p2.loadPolicy(policy)

    print('You are Player 1! You go first...')
    st = State(p1, p2)
    st.playHuman()
