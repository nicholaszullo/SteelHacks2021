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
        self.board = input_board

        # Boilerplate grid code
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = ChessBoard(container, self)
        self.frames[ChessBoard] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ChessBoard)

        self.update()
        

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


# Start page class (from boilerplate)
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)


# Chessboard class

class ChessBoard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        # Instance variables
        self.move_stack = parent.board.move_stack
        self.board = chess.Board()
        self.move_to_play = 0

        # Header
        label = tk.Label(self, text="ChessBoard", font=LARGE_FONT)
        label.pack(anchor='N')

        # Board (make svg and pass into png)
        self.board_frame = tk.Canvas(self, width=390, height=390)
        self.board_frame.pack()

        # Buttons
        forward_button = tk.Button(parent, text=">", command=self.forward)
        backward_button = tk.Button(parent, text="<",  command=self.backward)
        forward_button.pack()
        backward_button.pack()

        

    # Rerender
    def update(self):

        # Get png from board
        svg_info = chess.svg.board(board=self.board)
        with open(TEMP_SVG, "w") as f:
            f.write(svg_info)
        drawing = svg2rlg(TEMP_SVG)
        renderPM.drawToFile(drawing, TEMP_PNG, fmt="PNG")
        self.board_image = ImageTk.PhotoImage(Image.open(TEMP_PNG))
        self.board_frame.create_image(0,0,image=self.board_image)

    # Move board forward
    def forward(self):
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




    



# Chess board class
b = chess.Board()
app = Application(b)
app.mainloop()





