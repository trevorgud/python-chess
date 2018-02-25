#!/usr/bin/env python3

from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = 2


class Piece(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    CASTLE = 4
    QUEEN = 5
    KING = 6


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


class ChessBoard():
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

    _chessBoard = [
        [BLACK_CASTLE, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN,
            BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_CASTLE],
        [BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN,
            BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, 
            WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN],
        [WHITE_CASTLE, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN,
            WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_CASTLE],
    ]

    def movePiece(self, firstPos, secondPos):
        piece = self._chessBoard[firstPos[0]][firstPos[1]]
        # TODO: Check if the move is valid.
        # Not necessarily within this function.
        self._chessBoard[firstPos[0]][firstPos[1]] = None
        self._chessBoard[secondPos[0]][secondPos[1]] = piece

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


chessBoard = ChessBoard()

while(True):
    print(chessBoard)
    move = input("move: ")
    if(move == "exit" or move == "quit" or move == "q"):
    	exit()
    moveIndex = inputToIndex(move)
    if(moveIndex is not None):
        chessBoard.movePiece(moveIndex[0], moveIndex[1])
    else:
        print("Invalid input")