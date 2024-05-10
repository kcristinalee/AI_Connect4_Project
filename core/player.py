import random
import pickle


# Global variables for board dimensions
BOARD_ROWS = 7
BOARD_COLS = 8

# Defines agent
class Player():

    def __init__(self, name, exp_rate=0.4):

        self.name = name

        # records all positions taken for training purposes
        self.states = []

        # how much Q-vals are updated towards newly calc Q-vals
        self.learning_rate = 0.2

        # we will be doing e-greedy
        # where 70% of the time, exploit: agent will take the greedy action (curr estimation of state-vals)
        # and the other 30%, explore: agent will take a random action
        self.exp_rate = exp_rate

        # discount factor ( to do living reward)
        self.decay_gamma = 0.99

        self.exp_rate_decay = 0.999

        # dict to update the corresponding state -> val
        self.states_value = {}

    def getHash(self, board):
        return str(board.reshape(BOARD_COLS * BOARD_ROWS))

    # takes in a list that is returned from getAvailablePositions
    # and the board
    def chooseAction(self, actions, board, iteration):

        hash = self.getHash(board)

        exp = (self.exp_rate_decay ** iteration) * self.exp_rate

        # exploration version
        if random.random() < exp:
            action = random.choice(actions)

        # exploitation
        else:
            value_max = -999
            random.shuffle(actions)

            for a in actions:
                player, col = a

                value = 0 if self.states_value.get(hash) is None else \
                self.states_value.get(hash)[col]

                # next_board = board.copy()

                # for row in range(BOARD_ROWS-1, -1, -1):
                #     if next_board[row][col] == 0:
                #         next_board[row][col] = player
                #         break

                # next_hash = self.getHash(next_board)
                # # print(self.states_value[])

                # value = 0 if self.states_value.get(next_hash) is None else self.states_value.get(next_hash)

                if value >= value_max:
                    value_max = value
                    action = a

        return action

    def addStates(self, board_hash, action):
        if board_hash not in self.states:
            self.states.append((board_hash, action[1]))

    def feedReward(self, reward):

        # Loop through the states the player went through
        for st, act in reversed(self.states):

            # Initializes state value if not encountered before
            if self.states_value.get(st) is None:
                self.states_value[st] = [0, 0, 0, 0, 0, 0, 0, 0]

            # Use value iteration formula
            self.states_value[st][act] += self.learning_rate * (
                        self.decay_gamma * reward - self.states_value[st][act])

            # Updates reward for next iteration
            reward = self.states_value[st][act]

    def reset(self):
        self.states = []

    # Using pickle module to save and load policies
    def savePolicy(self):
        fw = open(str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()
