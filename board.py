import pygame as pg
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
import square
import king
import queen
import rook
import bishop
import knight
import pawn
import tkinter as tk
import os
import tktable
import sys
import traceback
from pgwindowinfo import *

import subprocess
#from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QHeaderView, QAbstractScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

# Define colours and constants
light_brown = (250, 190, 120)
brown = (150,75,0)
blue = (0, 0, 128)
green = (0, 255, 0)
board_width = board_height = 850
squareCenters = []
SQUARE_SIZE = 100

class Timer:

    def __init__(self, colour):
        pg.init()
        self.colour = colour
        self.font = pg.font.Font('freesansbold.ttf', 20)
        self.clock = pg.time.Clock()
        self.start_time = 0
        self.passed_time = 0
        self.time_before_move = 60
        self.timer_started = False

        if self.colour == 'white':
            self.position = (850, 200)
        else:
            self.position = (850, 630)

# class WorkerSignals(QObject):
#     '''
#     Defines the signals available from a running worker thread.

#     Supported signals are:

#     finished
#         No data
    
#     error
#         `tuple` (exctype, value, traceback.format_exc() )
    
#     result
#         `object` data returned from processing, anything

#     progress
#         `int` indicating % progress 

#     '''
#     finished = pyqtSignal()
#     error = pyqtSignal(tuple)
#     result = pyqtSignal(object)
#     progress = pyqtSignal(int)

# class Worker(QRunnable):
#     def __init__(self, fn, *args, **kwargs):
#         super(Worker, self).__init__()

#         # Store constructor arguments (re-used for processing)
#         self.fn = fn
#         self.args = args
#         self.kwargs = kwargs
#         self.signals = WorkerSignals()    

#         # Add the callback to our kwargs
#         self.kwargs['progress_callback'] = self.signals.progress        

#     @pyqtSlot()
#     def run(self):
#         '''
#         Initialise the runner function with passed args, kwargs.
#         '''
        
#         # Retrieve args/kwargs here; and fire processing using them
#         try:
#             result = self.fn(*self.args, **self.kwargs)
#         except:
#             traceback.print_exc()
#             exctype, value = sys.exc_info()[:2]
#             self.signals.error.emit((exctype, value, traceback.format_exc()))
#         else:
#             self.signals.result.emit(result)  # Return the result of the processing
#         finally:
#             self.signals.finished.emit()  # Done

class MainWindow(QWidget):

    def __init__(self, pgwindowpos, colour):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 875
        self.top = 357 
        self.width = 300
        self.height = 200
        self.initUI(pgwindowpos, colour)
        
    def initUI(self, pgwindowpos, colour):
        #self.setWindowTitle(self.title)
        self.setWindowTitle(colour)
        self.setGeometry(self.left + pgwindowpos['left'], self.top + pgwindowpos['top'], self.width, self.height)
        
        self.createTable(pgwindowpos, colour)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()

    def createTable(self, pgwindowpos, colour):
       # Create table
        self.tableWidget = QTableWidget()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['White Moves', 'Black Moves'])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
    # def progress_fn(self, n):
    #     print("%d%% done" % n)

    # def execute_this_fn(self, progress_callback):
    #     for n in range(0, 5):
    #         time.sleep(1)
    #         progress_callback.emit(n*100/4)
            
    #     return "Done."
 
    # def print_output(self, s):
    #     print(s)
        
    # def thread_complete(self):
    #     print("THREAD COMPLETE!")
 
    # def oh_no(self):
    #     # Pass the function to execute
    #     worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
    #     worker.signals.result.connect(self.print_output)
    #     worker.signals.finished.connect(self.thread_complete)
    #     worker.signals.progress.connect(self.progress_fn)
        
    #     # Execute
    #     self.threadpool.start(worker) 

        
    # def recurring_timer(self):
    #     self.counter +=1
    #     self.l.setText("Counter: %d" % self.counter)



class Board:

    def __init__(self, w, h, name):
        self.width = w
        self.height = h
        self.tk = tk.Tk()
        pg.init()
        self.screen = pg.display.set_mode((w,h))
        pg.display.set_caption(name)
        self.squares = pg.sprite.Group()
        self.pieces = pg.sprite.Group()
        self.white_pieces = pg.sprite.Group()
        self.black_pieces = pg.sprite.Group()
        self.timer = 10

        if name.split()[2] == 'white':
            self.buildBoard(self, 'white')
        else:
            self.buildBoard(self, 'black')
        self.setupBoard(self)

        # Must set this env var for PygameWindowInfo to work!
        os.environ['SDL_VIDEO_WINDOW_POS'] = "128,128"

        window = PygameWindowInfo()
        winPos = window.getWindowPosition()

        self.app = QApplication(sys.argv)
        self.move_table = MainWindow(winPos, name.split()[2])
        #sys.exit(app.exec_())

        # app = QApplication([])
        # label = QLabel('Hello World!')
        # label.show()
        # app.exec_()

        # master = tk.Tk()
        # master.geometry('500x200+250+200')
        # master.title('Dogs')
        #### DEFINING THE TABLE ####
        # self.tk.geometry('250x400+825+225')
        # table = tk.Frame(self.tk)
        # table.grid()
        # tk.mainloop()


    # Toggles between the two colours 
    def alternate_colours(self):
        while True:
            yield brown
            yield light_brown

        # Create an 8x8 grid
    def buildBoard(self, board, perspective):

        # Create a 'toggler'
        alternator = self.alternate_colours()

        increment = 100

        if perspective == 'white':
            cur_colour = light_brown

            coords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

            # Starting at the top left-hand corner (0, 0), create the board    
            for column in range(8):
                for row in range(8):
                    new_square = square.Square(Rect(row * increment + 25, column * increment + 25, increment + 1, increment + 1), f'{coords[row]}{8 - column}', cur_colour)
                    if new_square not in squareCenters:
                        squareCenters.append(new_square)
                    self.squares.add(new_square)
                    pg.draw.rect(self.screen, cur_colour, (new_square.x, new_square.y, 100, 100))
                    if column == 7:
                        font = pg.font.Font('freesansbold.ttf', 20)
                        text = font.render(f'{coords[row]}', True, green, (0, 0, 0))  
                        # create a rectangular object for the 
                        # text surface object 
                        textRect = text.get_rect()  
                        
                        # set the center of the rectangular object. 
                        textRect.center = (new_square.x + 50, new_square.y + 113) 
                        self.screen.blit(text, textRect) 

                    if row == 0:
                        font = pg.font.Font('freesansbold.ttf', 20)
                        text = font.render(f'{8 - column}', True, green, (0, 0, 0))  
                        # create a rectangular object for the 
                        # text surface object 
                        textRect = text.get_rect()  
                        
                        # set the center of the rectangular object. 
                        textRect.center = (new_square.x - 13, new_square.y + 50) 
                        self.screen.blit(text, textRect) 

                    cur_colour = next(alternator) 
                cur_colour = next(alternator)
        
        else:
            cur_colour = light_brown

            coords = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

            # Starting at the top left-hand corner (0, 0), create the board    
            for column in range(8):
                for row in range(8):
                    new_square = square.Square(Rect(row * increment + 25, column * increment + 25, increment + 1, increment + 1), f'{coords[row]}{column + 1}', cur_colour)
                    if new_square not in squareCenters:
                        squareCenters.append(new_square)
                    self.squares.add(new_square)
                    pg.draw.rect(self.screen, cur_colour, (new_square.x, new_square.y, 100, 100))

                    if column == 7:
                        font = pg.font.Font('freesansbold.ttf', 20)
                        text = font.render(f'{coords[row]}', True, green, (0, 0, 0))  
                        # create a rectangular object for the 
                        # text surface object 
                        textRect = text.get_rect()  
                        
                        # set the center of the rectangular object. 
                        textRect.center = (new_square.x + 50, new_square.y + 113) 
                        self.screen.blit(text, textRect) 

                    if row == 0:
                        font = pg.font.Font('freesansbold.ttf', 20)
                        text = font.render(f'{column + 1}', True, green, (0, 0, 0))  
                        # create a rectangular object for the 
                        # text surface object 
                        textRect = text.get_rect()  
                        
                        # set the center of the rectangular object. 
                        textRect.center = (new_square.x - 13, new_square.y + 50) 
                        self.screen.blit(text, textRect) 
                    cur_colour = next(alternator) 
                cur_colour = next(alternator)
    
        # move_list_board = Rect(875, 225, 1, 1)
        # pg.draw.rect(self.screen, (255, 255, 255), (move_list_board.x, move_list_board.y, 275, 405))
        # pg.draw.line(self.screen, (0, 0, 0), (move_list_board.x + 137.5, move_list_board.y), (move_list_board.x + 137.5, 875), 5)

    # Places the pieces in their correct starting positions
    def setupBoard(self, board):
        white_king = None
        black_king = None
        
        # Get all squares of interest
        eligible_squares = [square for square in self.squares if square.rank == 1 or square.rank == 2 or square.rank == 7 or square.rank == 8]
        
        for square in eligible_squares:
            
            # Set the colour
            if square.rank == 1 or square.rank == 2:
                colour = 'white'
            else:
                colour = 'black'

            # Determine which piece to be created based on rank and column
            if square.rank == 2 or square.rank == 7:
                piece = pawn.Pawn(square, colour)

            else:
                if square.file == 'A' or square.file == 'H':
                    piece = rook.Rook(square, colour)

                elif square.file == 'B' or square.file == 'G':
                    piece = knight.Knight(square, colour)

                elif square.file == 'C' or square.file == 'F':
                    piece = bishop.Bishop(square, colour)
            
                elif square.file == 'D':
                    piece = queen.Queen(square, colour)

                else:
                    piece = king.King(square, colour)
                    if square.id == 'E1':
                        white_king = piece
                    else:
                        black_king = piece

            self.pieces.add(piece)
            
            # While we are here, set square.isOccupied to be True, since when square objects are created, these are set to be False.
            square.isOccupied = True
            square.occupied_colour = colour

            self.screen.blit(piece.image, piece.rect)
            pg.display.update()  
        
        # Add pieces to appropriate groups
        for piece in self.pieces:
            if piece.colour == 'white':
                self.white_pieces.add(piece)
            else:
                self.black_pieces.add(piece)

        # We need to get the legal moves for each piece on startup, since if a king is selected to move
        # we need to check that no opponent's piece is controlling a given surrounding square of that king.
        # But since knights can move before every other piece has been moved, we account for that by getting every piece's available moves right away.
        for piece in self.pieces:
            
            # Get the legal moves for the current piece.
            if piece.name == 'King':
                piece.get_legal_moves(self.squares, self.pieces, None, None)
                if piece.colour == 'white':
                    white_king = piece
                else:
                    black_king = piece
            else:
                piece.get_legal_moves(self.squares, self.pieces, None, None)
            
            # Update pawn attribute.
            if piece.name == 'Pawn':
                piece.first_move = True

            # Now get each piece's king and its opponent's king.
            for k in [piece for piece in self.pieces if piece.name == 'King']:
                if piece.colour == k.colour:
                    piece.our_king = k
                else:
                    piece.opponents_king = k
        
        return white_king, black_king