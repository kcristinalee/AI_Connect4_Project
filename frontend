import tkinter as tk

def start_new_game():
    # Clear out board
    board_circles = []
    for row in range(6):
        for col in range(7):
            circle = tk.Canvas(board_frame, width=60, height=60, bg="#2D3047", highlightthickness=0)
            circle.create_oval(5, 5, 55, 55, outline="#F4F3EE", fill="#F4F3EE", width=2)
            circle.grid(row=row+1, column=col, padx=3, pady=3)
            board_circles.append(circle)
    
    # TODO: Reset game on backend

    print("New Game Button Pressed")

def column_button_click(column_index):
    # TODO: Feed column_index to backend

    # TODO: Retreive current board after AI plays
    #current_board_state = function to backend

    # Display current board
    #for row in range(6):
    #    for col in range(7):
    #        # Update the color of the circles based on the current board state
    #        if current_board_state[row][col] == 0:
    #            # Empty space
    #            board_circles[row * 7 + col].configure(bg="F4F3EE")
    #        elif current_board_state[row][col] == 1:
    #            # Player 1's piece
    #            board_circles[row * 7 + col].configure(bg="ED217C")
    #        elif current_board_state[row][col] == 2:
    #            # AI's piece
    #            board_circles[row * 7 + col].configure(bg="1B998B")

    # TODO: Check for win state (fetch from backend)
    # If won, remove all col buttons and display winner
    #for button in column_buttons:
    #    button.grid_remove()

    # Remove col buttons when cols are full
    #for col in range(7):
    #    if all(row != 0 for row in current_board_state[:, col]):
    #        # Column is full, hide the corresponding button
    #        column_buttons[column_index].grid_remove()

    print(column_index)

def toggle_fullscreen():
    if root.attributes('-fullscreen'):
        root.attributes('-fullscreen', False)
        fullscreen_button.config(text="Fullscreen On")
    else:
        root.attributes('-fullscreen', True)
        fullscreen_button.config(text="Fullscreen Off")

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

start_button_style = {
    "bg": "#2D3047",        # Background color
    "fg": "#F4F3EE",        # Foreground (text) color
    "font": ("Roboto", 15), # Font
    "bd": 0,                # Border thickness (set to 0 for no border)
    "relief": "flat",       # Border appearance (set to "flat" for no border)
    "justify": "center",    # Text alignment
    "padx": 10,             # Padding in x-direction
    "pady": 5,              # Padding in y-direction
    "state": "normal",      # Button state
    "cursor": "hand2"       # Cursor appearance
}

screen_button_style = {
    "bg": "#2D3047",        # Background color
    "fg": "#F4F3EE",        # Foreground (text) color
    "font": ("Roboto", 12), # Font
    "bd": 0,                # Border thickness (set to 0 for no border)
    "relief": "flat",       # Border appearance (set to "flat" for no border)
    "justify": "center",    # Text alignment
    "padx": 10,             # Padding in x-direction
    "pady": 5,              # Padding in y-direction
    "state": "normal",      # Button state
    "cursor": "hand2"       # Cursor appearance
}

# Create the main window
root = tk.Tk()
root.title("Connect4")

# Add a button to toggle fullscreen
fullscreen_button = tk.Button(root, text="Fullscreen Off", command=toggle_fullscreen, **screen_button_style)
fullscreen_button.pack()

# Make the window fullscreen
root.attributes('-fullscreen', True)

# Add background elements
left_frame = tk.Frame(root, bg="#D5DF73", width=293, height=813)
left_frame.place(x=50, y=225)

right_frame = tk.Frame(root, bg="#F4F3EE", width=586, height=813)
right_frame.place(x=625, y=150)

# Add welcome message
welcome_label = tk.Label(left_frame, text="Welcome to Connect4!", font=("Roboto", 24, "bold"), bg="#D5DF73", fg="#2D3047")
welcome_label.pack(pady=(20, 10))

# Add how to play section
how_to_play_label = tk.Label(left_frame, text="How to Play", font=("Roboto", 16, "bold"), bg="#D5DF73", fg="#2D3047")
how_to_play_label.pack(pady=(20, 10))

how_to_play_text = (
    "- Goal: Create a line with 4 of your pieces\n"
    "- The line can be horizontal, vertical, or diagonal\n"
    "- Click on a column with a green indicator to drop one of your pieces in that column\n"
    "- After you drop a piece, the AI will take a turn as well"
)
how_to_play_content = tk.Label(left_frame, text=how_to_play_text, font=("Roboto", 12), justify="left", bg="#D5DF73", fg="#2D3047")
how_to_play_content.pack(pady=(0, 20))

# Start game button
start_game_button = tk.Button(left_frame, text="Start New Game", command=start_new_game, **start_button_style)
start_game_button.pack(pady=(20, 10))

# Add board
board_frame = tk.Frame(right_frame, width=586, height=813, bg="#2D3047")
board_frame.pack()

# Column buttons
column_buttons = []
for i in range(7):
    column_button = tk.Button(board_frame, text=f"Play Here", command=lambda i=i: column_button_click(i), **col_button_style)
    column_button.grid(row=0, column=i, padx=10)
    column_buttons.append(column_button)

# Add circles for empty spaces on the board
board_circles = []
for row in range(6):
    for col in range(7):
        circle = tk.Canvas(board_frame, width=60, height=60, bg="#2D3047", highlightthickness=0)
        circle.create_oval(5, 5, 55, 55, outline="#F4F3EE", fill="#F4F3EE", width=2)
        circle.grid(row=row+1, column=col, padx=3, pady=3)
        board_circles.append(circle)

# Run the application
root.mainloop()
