from enum import Enum

from Color import Color
from Piece import Piece

class Pieces(Enum):
  def __init__(self, pieceType, color):
    self.pieceType = pieceType
    self.color = color

  def __str__(self):
    if(self.color is Color.WHITE):
      colorStr = "W"
    elif(self.color is Color.BLACK):
      colorStr  = "B"

    if(self.pieceType is Piece.PAWN):
      pieceStr = "P"
    elif(self.pieceType is Piece.KNIGHT):
      pieceStr = "K"
    elif(self.pieceType is Piece.BISHOP):
      pieceStr = "B"
    elif(self.pieceType is Piece.CASTLE):
      pieceStr = "C"
    elif(self.pieceType is Piece.QUEEN):
      pieceStr = "Q"
    elif(self.pieceType is Piece.KING):
      pieceStr = "K"

    return colorStr + pieceStr

  WHITE_PAWN = Piece.PAWN, Color.WHITE
  WHITE_KNIGHT = Piece.KNIGHT, Color.WHITE
  WHITE_BISHOP = Piece.BISHOP, Color.WHITE
  WHITE_CASTLE = Piece.CASTLE, Color.WHITE
  WHITE_QUEEN = Piece.QUEEN, Color.WHITE
  WHITE_KING = Piece.KING, Color.WHITE
  BLACK_PAWN = Piece.PAWN, Color.BLACK
  BLACK_KNIGHT = Piece.KNIGHT, Color.BLACK
  BLACK_BISHOP = Piece.BISHOP, Color.BLACK
  BLACK_CASTLE = Piece.CASTLE, Color.BLACK
  BLACK_QUEEN = Piece.QUEEN, Color.BLACK
  BLACK_KING = Piece.KING, Color.BLACK
