import tkinter as tk
from reversi import Reversi

if __name__ == "__main__":
    root = tk.Tk()
    game = Reversi(root)
    root.mainloop()
