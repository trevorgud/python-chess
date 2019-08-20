import pygame

from ChessRules import ChessRules
from PieceSet import PieceSet
from utils import resourcePath

class ChessBoard():
  _pieces = PieceSet()
  _chessBoard = [
    [_pieces.BLACK_CASTLE, _pieces.BLACK_KNIGHT, _pieces.BLACK_BISHOP,
      _pieces.BLACK_QUEEN, _pieces.BLACK_KING, _pieces.BLACK_BISHOP,
      _pieces.BLACK_KNIGHT, _pieces.BLACK_CASTLE],
    [_pieces.BLACK_PAWN, _pieces.BLACK_PAWN, _pieces.BLACK_PAWN,
      _pieces.BLACK_PAWN, _pieces.BLACK_PAWN, _pieces.BLACK_PAWN,
      _pieces.BLACK_PAWN, _pieces.BLACK_PAWN],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [_pieces.WHITE_PAWN, _pieces.WHITE_PAWN, _pieces.WHITE_PAWN,
      _pieces.WHITE_PAWN, _pieces.WHITE_PAWN, _pieces.WHITE_PAWN,
      _pieces.WHITE_PAWN, _pieces.WHITE_PAWN],
    [_pieces.WHITE_CASTLE, _pieces.WHITE_KNIGHT, _pieces.WHITE_BISHOP,
      _pieces.WHITE_QUEEN, _pieces.WHITE_KING, _pieces.WHITE_BISHOP,
      _pieces.WHITE_KNIGHT, _pieces.WHITE_CASTLE]
  ]
  _rules = ChessRules(_chessBoard, _pieces)

  _pieceDir = "images/pieces"
  _whiteDir = _pieceDir + "/default-white"
  _blackDir = _pieceDir + "/default-black"
  images = {
    _pieces.WHITE_PAWN: pygame.image.load(resourcePath(_whiteDir + "/pawn.png")),
    _pieces.WHITE_KNIGHT: pygame.image.load(resourcePath(_whiteDir + "/knight.png")),
    _pieces.WHITE_BISHOP: pygame.image.load(resourcePath(_whiteDir + "/bishop.png")),
    _pieces.WHITE_CASTLE: pygame.image.load(resourcePath(_whiteDir + "/castle.png")),
    _pieces.WHITE_QUEEN: pygame.image.load(resourcePath(_whiteDir + "/queen.png")),
    _pieces.WHITE_KING: pygame.image.load(resourcePath(_whiteDir + "/king.png")),
    _pieces.BLACK_PAWN: pygame.image.load(resourcePath(_blackDir + "/pawn.png")),
    _pieces.BLACK_KNIGHT: pygame.image.load(resourcePath(_blackDir + "/knight.png")),
    _pieces.BLACK_BISHOP: pygame.image.load(resourcePath(_blackDir + "/bishop.png")),
    _pieces.BLACK_CASTLE: pygame.image.load(resourcePath(_blackDir + "/castle.png")),
    _pieces.BLACK_QUEEN: pygame.image.load(resourcePath(_blackDir + "/queen.png")),
    _pieces.BLACK_KING: pygame.image.load(resourcePath(_blackDir + "/king.png"))
  }

  def validMove(self, startPos, endPos):
    return self._rules.validMove(startPos, endPos)

  def movePiece(self, startPos, endPos):
    self._rules.movePiece(startPos, endPos)

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
          pieceImage = self.images[piece]
          pieceRect = pieceImage.get_rect().move(dx, dy)
          screen.blit(pieceImage, pieceRect)
        columnIndex += 1
      rowIndex += 1
