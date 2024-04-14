import numpy as np
import random
import pickle
import copy

from state import State

BOARD_ROWS = 7
BOARD_COLS = 8

class Player():

    def __init__(self, name, first):
         
        self.name = name

        # records all positions taken for training purposes
        self.states = []

        # how much Q-vals are updated towards newly calc Q-vals
        self.learning_rate = 0.2

        # we will be doing e-greedy
        # where 70% of the time, exploit: agent will take the greedy action (curr estimation of state-vals)
        # and the other 30%, explore: agent will take a random action
        self.exp_rate = 0.3

        # discount factor ( to do living reward)
        self.decay_gamma = 0.9

        # dict to update the corresponding state -> val
        self.states_value = {}

        # this is a bool saying if this player is Player 1 or not
        self.first = first

    def getHash(self, board):
        return str(board.reshape(BOARD_COLS * BOARD_ROWS))
    
    # takes in a list that is returned from getAvailablePositions 
    # and the board
    def chooseAction(self, actions, state):
        action = random.choice(actions)
        return action


    def addStates(self, board_hash):
        self.states.append(board_hash)

    def feedReward(self, reward):
        pass

    def reset(self):
        pass

    # Using pickle module to save and load policies
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()
