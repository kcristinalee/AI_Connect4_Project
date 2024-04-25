class HumanPlayer:

    def __init__(self, name):
        self.name = name

    def chooseAction(self, actions, board):

        while True:
            col = int(input("Input your action col:"))
            if col in actions:
                return col
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