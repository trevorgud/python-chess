import pygame

from ChessRules import ChessRules
from Pieces import Pieces
from utils import resourcePath

class ChessBoard():
  _chessBoard = [
    [Pieces.BLACK_CASTLE, Pieces.BLACK_KNIGHT, Pieces.BLACK_BISHOP,
      Pieces.BLACK_QUEEN, Pieces.BLACK_KING, Pieces.BLACK_BISHOP,
      Pieces.BLACK_KNIGHT, Pieces.BLACK_CASTLE],
    [Pieces.BLACK_PAWN, Pieces.BLACK_PAWN, Pieces.BLACK_PAWN,
      Pieces.BLACK_PAWN, Pieces.BLACK_PAWN, Pieces.BLACK_PAWN,
      Pieces.BLACK_PAWN, Pieces.BLACK_PAWN],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [Pieces.WHITE_PAWN, Pieces.WHITE_PAWN, Pieces.WHITE_PAWN,
      Pieces.WHITE_PAWN, Pieces.WHITE_PAWN, Pieces.WHITE_PAWN,
      Pieces.WHITE_PAWN, Pieces.WHITE_PAWN],
    [Pieces.WHITE_CASTLE, Pieces.WHITE_KNIGHT, Pieces.WHITE_BISHOP,
      Pieces.WHITE_QUEEN, Pieces.WHITE_KING, Pieces.WHITE_BISHOP,
      Pieces.WHITE_KNIGHT, Pieces.WHITE_CASTLE]
  ]
  _rules = ChessRules(_chessBoard)

  _pieceDir = "images/pieces"
  _whiteDir = _pieceDir + "/default-white"
  _blackDir = _pieceDir + "/default-black"
  _images = {
    Pieces.WHITE_PAWN: pygame.image.load(resourcePath(_whiteDir + "/pawn.png")),
    Pieces.WHITE_KNIGHT: pygame.image.load(resourcePath(_whiteDir + "/knight.png")),
    Pieces.WHITE_BISHOP: pygame.image.load(resourcePath(_whiteDir + "/bishop.png")),
    Pieces.WHITE_CASTLE: pygame.image.load(resourcePath(_whiteDir + "/castle.png")),
    Pieces.WHITE_QUEEN: pygame.image.load(resourcePath(_whiteDir + "/queen.png")),
    Pieces.WHITE_KING: pygame.image.load(resourcePath(_whiteDir + "/king.png")),
    Pieces.BLACK_PAWN: pygame.image.load(resourcePath(_blackDir + "/pawn.png")),
    Pieces.BLACK_KNIGHT: pygame.image.load(resourcePath(_blackDir + "/knight.png")),
    Pieces.BLACK_BISHOP: pygame.image.load(resourcePath(_blackDir + "/bishop.png")),
    Pieces.BLACK_CASTLE: pygame.image.load(resourcePath(_blackDir + "/castle.png")),
    Pieces.BLACK_QUEEN: pygame.image.load(resourcePath(_blackDir + "/queen.png")),
    Pieces.BLACK_KING: pygame.image.load(resourcePath(_blackDir + "/king.png"))
  }

  def validMove(self, startPos, endPos):
    return self._rules.validMove(startPos, endPos)

  def movePiece(self, startPos, endPos):
    self._rules.movePiece(startPos, endPos)

  def turn(self):
    return self._rules.turn()

  def isCheck(self):
    return self._rules.isCheck()

  def isCheckmate(self):
    return self._rules.isCheckmate()

  def __str__(self):
    boardStr = ""
    rowIndex = 8
    for row in self._chessBoard:
      boardStr += str(rowIndex)
      for column in row:
        boardStr += " "
        if(column is not None):
          boardStr += str(column)
        else:
          boardStr += "00"
      boardStr += "\n"
      rowIndex -= 1
    boardStr += "  a  b  c  d  e  f  g  h\n"
    return boardStr

  def boardToPygameIndex(self, xpos, ypos):
    return (20 + (ypos * 50), 20 + (xpos * 50))

  def pygameBlit(self, screen):
    rowIndex = 0
    for row in self._chessBoard:
      columnIndex = 0
      for piece in row:
        if(piece is not None):
          (dx, dy) = self.boardToPygameIndex(rowIndex, columnIndex)
          pieceImage = self._images[piece]
          pieceRect = pieceImage.get_rect().move(dx, dy)
          screen.blit(pieceImage, pieceRect)
        columnIndex += 1
      rowIndex += 1
