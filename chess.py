#!/usr/bin/env python3

import jsonpickle
import pygame
import socket
import time

from ChessBoard import ChessBoard
from MoveStatus import MoveStatus
from gui import Banner
from gui import Button
from utils import *


def updateDisplay(screen, img, rect, board, click = None):
  # Blit the board background image.
  screen.blit(img, rect)

  # Blit the board pieces.
  board.pygameBlit(screen)

  # Blit the current mouse select, if one is present.
  if click is not None:
    pgRect = pygameToBoardRect(click)
    rgbBlack = (0, 0, 0)
    pygame.draw.rect(screen, rgbBlack, pgRect, 3)

  # Flip the display buffer and show all blitted changes.
  pygame.display.flip()


def receiveRemoteMove(connection, board):
  validMove = False
  while not validMove:
    print("Waiting for opponent move...")

    data = connection.recv(256)
    serverMove = jsonpickle.decode(data.decode("utf-8"))
    print("Opponent move received:", serverMove)

    if chessBoard.validMove(*serverMove):
      chessBoard.movePiece(*serverMove)
      status = MoveStatus.OK
      validMove = True
    else:
      status = MoveStatus.INVALID

    print("Responding with:", status)
    response = jsonpickle.encode(status).encode("utf-8")
    connection.sendall(response)


appTitle = "python-chess"
chessBoard = ChessBoard()

pygame.init()
pygame.display.set_caption(appTitle)

backImg = pygame.image.load(resourcePath("images/backgrounds/1.jpeg"))
backRect = backImg.get_rect()
screen = pygame.display.set_mode((backRect.width, backRect.height))
screen.blit(backImg, backRect)


bannerFile = open("banner.txt", "r")
bannerText = bannerFile.read()
bannerCenter = backRect.center
banner = Banner(bannerText)
banner.blit(screen)

startRect = pygame.Rect(0, 0, 80, 20)
startRect.center = backRect.center
menuSelect = True
def stopMenuSelect():
  global menuSelect
  menuSelect = False
startButton = Button("Start!", startRect, stopMenuSelect, None)
startButton.blit(screen)

pygame.display.flip()


while menuSelect:
  time.sleep(0.1)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    startButton.handle(event, pygame.mouse.get_pos())


boardImg = pygame.image.load(resourcePath("images/boards/black-white.png"))
boardRect = boardImg.get_rect()
screen = pygame.display.set_mode((boardRect.width, boardRect.height))
edges = 40
innerRect = pygame.Rect(0, 0, boardRect.width - edges, boardRect.height - edges)
innerRect.center = boardRect.center
updateDisplay(screen, boardImg, boardRect, chessBoard)


multiplayer = False
clientSide = False

# If command line arguments found, try to set up multiplayer socket connection.
if len(sys.argv) > 1:
  multiplayer = True

  if sys.argv[1] == "server":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9992))
    sock.listen(1)
    print("Waiting for connection...")
    connection, clientAddr = sock.accept()
    print("Connection accepted from", clientAddr)

  elif sys.argv[1] == "client" and len(sys.argv) > 2:
    clientSide = True
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = (sys.argv[2], 9992)
    print("Connecting to server at ", serverAddr)
    connection.connect(serverAddr)
    print("Connected to", serverAddr)

if clientSide:
  receiveRemoteMove(connection, chessBoard)
  updateDisplay(screen, boardImg, boardRect, chessBoard)


currentClick = None
running = True
while running:
  time.sleep(0.01)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONUP:
      mousePos = pygame.mouse.get_pos()
      if currentClick is None:
        if innerRect.collidepoint(mousePos):
          currentClick = mousePos
      else:
        startBoardIndex = pygameToBoardIndex(currentClick)
        endBoardIndex = pygameToBoardIndex(mousePos)
        if chessBoard.validMove(startBoardIndex, endBoardIndex):
          if multiplayer:
            myMove = (startBoardIndex, endBoardIndex)
            myMoveBytes = jsonpickle.encode(myMove).encode("utf-8")
            print("Sending my move:", myMove)
            connection.sendall(myMoveBytes)
            print("Waiting for response...")
            responseBytes = connection.recv(512)
            status = jsonpickle.decode(responseBytes.decode("utf-8"))
            print("Received response:", status)
            if status == MoveStatus.OK:
              chessBoard.movePiece(startBoardIndex, endBoardIndex)
              updateDisplay(screen, boardImg, boardRect, chessBoard)
              receiveRemoteMove(connection, chessBoard)
          else:
            chessBoard.movePiece(startBoardIndex, endBoardIndex)

        currentClick = None

      updateDisplay(screen, boardImg, boardRect, chessBoard, currentClick)

if multiplayer:
  connection.close()


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
