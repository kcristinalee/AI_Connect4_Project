import tkinter as tk

from state import State
from player import Player
from human import HumanPlayer

from dql import DQL

state = None
column_buttons = []
board_circles = []

dql = DQL('model.pt')


def start_new_game():
    # Retreiving global vars
    global column_buttons
    global board_circles

    # Clear out board
    for row in range(7):
        for col in range(8):
            board_circles[row * 8 + col].itemconfig("oval", fill = "#F4F3EE")

    # Column buttons
    column_buttons = []
    for i in range(8):
        column_button = tk.Button(board_frame, text=f"Play Here", command=lambda i=i: column_button_click(i), **col_button_style)
        column_button.grid(row=0, column=i, padx=10)
        column_buttons.append(column_button)

    # Specifying policy
    policy = 'policy_p1'

    # Creating players
    p1 = HumanPlayer('human')
    p2 = Player('ai', exp_rate=0)

    # Loading policy
    p2.loadPolicy(policy)

    # Creating game state
    global state
    state = State(p1, p2)

    # Changing play labels
    play_left_label.config(text="Play!")
    play_right_label.config(text="Play!")

def column_button_click(column_index):
    # Retreiving global vars
    global state
    global column_buttons
    global board_circles

    # player 1
    p1_action = state.p1.chooseActionF(column_index, state.board)
    state.updateState(p1_action)

    # check for end state
    win = state.winner()
    if win == 1:
        # Remove all col buttons
        for button in column_buttons:
            button.destroy()
        # Changing play labels
        play_left_label.config(text="You win!\nPress \"Start New Game\"\nto start a new game")
        play_right_label.config(text="You win!\nPress \"Start New Game\"\nto start a new game")
    elif win == 2:
        # Remove all col buttons
        for button in column_buttons:
            button.destroy()
        # Changing play labels
        play_left_label.config(text="AI wins!\nPress \"Start New Game\"\nto start a new game")
        play_right_label.config(text="AI wins!\nPress \"Start New Game\"\nto start a new game")
    else:
        pos = state.getAvailablePositions(2)
        p2_action = dql.chooseActionDeep(pos, state.board)
        state.updateState(p2_action)

        # p2_action = state.p2.chooseAction(pos, state.board)
        # board_hash = state.getHash()
        # state.p2.addStates(board_hash)

        win = state.winner()
        if win == 1:
            # Remove all col buttons
            for button in column_buttons:
                button.destroy()
            # Changing play labels
            play_left_label.config(text="You win!\nPress \"Start New Game\" to start a new game")
            play_right_label.config(text="You win!\nPress \"Start New Game\" to start a new game")
        elif win == 2:
            # Remove all col buttons
            for button in column_buttons:
                button.destroy()
            # Changing play labels
            play_left_label.config(text="AI wins!\nPress \"Start New Game\" to start a new game")
            play_right_label.config(text="AI wins!\nPress \"Start New Game\" to start a new game")

    current_board_state = state.board
    print(current_board_state)

    # Display current board
    for row in range(7):
        for col in range(8):
            # Update the color of the circles based on the current board state
            if current_board_state[row][col] == 1:
                # Player 1's piece
                board_circles[row * 8 + col].itemconfig("oval", fill = "#ED217C")
            elif current_board_state[row][col] == 2:
                # AI's piece
                board_circles[row * 8 + col].itemconfig("oval", fill = "#1B998B")

    # Remove col buttons when cols are full
    for col in range(len(current_board_state[0])):
        column_values = [row[col] for row in current_board_state]
        if all(value != 0 for value in column_values):
            column_buttons[col].destroy()

# Sets style for column buttons
col_button_style = {
    "bg": "#D5DF73",        # Background color
    "fg": "#2D3047",        # Foreground (text) color
    "width": 5,             # Width in characters
    "height": 1,            # Height in characters
    "font": ("Roboto", 11), # Font
    "bd": 0,                # Border thickness (set to 0 for no border)
    "relief": "flat",       # Border appearance (set to "flat" for no border)
    "justify": "center",    # Text alignment
    "padx": 10,             # Padding in x-direction
    "pady": 5,              # Padding in y-direction
    "state": "normal",      # Button state
    "cursor": "hand2"       # Cursor appearance
}

# Sets style for start button
start_button_style = {
    "bg": "#2D3047",        # Background color
    "fg": "#F4F3EE",        # Foreground (text) color
    "font": ("Roboto", 12), # Font
    "bd": 0,                # Border thickness (set to 0 for no border)
    "relief": "flat",       # Border appearance (set to "flat" for no border)
    "justify": "center",    # Text alignment
    "state": "normal",      # Button state
    "cursor": "hand2"       # Cursor appearance
}

# Create the main window
root = tk.Tk()
root.title("Connect4")

# Maximize the window
root.state('zoomed')

# Add background elements
top_frame = tk.Frame(root, bg = "#D5DF73", width = 293, height = 813)
top_frame.pack(side = "top", fill = "both", expand = True)

bottom_frame = tk.Frame(root, bg = "#F4F3EE", width = 586, height = 813)
bottom_frame.pack(side = "bottom", fill = "both", expand = True)

# Add welcome message
welcome_label = tk.Label(top_frame, text = "Welcome to Connect4!", font = ("Roboto", 24, "bold"), bg = "#D5DF73", fg = "#2D3047")
welcome_label.pack(pady = (0, 0))

# Add how to play section
how_to_play_label = tk.Label(top_frame, text = "How to Play", font = ("Roboto", 16, "bold"), bg = "#D5DF73", fg = "#2D3047")
how_to_play_label.pack(pady = (0, 0))

how_to_play_text = (
    "- Goal: Create a line with 4 of your pieces\n"
    "- The line can be horizontal, vertical, or diagonal\n"
    "- Click on a column with a green indicator to drop one of your pieces in that column\n"
    "- After you drop a piece, the AI will take a turn as well"
)
how_to_play_content = tk.Label(top_frame, text = how_to_play_text, font = ("Roboto", 12), justify = "left", bg = "#D5DF73", fg = "#2D3047")
how_to_play_content.pack(pady = (0, 0))

# Start game button
start_game_button = tk.Button(top_frame, text = "Start New Game", command = start_new_game, **start_button_style)
start_game_button.pack(pady = (5, 5))

# Add board
board_frame = tk.Frame(bottom_frame, width = 586, height = 813, bg = "#2D3047")
board_frame.pack(pady = (10, 10))

# Add text labels to play
play_left_label = tk.Label(bottom_frame, text = "Press \"Start New Game\" \nbutton to start", font = ("Roboto", 16), bg = "#F4F3EE", fg = "#2D3047")
play_left_label.place(relx = 0.15, rely = 0.5, anchor = "center")

play_right_label = tk.Label(bottom_frame, text = "Press \"Start New Game\" \nbutton to start", font = ("Roboto", 16), bg = "#F4F3EE", fg = "#2D3047")
play_right_label.place(relx = 0.85, rely = 0.5, anchor = "center")

# Add circles for empty spaces on the board
board_circles = []
for row in range(7):
    for col in range(8):
        circle = tk.Canvas(board_frame, width = 50, height = 50, bg = "#2D3047", highlightthickness = 0)
        circle.create_oval(5, 5, 45, 45, outline = "#F4F3EE", fill = "#F4F3EE", width = 2, tags="oval")
        circle.grid(row = row+1, column = col, padx = 3, pady = 3)
        board_circles.append(circle)

# Run the application
root.mainloop()