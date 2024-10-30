import numpy as np
import tkinter as tk
from tkinter import messagebox
import random

EMPTY, BLACK, WHITE = 0, 1, -1
SIZE = 8
CELL_SIZE = 60

class Reversi:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversi")
        self.init_game()
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, anchor="center")
        
        self.new_game_button = tk.Button(self.button_frame, text="New game", command=self.reset_game)
        self.new_game_button.pack()

    def init_game(self):
        self.board = np.zeros((SIZE, SIZE), dtype=int)
        self.board[3, 3] = WHITE
        self.board[3, 4] = BLACK
        self.board[4, 3] = BLACK
        self.board[4, 4] = WHITE
        self.current_player = BLACK

        self.canvas = tk.Canvas(self.root, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg='green')
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(SIZE):
            for j in range(SIZE):
                x0, y0 = j * CELL_SIZE, i * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='black')
                
                if self.board[i, j] == BLACK:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill='black')
                elif self.board[i, j] == WHITE:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill='white', outline='black')

    def on_click(self, event):
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if self.make_move(row, col):
            self.draw_board()
            if not self.get_valid_moves():
                self.end_game()
            else:
                self.root.after(500, self.ai_move)

    def valid_move(self, row, col):
        if self.board[row, col] != EMPTY:
            return False
        opponent = -self.current_player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < SIZE and 0 <= c < SIZE and self.board[r, c] == opponent:
                while 0 <= r < SIZE and 0 <= c < SIZE:
                    r += dr
                    c += dc
                    if not (0 <= r < SIZE and 0 <= c < SIZE):
                        break
                    if self.board[r, c] == EMPTY:
                        break
                    if self.board[r, c] == self.current_player:
                        return True
        return False

    def make_move(self, row, col):
        if not self.valid_move(row, col):
            return False
        opponent = -self.current_player
        self.board[row, col] = self.current_player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_positions = []
            while 0 <= r < SIZE and 0 <= c < SIZE and self.board[r, c] == opponent:
                flip_positions.append((r, c))
                r += dr
                c += dc
            if 0 <= r < SIZE and 0 <= c < SIZE and self.board[r, c] == self.current_player:
                for fr, fc in flip_positions:
                    self.board[fr, fc] = self.current_player
        self.current_player = -self.current_player
        return True

    def get_valid_moves(self):
        return [(r, c) for r in range(SIZE) for c in range(SIZE) if self.valid_move(r, c)]

    def ai_move(self):
        valid_moves = self.get_valid_moves()
        if valid_moves:
            move = random.choice(valid_moves)
            self.make_move(*move)
            self.draw_board()
            if not self.get_valid_moves():
                self.end_game()

    def end_game(self):
        black_score = np.sum(self.board == BLACK)
        white_score = np.sum(self.board == WHITE)
        if black_score > white_score:
            winner = "You won!"
        elif white_score > black_score:
            winner = "You lost!"
        else:
            winner = "Tie!"
        messagebox.showinfo("End of the game", f"End of the game!\nBlack: {black_score}\nWhite: {white_score}\n\n{winner}")

    def reset_game(self):
        self.canvas.destroy()
        self.init_game()