"""
application.py

Application class for rendering game
"""

import tkinter as tk
import chess
import chess.svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from tempfile import TemporaryFile

LARGE_FONT= ("Verdana", 12)
BOARD_PIXEL_SIZE = 390
TEMP_PNG = "temp.png"
TEMP_SVG = "temp.svg"

class Application(tk.Tk):

    # Constructor
    def __init__(self, input_mcts, *args, **kwargs):
        
        # Store board (game ended)

        # Boilerplate grid code
        tk.Tk.__init__(self, *args, **kwargs)
        self.model = input_mcts  # This holds all of the model data


        # Make a 2x2 grid (board on left, info on right, buttons bottom right)
        self.data_panel = None
        self.chessboard = ChessBoard(self)
        self.button_panel = ButtonPanel(self)
        self.data_panel = DataPanel(self)

        self.chessboard.grid(column=0,rowspan=2)
        self.button_panel.grid(column=1,row=1)
        self.data_panel.grid(column=1, row=0)


# ButtonPanel class
class ButtonPanel(tk.Frame):

    # Constructor
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent

        cb = self.parent.chessboard
        forward_move = tk.Button(self, text="> Move >", command=cb.forward_move)
        backward_move = tk.Button(self, text="< Move <", command=cb.backward_move)
        forward_game = tk.Button(self, text="> Game >", command=cb.forward_game)
        backward_game = tk.Button(self, text="< Game <", command=cb.backward_game)

        forward_move.grid(column=1, row=0)
        backward_move.grid(column=0, row=0)
        forward_game.grid(column=1, row=1)
        backward_game.grid(column=0, row=1)


# DataPanel class
class DataPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent

        self.current_move_num = tk.StringVar()
        self.current_board_num = tk.StringVar()
        self.last_move = tk.StringVar()
        self.to_play = tk.StringVar()

        # Instance variables
        self.update_data()

        # Pack labels
        lbls = [
            tk.Label(self, text="Flowgod's FlowChess", font=LARGE_FONT),
            tk.Label(self, textvariable=self.current_move_num),
            tk.Label(self, textvariable=self.current_board_num),
            tk.Label(self, textvariable=self.last_move),
            tk.Label(self, textvariable=self.to_play),
        ]

        for lbl in lbls:
            lbl.pack()


    def update_data(self):

        # Set instance variables based on mcts
        cb = self.parent.chessboard
        self.current_move_num.set(f"Move number: {cb.active_move}")
        self.current_board_num.set(f"Board number: {cb.active_board}")
        last_move_string = cb._board.move_stack[-1].uci() if len(cb._board.move_stack) > 0 else None
        self.last_move.set(f"Last move: {last_move_string}")
        self.to_play.set(f"To play: {'WHITE' if cb._board.turn else 'BLACK'}")


# Chessboard class
class ChessBoard(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

        # Instance variables
        self.active_board = 0
        self.active_move = 0
        self.parent = parent


        # Board (make svg and pass into png)
        self.board_image = None
        self.board_frame = tk.Canvas(self, width=BOARD_PIXEL_SIZE, height=BOARD_PIXEL_SIZE)
        self.board_frame.pack()

        self.forward_game()
        self.update()

        

    # Rerender
    def update(self):

        # Replace image
        svg_info = chess.svg.board(board=self._board)
        with open(TEMP_SVG, "w") as f:
            f.write(svg_info)
        drawing = svg2rlg(TEMP_SVG)
        renderPM.drawToFile(drawing, TEMP_PNG, fmt="PNG")
        self.board_image = ImageTk.PhotoImage(Image.open(TEMP_PNG))
        self.board_frame.create_image(BOARD_PIXEL_SIZE/2,BOARD_PIXEL_SIZE/2, image=self.board_image)

        # Update datapanel
        if (self.parent.data_panel is not None): self.parent.data_panel.update_data()

    # Move game forward
    def forward_move(self):
        if (self.active_move + 1 >= self.num_moves()):
            return
        # else
        self._board.push(self._stack[self.active_move])
        self.active_move += 1
        self.update()

    # Move game backward
    def backward_move(self):
        if (self.active_move == 0):
            return
        # else
        self.active_move -= 1
        self._board.pop()
        self.update()

    # Forward in game list
    def forward_game(self):
        self.active_board = (self.active_board + 1) % self.num_games()
        self.active_move = 0
        self._stack = self.parent.model.last_win.move_stack
        self._board = chess.Board()
        self.update()

    # Backward in game list
    def backward_game(self):
        self.active_board = (self.active_board - 1) % self.num_games()
        self.active_move = 0
        self._stack = self.parent.model.last_win.move_stack
        self._board = chess.Board()
        self.update()

    # Availible moves
    def num_moves(self):
        return (len(self.parent.model.last_win.move_stack))

    # Availible games
    def num_games(self):
        return 1 # TODO: support multiple games


# # Chess board class
# b = chess.Board()
# b.push_uci("e2e4")
# b.push_uci("e7e5")
# b.push_uci("b1c3")
# b.push_uci("g8f6")





