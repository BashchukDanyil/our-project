from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
import random
import time


class Time:
    def __init__(self, secund):
        self.sec = secund
    def time_tabel(self):
        m = self.sec // 60
        s = self.sec % 60
        if s < 10:
            s = "0" + str(s)
        return f"{m}:{s}"
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

class WinnerWindow(Game):
    def __init__(self, canvas, moves, start_time):
        super().__init__(canvas)
        self.moves = moves
        self.start_time = start_time
        self.win_frame = None
        self.lbl = None
        self.res = None
        self.moves_label = None
        self.time_label = None
    def create_frame(self):
        self.win_frame = tk.Frame(self.canvas,
                                  bg=self.colors['bg'])
        self.win_frame.pack(fill=tk.BOTH, side = tk.TOP, pady=(30, 10))
        self.lbl = tk.Label(self.win_frame, text="You winner", fg = 'white', font = ("Helvetica", 48, "bold"), bg=self.colors['gameover_fg'])
        self.lbl.pack(side = tk.TOP, pady=(0, 10))
        self.res = tk.Label(self.win_frame, text="Result:", fg ='white', font = self.custom_font, bg=self.colors['gameover_fg'])
        self.res.pack(side = tk.TOP)
        self.moves_label = tk.Label(self.win_frame, text=f"Moves: {self.moves}",
                               font=self.custom_font,
                               bg=self.colors['gameover_fg'], fg=self.colors['text'])
        self.moves_label.pack(pady=(0, 10))
        self.time_label = tk.Label(self.win_frame, text=f"Time: {self.start_time}",
                              font=self.custom_font,
                              bg=self.colors['gameover_fg'], fg=self.colors['text'])
        self.time_label.pack(pady=(0, 10))
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

    # def position_reveal(self):
    #     rows, cols = self.difficulty_levels[self.current_difficulty]["grid"]
    #     for i in range(rows):
    #         for j in range(cols):
    #             self.reveal_card(i * cols + j)
    #
    # def position_hidden(self):
    #     rows, cols = self.difficulty_levels[self.current_difficulty]["grid"]
    #     if self.animation == True:
    #         self.animation = False
    #         for i in range(rows):
    #             for j in range(cols):
    #                 self.hidden_card(i*cols+j)






    def on_card_click(self, idx):
        if self.animation == True:
            if idx not in self.matched_cards and idx not in self.revealed:
                self.moves += 1
                self.moves_label["text"] = f"Moves: {self.moves}"
                self.animation = False
                self.reveal_card(idx)
                if len(self.matched_cards) < 2:
                    self.matched_cards.append(idx)
                elif len(self.matched_cards) == 2:
                    if self.symbols[self.matched_cards[0]] != self.symbols[self.matched_cards[1]]:
                        self.hidden_card(self.matched_cards[0])
                        self.hidden_card(self.matched_cards[1])
                    else:
                        self.revealed += self.matched_cards
                    self.matched_cards = [idx]
        if len(self.revealed) + len(self.matched_cards) == len(self.difficulty_levels[self.current_difficulty]["symbols"] * 2):
            self.game_solved = True
    def reveal_card(self, idx):
        card = self.cards[idx]
        card.after(10, self.go, 80, card, "normal")
    def hidden_card(self, idx):
        card = self.cards[idx]
        card.after(10, self.go, 80, card, "hidden")

    #animation
    def go(self, width, card, state):
        width -= 2
        card.config(width = width)
        if width > 0:
            card.after(10, self.go, width, card, state)
        else:
            card.after(10, self.revers, width, card)
            card.itemconfig('front', state=state)
            card.itemconfig('symbol', state=state)

    def revers(self, width, card):
            width += 2
            card.config(width = width)
            if width < 80:
                card.after(10, self.revers, width, card)
            else:
                self.animation = True




    def new_game(self):
        self.game_solved = False  # Reset game solved flag
        self.revealed.clear()  # Clear revealed cards list
        self.matched_cards.clear()  # Clear matched cards list
        self.moves=0  # Reset moves counter
        self.start_time = None  # Reset start time

        #reset labels
        #self.time_label.config(text="Time: 0:00")

        #recreate the game grid
        self.game_frame.destroy()
        self.create_game_grid()

class StartFront(Game):
    def __init__(self, window):
        super().__init__(window)

        self.front_frame = tk.Frame(self.canvas, bg=self.colors['bg'])

    def change_difficulty(self, event):
        self.current_difficulty = event.widget.get()

    def create_front(self):

        #create front frame:
        self.front_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        self.front_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        #Create title and subtitle:
        tk.Label(self.front_frame, text="Memory Game",
                            font=("Helvetica", 48, "bold"),
                            bg=self.colors['sidebar_bg'], fg=self.colors['text']).pack(pady = (30, 10))

        tk.Label(self.front_frame, text="Test Your Memory!",
                                font=("Helvetica", 24, "italic"),
                                bg=self.colors['sidebar_bg'], fg=self.colors['text']).pack(pady=(0, 30))

        tk.Label(self.front_frame, text="Difficulty:",
                                       font=self.custom_font,
                                       bg=self.colors['sidebar_bg'], fg=self.colors['text']).pack(pady=(0, 5))

        #create combobox
        difficulty_combox = ttk.Combobox(self.front_frame, values=list(self.difficulty_levels.keys()),
                                              state="readonly", font=self.custom_font, width=10)
        difficulty_combox.set(self.current_difficulty)
        difficulty_combox.pack(pady=(0, 20))
        difficulty_combox.bind("<<ComboboxSelected>>", self.change_difficulty)

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


    def tick(self):
        if (self.GC.game_solved == False) and (self.restart == False):                                                            
            self.GC.start_time = self.T.time_tabel()
            self.GC.time_label.config(text=f"Time: {self.GC.start_time}")
            self.T.sec += 1
            self.canvas.after(1000, self.tick)

    def next(self):
        self.SF.front_frame.destroy()
        self.create_game()

    def back(self):
        self.restart = True
        self.T.sec = 0
        self.GC.game_frame.destroy()
        self.create_frame()
    def start(self):
        self.WW.win_frame.destroy()
        self.create_frame()

    def reset(self):
        self.GC.cards_frame.destroy()
        self.GC.game_solved = False
        self.GC.start_time = 0
        self.T.sec = 0
        self.GC.moves = 0  # Reset moves counter
        self.GC.time_label.config(text="Time: 0:00")
        self.GC.moves_label.config(text="Moves: 0")
        self.GC.create_cards()

    def create_frame(self):

        self.SF.create_front()

        # create new game button
        new_game_button = tk.Button(self.SF.front_frame, text="New Game",
                                    font=self.custom_font,
                                    bg=self.colors['button_bg'],
                                    fg=self.colors['text'],
                                    command = self.next)
        new_game_button.pack(pady=(0, 30))

        # add hover effect
        new_game_button.bind("<Enter>", lambda e: e.widget.config(bg="red"))
        new_game_button.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))

    def create_game(self):

        self.GC.current_difficulty = self.SF.current_difficulty
        self.GC.new_game()

        #add Go_out_button
        Go_out_button = tk.Button(self.GC.control_frame,
                                  text="Go out",
                                  font=self.custom_font,
                                  bg=self.colors['button_bg'],
                                  fg=self.colors['text'],
                                  command=self.back)
        Go_out_button.pack(pady=(30, 10))

        Go_out_button.bind("<Enter>", lambda e: e.widget.config(bg="red"))
        Go_out_button.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))

        # add reset_button
        reset_button = tk.Button(self.GC.control_frame,
                                 text="Reset",
                                 font=self.custom_font,
                                 bg=self.colors['button_bg'],
                                 fg=self.colors['text'],
                                 command=self.reset)
        reset_button.pack(pady=(0, 30))

        reset_button.bind("<Enter>", lambda e: e.widget.config(bg="red"))
        reset_button.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))

        # add timer
        self.restart = False
        self.tick()
        
        #add winner new game button
        self.canvas.after(5000, self.create_over)
    def create_over(self):
        if self.GC.game_solved == True:
            self.restart = True
            self.T.sec = 0
            self.GC.game_frame.destroy()
            self.WW.moves = self.GC.moves
            self.WW.start_time = self.GC.start_time
            self.WW.create_frame()
            btn = tk.Button(self.WW.win_frame, text="New Game", fg="white", font=self.custom_font,
                                 bg=self.colors['button_bg'], command=self.start)
            btn.pack(side=tk.TOP, pady=(10, 10))

            btn.bind("<Enter>", lambda e: e.widget.config(bg="red"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))
        else:
            self.canvas.after(5000, self.create_over)

        #reveal start position
        # self.GC.position_reveal()



if __name__ == "__main__":
    root = tk.Tk()

    MemoryGame(root).create_frame()

    root.mainloop()