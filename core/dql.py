import torch
import torch.nn as nn
import torch.nn.functional as F
from core.state import State

BOARD_ROWS = 7
BOARD_COLS = 8


class DQL:

    def __init__(self, model_path):
        self.model = _DQLNet()
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

    def chooseActionDeep(self, actions, board):
        valmax = -9999
        action = None

        for a in actions:
            player, col = a

            next_board = board.copy()
            for row in range(BOARD_ROWS - 1, -1, -1):
                    if next_board[row][col] == 0:
                        next_board[row][col] = player
                        temp_state = State(1, 2, next_board)
                        if temp_state.winner() != 0:
                            return a
                        break

        for a in actions:
            player, col = a
            if player == 1:
                opp = 2
            else:
                opp = 1

            next_board = board.copy()
            for row in range(BOARD_ROWS - 1, -1, -1):
                if next_board[row][col] == 0:
                    next_board[row][col] = opp
                    temp_state = State(1, 2, next_board)
                    if temp_state.winner() != 0:
                        return a
                    break


        vals = self.model(torch.tensor(board).to(torch.float32).unsqueeze(0)).squeeze()

        for a in actions:
            player, col = a

            val = vals[col]
            if val >= valmax:
                valmax = val
                action = a

        return action


class _DQLNet(nn.Module):
    def __init__(self):
        super(_DQLNet, self).__init__()

        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(256 * 7 * 8, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 8)

    def forward(self, x):
        x = x.unsqueeze(1)

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = x.view(-1, 256 * 7 * 8)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x
