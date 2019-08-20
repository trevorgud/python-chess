from Color import Color

class ChessState():
  def __init__(self, chessBoard):
    self.chessBoard = chessBoard
    self.turn = Color.WHITE
    self.kingMoved = {Color.WHITE: False, Color.BLACK: False}
    self.castle1Moved = {Color.WHITE: False, Color.BLACK: False}
    self.castle2Moved = {Color.WHITE: False, Color.BLACK: False}
