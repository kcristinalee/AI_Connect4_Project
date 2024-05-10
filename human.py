from core.state import State
from core.player import Player


class HumanPlayer:

    def __init__(self, name, player_num=1):
        self.name = name
        self.player_num = player_num

    def chooseAction(self, actions, board):
        # Taking in human input through command line
        while True:
            # Prompting for input
            col = int(input("Input your action col:"))
            # Checking validity of input
            if any(col == a[1] for a in actions):
                # Preforming move
                return self.player_num, col
            else:
                # Printing error message
                print('Try again')

    # Alternate version for choose action that uses the frontend
    def chooseActionF(self, col, board):
        return self.player_num, col

    # Passing functions
    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass

# Main function to play through command line
if __name__ == "__main__":
    # Specifying policy
    policy = 'policy_p1'

    # Creating players
    p1 = HumanPlayer('human')
    p2 = Player('ai', exp_rate=0)

    # Loading policy
    p2.loadPolicy(policy)

    # Printing welcome message
    print('You are Player 1! You go first...')
    # Creating game state
    st = State(p1, p2)
    # Playing
    st.playHuman()
