import pickle
import random
import numpy as np


BOARD_ROWS = 7
BOARD_COLS = 8


class State:
    def __init__(self, p1, p2, board=None):

        if not board:
            self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]])
        else:
            self.board = board


        self.p1 = p1
        self.p2 = p2

        self.isEnd = False

        self.boardHash = None

    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

    def getAvailablePositions(self, p):

        availCols = []
        for col in range(BOARD_COLS):
            if self.board[0][col] == 0:
                availCols.append((p, col))

        return availCols

    def winner(self):

        draw = True

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                loc = self.board[row][col]

                if loc != 0:
                    if col + 3 < BOARD_COLS and \
                        loc == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]:
                        return loc

                    if row + 3 < BOARD_ROWS and \
                        loc == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
                        return loc

                    if row + 3 < BOARD_ROWS and col + 3 < BOARD_COLS and \
                       loc == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]:
                        return loc

                    if row - 3 >= 0 and col + 3 < BOARD_COLS and \
                       loc == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3]:
                        return loc

                else:
                    draw = False

        return 0 if not draw else -1


    def updateState(self, action):

        player, col = action

        for row in range(BOARD_ROWS-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                break

        # check if there's a winner after the move
        if self.winner() != 0:
            self.isEnd = True

    # reset game
    def reset(self):
        self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])

        self.isEnd = False
        self.boardHash = None

   # gives rewards to Players from the action that was just made
    def giveReward(self, action):

        result = self.winner()

        player_num, col = action

        # player 1 won
        if result == 1:
            self.p1.feedReward(20)
            self.p2.feedReward(-20)
        # player 2 won
        elif result == 2:
            self.p1.feedReward(-20)
            self.p2.feedReward(20)

    # check how many consecutive the action made
    def checkConsecutives(self, action):
        player, col = action
        row = len(self.board) - 1  # start checking from the bottom row
        consecutives = 0

        # check vertically
        while row >= 0 and self.board[row][col] == player:
            consecutives += 1
            row -= 1

        # check horizontally
        row = len(self.board) - 1  # reset row to bottom
        for c in range(col - 1, max(col - 4, -1), -1):
            if self.board[row][c] == player:
                consecutives += 1
            else:
                break

        for c in range(col + 1, min(col + 4, len(self.board[0]))):
            if self.board[row][c] == player:
                consecutives += 1
            else:
                break

        # check diagonally (down-right and down-left)
        directions = [(1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1  # count the initial move
            r, c = row + dx, col + dy
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == player:
                count += 1
                r += dx
                c += dy

            r, c = row - dx, col - dy
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == player:
                count += 1
                r -= dx
                c -= dy

            consecutives = max(consecutives, count)

        return consecutives

    # two AI bots play against each other for training purposes
    def play(self, num_eps = 50000):
        for i in range(num_eps):

            while not self.isEnd:
                # player 1
                positions = self.getAvailablePositions(1)
                p1_action = self.p1.chooseAction(positions, self.board, i)
                board_hash = self.getHash()
                self.updateState(p1_action)

                self.p1.addStates(board_hash, p1_action)


                # check for end state
                win = self.winner()
                if win != 0:
                    # self.showBoard()

                    if i % 100 == 0:
                        print("Rounds {}".format(i))
                        print(self.board)

                    self.giveReward(p1_action)
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    pos = self.getAvailablePositions(2)
                    p2_action = self.p2.chooseAction(pos, self.board, i)
                    board_hash = self.getHash()
                    self.updateState(p2_action)
                    self.p2.addStates(board_hash, p2_action)

                    win = self.winner()
                    if win != 0:
                        # self.showBoard()

                        if i % 100 == 0:
                            print("Rounds {}".format(i))
                            print(self.board)

                        self.giveReward(p2_action)
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break



    def printBoard(self):
        print(self.board)


class Player:

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

        # dict to update the corresponding state -> val
        self.states_value = {}


    def getHash(self, board):
        return str(board.reshape(BOARD_COLS * BOARD_ROWS))

    # takes in a list that is returned from getAvailablePositions
    # and the board
    def chooseAction(self, actions, board, iteration):

        hash = self.getHash(board)

        exp = (0.999998 ** iteration) * self.exp_rate

        # exploration version
        if random.random() < exp:
            action = random.choice(actions)

        # exploitation
        else:
            value_max = -999
            random.shuffle(actions)

            for a in actions:
                player, col = a



                value = 0 if self.states_value.get(hash) is None else self.states_value.get(hash)[col]

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
            self.states_value[st][act] += self.learning_rate * (self.decay_gamma * reward - self.states_value[st][act])

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


num_episodes = 2000000
policy_name = 'policy'

p1 = Player("p1")
p2 = Player(policy_name)

st = State(p1, p2)
print("training...")
st.play(num_episodes)
p2.savePolicy()
print('saved policy')