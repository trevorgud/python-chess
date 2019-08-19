from ChessPiece import ChessPiece
from Color import Color
from Piece import Piece

class PieceSet():
    WHITE_PAWN = ChessPiece(Piece.PAWN, Color.WHITE)
    WHITE_KNIGHT = ChessPiece(Piece.KNIGHT, Color.WHITE)
    WHITE_BISHOP = ChessPiece(Piece.BISHOP, Color.WHITE)
    WHITE_CASTLE = ChessPiece(Piece.CASTLE, Color.WHITE)
    WHITE_QUEEN = ChessPiece(Piece.QUEEN, Color.WHITE)
    WHITE_KING = ChessPiece(Piece.KING, Color.WHITE)
    BLACK_PAWN = ChessPiece(Piece.PAWN, Color.BLACK)
    BLACK_KNIGHT = ChessPiece(Piece.KNIGHT, Color.BLACK)
    BLACK_BISHOP = ChessPiece(Piece.BISHOP, Color.BLACK)
    BLACK_CASTLE = ChessPiece(Piece.CASTLE, Color.BLACK)
    BLACK_QUEEN = ChessPiece(Piece.QUEEN, Color.BLACK)
    BLACK_KING = ChessPiece(Piece.KING, Color.BLACK)
