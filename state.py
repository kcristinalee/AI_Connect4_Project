import numpy as np

BOARD_ROWS = 7
BOARD_COLS = 8

# represents states (boards) in Connect 4 game 
class State():
    def __init__(self, p1, p2):

        # initial state of board 
        self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]])
        
        self.p1 = p1
        self.p2 = p2

        self.isEnd = False

        self.boardHash = None

    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash   
    
    # returns a list of the available cols that Player can drop a piece in
    def getAvailablePositions(self, p):

        availCols = []
        
        # just have to check the first row if the col is open
        for col in range(BOARD_COLS):
            if self.board[0][col] == 0:
                availCols.append((p, col))
        
        return availCols


    # returns 1 is Player 1 won
    # 2 if Player 2 won
    # and 0 if no winner yet
    def winner(self):

        draw = True

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):

                # location
                loc = self.board[row][col]

                # only check non-empty spaces
                if loc != 0:

                    # check horizontal consecutive
                    if col + 3 < BOARD_COLS and \
                        loc == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]:
                        return loc
                    
                    # check vertical
                    if row + 3 < BOARD_ROWS and \
                        loc == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
                        return loc
                    
                    # check diagonal (down-right)
                    if row + 3 < BOARD_ROWS and col + 3 < BOARD_COLS and \
                       loc == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]:
                        return loc
                    
                    # check diagonal (up-right)
                    if row - 3 >= 0 and col + 3 < BOARD_COLS and \
                       loc == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3]:
                        return loc
                
                else:
                    draw = False
                    
        return 0 if not draw else -1
                
    # updates the board by performing the action
    # action is a tuple where the first num is Player #
    # and sec num is the col you want to drop the piece in
    def updateState(self, action):

        player, col = action

        # iterate through the rows from bottom to top
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
    def giveReward(self):
    
        result = self.winner()

        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == 2:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.5)
            self.p2.feedReward(0.5)

    # two AI bots play against each other for training purposes
    def play(self, num_eps = 1000):
        for i in range(num_eps):

            while not self.isEnd:
                # player 1
                positions = self.getAvailablePositions(1)
                p1_action = self.p1.chooseAction(positions, self.board)
                self.updateState(p1_action)
                board_hash = self.getHash()

                # check for end state
                win = self.winner()
                if win != 0:
                    # self.showBoard()

                    if i % 100 == 0:
                        print("Rounds {}".format(i))
                        print(self.board)

                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    pos = self.getAvailablePositions(2)
                    p2_action = self.p2.chooseAction(pos, self.board)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addStates(board_hash)

                    win = self.winner()
                    if win != 0:
                        # self.showBoard()

                        if i % 100 == 0:
                            print("Rounds {}".format(i))
                            print(self.board)

                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break


    def printBoard(self):
        print(self.board)
