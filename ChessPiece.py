from Color import Color
from Piece import Piece

class ChessPiece():
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
