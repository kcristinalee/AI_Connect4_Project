import numpy as np

# Global variables for board dimensions
BOARD_ROWS = 7
BOARD_COLS = 8

# represents states (boards) in Connect 4 game 
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
            self.p1.feedReward(10)
            self.p2.feedReward(-10)
        # player 2 won
        elif result == 2:
            self.p1.feedReward(-10)
            self.p2.feedReward(10)

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