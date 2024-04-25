import numpy as np
import random
import pickle
import copy

from state import State

BOARD_ROWS = 7
BOARD_COLS = 8

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

        # dict to update the corresponding state -> val
        self.states_value = {}

    def getHash(self, board):
        return str(board.reshape(BOARD_COLS * BOARD_ROWS))
    
    # takes in a list that is returned from getAvailablePositions 
    # and the board
    def chooseAction(self, actions, board):

        # exploration version
        if random.random() < self.exp_rate:
            action = random.choice(actions)

        # exploitation
        else:
            # print(actions)
            value_max = -999
            random.shuffle(actions)

            for a in actions:
                player, col = a
                
                next_board = board.copy()

                for row in range(BOARD_ROWS-1, -1, -1):
                    if next_board[row][col] == 0:
                        next_board[row][col] = player
                        break

                next_hash = self.getHash(next_board)
                # print(self.states_value[])

                value = 0 if self.states_value.get(next_hash) is None else self.states_value.get(next_hash)

                if value >= value_max:
                    value_max = value
                    action = a
            # print(action)
        
        return action

    def addStates(self, board_hash):
        self.states.append(board_hash)

    def feedReward(self, reward):
        
        # Loop through the states the player went through
        for curr in reversed(self.states):
            
            # Initializes state value if not encountered before
            if self.states_value.get(curr) is None:
                self.states_value[curr] = 0
                
            # Use value iteration formula
            self.states_value[curr] += self.learning_rate * (self.decay_gamma * reward - self.states_value[curr])
            
            # Updates reward for next iteration
            reward = self.states_value[curr]

    def reset(self):
        self.states = []

    # Using pickle module to save and load policies
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()
