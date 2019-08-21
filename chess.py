#!/usr/bin/env python3

import datetime
import pygame
import socket
import tkinter as tk

from ActionLog import ActionLog
from ChessBoard import ChessBoard
from TkLogList import TkLogList
from utils import *


# If command line arguments found, try to set up multiplayer socket connection.
if len(sys.argv) > 1:
  if sys.argv[1] == "server":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9992))
    sock.listen(1)
    print("Waiting for connection...")
    connection, clientAddr = sock.accept()
    print("Connection accepted from", clientAddr)
    print("Sending test data...")
    message = "Test sending some data from server side."
    connection.sendall(message.encode("utf-8"))
    print("Closing connection.")
    connection.close()

  elif sys.argv[1] == "client" and len(sys.argv) > 2:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = (sys.argv[2], 9992)
    print('Connecting to server at ', serverAddr)
    sock.connect(serverAddr)
    data = sock.recv(256000)
    print("Test data received:", data.decode("utf-8"))
    print("Closing connection.")
    sock.close()

  exit()


# If no command line arguments, assume local game.
appTitle = "python-chess"
chessBoard = ChessBoard()

root = tk.Tk()
root.title(appTitle)

logs = [ActionLog(time = datetime.datetime.now(), msg = "Starting...")]
tkLogList = TkLogList(elem = root, logs = logs)
tkLogList.pack()

root.update()

pygame.init()
pygame.display.set_caption(appTitle)
screen = pygame.display.set_mode((440, 440))
boardImg = pygame.image.load(resourcePath("images/boards/black-white.png"))
boardRect = boardImg.get_rect()
innerRect = (20, 20, 8 * 50, 8 * 50)

currentMousePos = None
running = True
while running:
  root.update()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONUP:
      mousePos = pygame.mouse.get_pos()
      if currentMousePos is None:
        if isWithinBound(mousePos, innerRect):
          currentMousePos = mousePos
      else:
        startBoardIndex = pygameToBoardIndex(currentMousePos)
        endBoardIndex = pygameToBoardIndex(mousePos)
        moveStr = str(startBoardIndex) + " to " + str(endBoardIndex)
        time = datetime.datetime.now()
        if chessBoard.validMove(startBoardIndex, endBoardIndex):
          chessBoard.movePiece(startBoardIndex, endBoardIndex)
          logs.append(ActionLog(time, "Moved: " + moveStr))
        else:
          logs.append(ActionLog(time, "Invalid move: " + moveStr))
        currentMousePos = None
        tkLogList.destroy()
        tkLogList = TkLogList(elem = root, logs = logs)
        tkLogList.pack()

    # Blit the board background image.
    screen.blit(boardImg, boardRect)

    # Blit the board pieces.
    chessBoard.pygameBlit(screen)

    # Blit the current mouse select, if one is present.
    if currentMousePos is not None:
      pgRect = pygameToBoardRect(currentMousePos)
      rgbBlack = (0, 0, 0)
      pygame.draw.rect(screen, rgbBlack, pgRect, 3)

    # Flip the display buffer and show all blitted changes.
    pygame.display.flip()


# TODO: Allow selection between command line and GUI chess modes.
# while(True):
#   print(chessBoard)
#   move = input("move: ")
#   if(move == "exit" or move == "quit" or move == "q"):
#     exit()
#   moveIndex = inputToIndex(move)
#   if(moveIndex is not None):
#     chessBoard.movePiece(moveIndex[0], moveIndex[1])
#   else:
#     print("Invalid input")
