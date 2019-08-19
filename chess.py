#!/usr/bin/env python3

import datetime
import pygame
import tkinter as tk

from ActionLog import ActionLog
from ChessBoard import ChessBoard
from ChessRules import ChessRules
from Color import Color
from Piece import Piece
from PieceSet import PieceSet
from TkLogList import TkLogList
from utils import *


appTitle = "python-chess"
chessBoard = ChessBoard()

logs = [ActionLog(time = datetime.datetime.now(), msg = "Starting...")]

root = tk.Tk()
root.title(appTitle)

tkLogList = TkLogList(elem = root, logs = logs)
tkLogList.pack()

root.update()

pygame.init()
pygame.display.set_caption(appTitle)
screen = pygame.display.set_mode((440, 440))
board = pygame.image.load(resourcePath("images/boards/black-white.png"))
boardRect = board.get_rect()

currentMouseSelect = None
running = True
while running:
    root.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # TODO: Don't register clicks that are out of bounds.
            if currentMouseSelect is None:
                currentMouseSelect = pygame.mouse.get_pos()
            else:
                newMouseSelect = pygame.mouse.get_pos()
                startBoardIndex = pygameToBoardIndex(currentMouseSelect)
                endBoardIndex = pygameToBoardIndex(newMouseSelect)
                moveStr = str(startBoardIndex) + " to " + str(endBoardIndex)
                time = datetime.datetime.now()
                if(chessBoard.validMove(startBoardIndex, endBoardIndex)):
                    chessBoard.movePiece(startBoardIndex, endBoardIndex)
                    logs.append(ActionLog(time, "Moved: " + moveStr))
                else:
                    logs.append(ActionLog(time, "Invalid move: " + moveStr))
                currentMouseSelect = None
                tkLogList.destroy()
                tkLogList = TkLogList(elem = root, logs = logs)
                tkLogList.pack()

        screen.blit(board, boardRect)
        chessBoard.pygameBlit(screen)
        pygame.display.flip()

# TODO: Allow selection between command line and GUI chess modes.
# while(True):
#     print(chessBoard)
#     move = input("move: ")
#     if(move == "exit" or move == "quit" or move == "q"):
#       exit()
#     moveIndex = inputToIndex(move)
#     if(moveIndex is not None):
#         chessBoard.movePiece(moveIndex[0], moveIndex[1])
#     else:
#         print("Invalid input")
