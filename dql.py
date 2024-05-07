import torch
import torch.nn as nn
import torch.nn.functional as F


class DQL:

    def __init__(self, model_path):
        self.model = _DQLNet()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def chooseActionDeep(self, actions, board):
        valmax = -9999
        action = None
        for a in actions:
            player, col = a

            next_board = board.copy()
            for row in range(6, -1, -1):
                if next_board[row][col] == 0:
                    next_board[row][col] = player
                    break

            val = self.model(torch.tensor(next_board).to(torch.float32).unsqueeze(0))
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
        self.fc3 = nn.Linear(64, 1)

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
