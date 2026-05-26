from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
import random



class Game(ABC):
    def __init__(self, canvas):
        self.canvas = canvas

        #All colors:
        self.colors = {
            'bg': "#1a1a2e",
            'sidebar_bg': "#16213e",
            'card_bg': "#0f3469",
            'card_fg': "#e94560",
            'text': "#ffffff",
            'button_bg': "#4caf50",
            'button_fg': "#ffffff",
            'combobox_bg': "#32374b",
            'combobox_fg': "#ffffff",
            'gameover_fg': "#0f3460"}

        #All difficulty:
        self.difficulty_levels = {
            'Easy': {"grid": (4, 4), "symbols": ["1", "2", "3", "4", "5", "6", "7", "8"]},
            'Medium': {"grid": (4, 5), "symbols": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]},
            'Hell': {"grid": (5, 6),
                     "symbols": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]}}

        #start difficulty
        self.current_difficulty = "Easy"

        #custom font:
        self.custom_font = ("Helvetica", 24, "bold")



class GameCard(Game):
    def __init__(self, window):
        super().__init__(window)

        self.moves_label = None
        self.time_label = None

        self.game_frame = tk.Frame(self.canvas, bg="#1a1a2e")
        self.control_frame = tk.Frame(self.game_frame,
                                      bg=self.colors['bg'])
        self.cards_frame = tk.Frame(self.game_frame,
                                    bg=self.colors['bg'])
        self.revealed = []
        #self.matched_pairs = 0
        self.matched_cards = []
        self.moves = 0
        self.start_time = "0:00"
        self.game_solved = False
        self.cards = []
        self.symbols = []

        #flag for animation
        self.animation = True


    def create_game_grid(self):
        self.game_frame = tk.Frame(self.canvas,
                                   bg=self.colors['bg'])
        self.game_frame.pack(side = tk.TOP,
                             fill = tk.BOTH,
                             expand=True)

        self.control_frame = tk.Frame(self.game_frame,
                                      bg=self.colors['bg'])
        self.control_frame.pack(side = tk.LEFT,
                                fill = tk.Y,
                                expand = True)
        # add some labels
        self.moves_label = tk.Label(self.control_frame, text="Moves: 0",
                               font=self.custom_font,
                               bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.moves_label.pack(pady=(0, 10))

        self.time_label = tk.Label(self.control_frame, text="Time: 0:00",
                              font=self.custom_font,
                              bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.time_label.pack(pady=(0, 10))

        self.create_cards()

    def create_cards(self):
        self.cards_frame = tk.Frame(self.game_frame,
                                   bg=self.colors['bg'])
        self.cards_frame.pack(side = tk.RIGHT,
                              fill = tk.Y,
                              expand = True)

        rows, cols = self.difficulty_levels[self.current_difficulty]["grid"]
        symbols = self.difficulty_levels[self.current_difficulty]["symbols"] * 2

        self.cards = []

        random.shuffle(symbols)
        self.symbols = symbols

        #create cards in grid
        for i in range(rows):
            for j in range(cols):
                card_idx = i*cols+j

                #create card canvas
                card = tk.Canvas(self.cards_frame, width=80, height=100,
                                 bg=self.colors['card_bg'], highlightthickness=0)
                card.grid(row=i, column=j, padx=5, pady=5)

                card.bind("<Button-1>", lambda e, idx=card_idx: self.on_card_click(idx))

                #create card back
                card.create_rectangle(5, 5, 75, 95, fill=self.colors['card_bg'],  # Create card shape
                                      outline=self.colors['card_fg'], width=2)  # Add colored border
                card.create_text(40, 50, text="?", font=("Helvetica", 24, "bold"),  # Add question mark
                                 fill=self.colors['card_fg'], tags=('shirt',))  # Set text color

                # Create card front (hidden initially)
                card.create_rectangle(5, 5, 75, 95, fill=self.colors['card_fg'], # Create card shape
                                      outline=self.colors['card_bg'], width=2,# Add colored border
                                      state='hidden', tags=('front',))  # Hide initially and add tag for later reference

                card.create_text(40, 50, text=self.symbols[card_idx],
                                 font=("Helvetica", 24, "bold"),
                                 fill=self.colors['card_bg'],
                                 state='hidden', tags=('symbol',))
                self.cards.append(card)



class MemoryGame(Game):
    def __init__(self, window):
        super().__init__(window)

        self.restart = False

        #main window
        self.canvas.title("Memory Game")
        self.canvas.geometry("900x600")
        self.canvas.configure(background="#1a1a2e")

        style = ttk.Style()
        style.theme_create("modern", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": self.colors['combobox_bg'],
                    "fieldbackground": self.colors['combobox_bg'],
                    "background": self.colors['button_bg'],
                    "foreground": self.colors['combobox_fg']
                }
            }
        })
        style.theme_use("modern")

        #start with:
        self.WW = WinnerWindow(self.canvas, 0, "0:00")

        self.GC = GameCard(self.canvas)

        self.SF = StartFront(self.canvas)

        #for time work
        self.T = Time(0)





if __name__ == "__main__":
    root = tk.Tk()
    MemoryGame(root).create_frame()
    root.mainloop()
