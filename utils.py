import math
import os
import sys

def resourcePath(relative):
  if hasattr(sys, "_MEIPASS"):
    return os.path.join(sys._MEIPASS, relative)
  return os.path.join(relative)

def inputToIndex(userInput):
  tokens = userInput.split(" ")
  if(len(tokens) == 2 and len(tokens[0]) == 2 and len(tokens[1]) == 2):
    firstPos = tokens[0]
    secondPos = tokens[1]
    atoi = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    firstCol = atoi.get(firstPos[0])
    secondCol = atoi.get(secondPos[0])
    try:
      firstRow = int(firstPos[1])
      secondRow = int(secondPos[1])
    except ValueError:
      return None
    if(firstCol is None or secondCol is None or
      firstRow < 1 or firstRow > 8 or secondRow < 1 or secondRow > 8):
      return None
    return ((8 - firstRow, firstCol), (8 - secondRow, secondCol))
  else:
    return None

def pygameToBoardIndex(screenPos):
  xnew = math.floor((screenPos[1] - 20) / 50)
  ynew = math.floor((screenPos[0] - 20) / 50)
  return (xnew, ynew)

def pygameToBoardRect(screenPos):
  # Board index is inverted from pygame index.
  y, x = pygameToBoardIndex(screenPos)
  xScreen = x * 50 + 20
  yScreen = y * 50 + 20
  width = 50
  height = 50
  return (xScreen, yScreen, width, height)

def isWithinBound(pos, bound):
  x, y = pos
  xBound, yBound, width, height = bound
  return (x >= xBound and y >= yBound and
    x <= xBound + width and y <= yBound + width)
