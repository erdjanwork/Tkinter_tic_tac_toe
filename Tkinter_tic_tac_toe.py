import tkinter as tk
from tkinter import messagebox
from collections import deque
from pyfiglet import Figlet

SIZE = 3
turns = 0
game_board = [[str(i), str(i + 1), str(i + 2)] for i in range(1, SIZE * SIZE + 1, SIZE)]
players = deque()


def check_for_win():
    player_name, player_symbol = players[0]
    first_diagonal_win = all([game_board[i][i] == player_symbol for i in range(SIZE)])
    second_diagonal_win = all([game_board[i][SIZE - i - 1] == player_symbol for i in range(SIZE)])

    row_win = any([all(player_symbol == pos for pos in row) for row in game_board])
    col_win = any([all(game_board[r][c] == player_symbol for r in range(SIZE)) for c in range(SIZE)])

    if any([first_diagonal_win, second_diagonal_win, row_win, col_win]):
        messagebox.showinfo("Game Over", f"{player_name} won!")
        reset_game()
        return True

    if turns == SIZE * SIZE:
        messagebox.showinfo("Game Over", "Draw!")
        reset_game()
        return True

    return False


def place_symbol(row, col):
    game_board[row][col] = players[0][1]

    if check_for_win():
        return

    update_board()

    players.rotate()


def choose_position(position):
    global turns

    row, col = (position - 1) // SIZE, (position - 1) % SIZE

    if game_board[row][col] != str(row * SIZE + col + 1):
        messagebox.showinfo("Invalid Move", "Please select an empty position.")
        return

    turns += 1
    place_symbol(row, col)


def update_board():
    for row in range(SIZE):
        for col in range(SIZE):
            button = buttons[row][col]
            button["text"] = game_board[row][col]


def reset_game():
    global turns
    turns = 0

    for row in range(SIZE):
        for col in range(SIZE):
            game_board[row][col] = str(row * SIZE + col + 1)

    update_board()


def start_game():
    player_one_name = player_one_entry.get()
    player_two_name = player_two_entry.get()

    player_one_symbol = player_one_symbol_var.get()
    player_two_symbol = "O" if player_one_symbol == "X" else "X"

    players.append([player_one_name, player_one_symbol])
    players.append([player_two_name, player_two_symbol])

    update_board()
    choose_position_label.config(text=f"{player_one_name}, choose a position:")

    player_one_entry.config(state="disabled")
    player_two_entry.config(state="disabled")
    player_one_symbol_menu.config(state="disabled")
    start_button.config(state="disabled")


def create_button(row, col):
    button = tk.Button(game_frame, text="", width=10, height=5,
                       command=lambda row=row, col=col: choose_position(row * SIZE + col + 1))
    button.grid(row=row, column=col)
    return button


root = tk.Tk()
root.title("Tic-Tac-Toe")

title_label = tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

player_one_label = tk.Label(root, text="Player One Name:")
player_one_label.pack()
player_one_entry = tk.Entry(root)
player_one_entry.pack()

player_two_label = tk.Label(root, text="Player Two Name:")
player_two_label.pack()
player_two_entry = tk.Entry(root)
player_two_entry.pack()

player_one_symbol_label = tk.Label(root, text="Player One Symbol:")
player_one_symbol_label.pack()
player_one_symbol_var = tk.StringVar(value="X")
player_one_symbol_menu = tk.OptionMenu(root, player_one_symbol_var, "X", "O")
player_one_symbol_menu.pack()

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

choose_position_label = tk.Label(root, text="")
choose_position_label.pack()

game_frame = tk.Frame(root)
game_frame.pack()

buttons = [[create_button(row, col) for col in range(SIZE)] for row in range(SIZE)]

root.mainloop()
