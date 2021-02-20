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

LARGE_FONT= ("Verdana", 12)
TEMP_SVG = "temp.svg"
TEMP_PNG = "temp.png"

class Application(tk.Tk):

    # Constructor
    def __init__(self, input_board, *args, **kwargs):
        
        # Store board (game ended)

        # Boilerplate grid code
        tk.Tk.__init__(self, *args, **kwargs)
        frame = ChessBoard(self, input_board)
        frame.pack()

# Chessboard class

class ChessBoard(tk.Frame):

    def __init__(self, parent, input_board):
        tk.Frame.__init__(self,parent)

        # Instance variables
        self.move_stack = input_board.move_stack
        self.board = chess.Board()
        self.move_to_play = 0

        # Header
        self.label = tk.Label(self, text="ChessBoard", font=LARGE_FONT)

        # Board (make svg and pass into png)
        self.board_frame = tk.Canvas(self, width=390, height=390)
        self.board_frame.pack()

        # Buttons
        forward_button = tk.Button(parent, text=">", command=self.forward)
        backward_button = tk.Button(parent, text="<",  command=self.backward)

        self.label.pack(anchor='n')
        self.board_frame.pack(anchor='center')
        forward_button.pack(anchor='se')
        backward_button.pack(anchor='sw')

        self.update()

        

    # Rerender
    def update(self):

        # Get png from board
        svg_info = chess.svg.board(board=self.board)
        with open(TEMP_SVG, "w") as f:
            f.write(svg_info)
        drawing = svg2rlg(TEMP_SVG)
        renderPM.drawToFile(drawing, TEMP_PNG, fmt="PNG")
        self.board_image = ImageTk.PhotoImage(Image.open(TEMP_PNG))
        self.board_frame.create_image(195,195, image=self.board_image)

    # Move board forward
    def forward(self):
        if (len(self.move_stack) == 0 or self.move_to_play >= len(self.move_stack)):
            # Do nothing
            return

        self.board.push(self.move_stack[self.move_to_play])
        self.move_to_play += 1
        self.update()

    def backward(self):
        if (self.move_to_play == 0):
            # Do nothing
            return
        # else
        self.board.pop()
        self.move_to_play -= 1
        self.update()


# # Chess board class
# b = chess.Board()
# b.push_uci("e2e4")
# b.push_uci("e7e5")
# b.push_uci("b1c3")
# b.push_uci("g8f6")





