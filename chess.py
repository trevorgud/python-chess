#!/usr/bin/env python3

import jsonpickle
import pygame
import socket
import time

from ChessBoard import ChessBoard
from MoveStatus import MoveStatus
from gui import Banner, Button, CheckStatus, Text, TextInput, TurnText
from utils import *


def updateDisplay(screen, img, rect, board, click = None):
  # Blit the board background image.
  screen.blit(img, rect)

  # Blit the board pieces.
  board.pygameBlit(screen)

  # Blit the current mouse select, if one is present.
  if click is not None and not board.isCheckmate():
    pgRect = pygameToBoardRect(click)
    rgbBlack = (0, 0, 0)
    pygame.draw.rect(screen, rgbBlack, pgRect, 3)

  rgbGrey = (153, 153, 153)
  edge = 4
  menuRect = pygame.Rect(edge, rect.height - edge, rect.width - (2 * edge), 50)
  pygame.draw.rect(screen, rgbGrey, menuRect)

  turnRect = pygame.Rect(16, menuRect.top, 80, 16)
  turnText = TurnText(board.turn(), turnRect)
  turnText.blit(screen)

  checkRect = pygame.Rect(16, turnRect.top + turnRect.height, 80, 16)
  checkStatus = CheckStatus(board.isCheck(), board.isCheckmate(), checkRect)
  checkStatus.blit(screen)

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


def initConnection():
  global multiplayer, connection, clientSide, textInput
  multiplayer = True
  if len(textInput.text) == 0:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9992))
    sock.listen(1)
    print("Waiting for connection...")
    connection, clientAddr = sock.accept()
    print("Connection accepted from", clientAddr)
  else:
    clientSide = True
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = (textInput.text, 9992)
    print("Connecting to server at ", serverAddr)
    connection.connect(serverAddr)
    print("Connected to", serverAddr)


appTitle = "python-chess"
chessBoard = ChessBoard()
multiplayer = False
clientSide = False
connection = None

pygame.init()
pygame.display.set_caption(appTitle)
pygame.key.set_repeat(500, 25)

backImg = pygame.image.load(resourcePath("images/backgrounds/1.jpeg"))
backRect = backImg.get_rect()
screen = pygame.display.set_mode((backRect.width, backRect.height))

bannerFile = open("banner.txt", "r")
bannerText = bannerFile.read()
bannerCenter = backRect.center
banner = Banner(bannerText)

menuSelect = True

localRect = pygame.Rect(0, 0, 80, 20)
localRect.center = backRect.center
def localSelect():
  global menuSelect
  menuSelect = False
localButton = Button("Local", localRect, localSelect, None)

inputRect = localRect.copy()
inputRect.width += 75
inputRect.center = localRect.center
inputRect.top += 25
textInput = TextInput(inputRect, 15)
labelRect = inputRect.copy()
labelRect.left -= 50
labelRect.width = 25
inputLabel = Text("Host IP:", labelRect.center)

connRect = localRect.copy()
connRect.center = backRect.center
connRect.left -= 85
def connSelect():
  global menuSelect
  menuSelect = False
  initConnection()
connButton = Button("Online", connRect, connSelect, None)

aiRect = localRect.copy()
aiRect.center = backRect.center
aiRect.left += 85
aiButton = Button("AI", aiRect, lambda: None, None)

displayElems = [banner, inputLabel]
guiElems = [textInput, localButton, connButton, aiButton]

while menuSelect:
  time.sleep(0.01)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    for elem in guiElems:
      elem.handle(event, pygame.mouse.get_pos())
    screen.blit(backImg, backRect)
    for elem in displayElems + guiElems:
      elem.blit(screen)
    pygame.display.flip()

boardImg = pygame.image.load(resourcePath("images/boards/black-white.png"))
boardRect = boardImg.get_rect()
screenRect = boardRect.copy()
screenRect.height += 50
screen = pygame.display.set_mode((screenRect.width, screenRect.height))
edges = 40
innerRect = pygame.Rect(0, 0, boardRect.width - edges, boardRect.height - edges)
innerRect.center = boardRect.center
updateDisplay(screen, boardImg, boardRect, chessBoard)

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
