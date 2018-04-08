#!/usr/bin/env python3

from enum import Enum
import math
import numpy
import pygame


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
    def __init__(self, pieceType, color, image):
        self.pieceType = pieceType
        self.color = color
        self.image = image

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


# TODO: Detect check and checkmate conditions within the rules.
class ChessRules():
    def __init__(self, chessBoard):
        self._chessBoard = chessBoard
        self.turn = Color.WHITE
        self.boardWidth = 8
        self.boardHeight = 8

    def _switchTurn(self):
        if(self.turn == Color.WHITE):
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE

    def movePiece(self, startPos, endPos):
        piece = self._chessBoard[startPos[0]][startPos[1]]
        self._chessBoard[startPos[0]][startPos[1]] = None
        self._chessBoard[endPos[0]][endPos[1]] = piece
        self._switchTurn()

    def validMove(self, startPos, endPos):
        if(startPos[0] >= self.boardHeight or startPos[0] < 0 or
            startPos[1] >= self.boardWidth or startPos[1] < 0 or
            endPos[0] >= self.boardHeight or endPos[0] < 0 or
            endPos[1] >= self.boardWidth or endPos[1] < 0):
            return False

        startPiece = self._chessBoard[startPos[0]][startPos[1]]
        endPiece = self._chessBoard[endPos[0]][endPos[1]]
        if(startPos == endPos or
            startPiece == None or
            startPiece.color != self.turn or
            (endPiece != None and startPiece.color == endPiece.color)):
            return False

        if(startPiece.pieceType == Piece.PAWN):
            return self._validPawnMove(startPos, endPos)
        elif(startPiece.pieceType == Piece.KNIGHT):
            return self._validKnightMove(startPos, endPos)
        elif(startPiece.pieceType == Piece.BISHOP):
            return self._validBishopMove(startPos, endPos)
        elif(startPiece.pieceType == Piece.CASTLE):
            return self._validCastleMove(startPos, endPos)
        elif(startPiece.pieceType == Piece.QUEEN):
            return self._validQueenMove(startPos, endPos)
        elif(startPiece.pieceType == Piece.KING):
            return self._validKingMove(startPos, endPos)
        else:
            return False

    def _validPawnMove(self, startPos, endPos):
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        endPiece = self._chessBoard[endPos[0]][endPos[1]]
        startPiece = self._chessBoard[startPos[0]][startPos[1]]
        # Enforce the directionality of piece colors.
        if((startPiece.color == Color.BLACK and dx < 1) or
            (startPiece.color == Color.WHITE and dx > -1)):
            return False

        dx = abs(dx)
        # Normal one space move.
        if(dx == 1 and dy == 0 and endPiece == None):
            return True
        # Attack move.
        elif(dx == 1 and
            abs(dy) == 1 and
            endPiece != None and
            endPiece.color != startPiece.color):
            return True

        # TODO: Implement two space forward moves if first move for this pawn.

        return False

    def _validKnightMove(self, startPos, endPos):
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        return ((abs(dx) == 1 and abs(dy) == 2) or
            (abs(dy) == 1 and abs(dx) == 2))

    def _validBishopMove(self, startPos, endPos):
        drow = endPos[0] - startPos[0]
        dcol = endPos[1] - startPos[1]

        if(not self._validBishopMovement(drow, dcol)):
            return False

        rowstep = numpy.sign(drow)
        colstep = numpy.sign(dcol)
        rowstart = startPos[0] + rowstep
        colstart = startPos[1] + colstep
        rowend = endPos[0]
        colend = endPos[1]

        row, col = rowstart, colstart
        while(row != rowend or col != colend):
            if(self._chessBoard[row][col] != None):
                return False
            row += rowstep
            col += colstep

        # No rule violations found. Move is valid.
        return True

    def _validCastleMove(self, startPos, endPos):
        drow = endPos[0] - startPos[0]
        dcol = endPos[1] - startPos[1]

        if(not self._validCastleMovement(drow, dcol)):
            return False

        rowstep = numpy.sign(drow)
        colstep = numpy.sign(dcol)
        rowstart = startPos[0] + rowstep
        colstart = startPos[1] + colstep
        rowend = endPos[0]
        colend = endPos[1]

        row, col = rowstart, colstart
        while(row != rowend or col != colend):
            if(self._chessBoard[row][col] != None):
                return False
            row += rowstep
            col += colstep

        # No rule violations found. Move is valid.
        return True

    def _validQueenMove(self, startPos, endPos):
        drow = endPos[0] - startPos[0]
        dcol = endPos[1] - startPos[1]

        if(not self._validQueenMovement(drow, dcol)):
            return False

        rowstep = numpy.sign(drow)
        colstep = numpy.sign(dcol)
        rowstart = startPos[0] + rowstep
        colstart = startPos[1] + colstep
        rowend = endPos[0]
        colend = endPos[1]

        row, col = rowstart, colstart
        while(row != rowend or col != colend):
            if(self._chessBoard[row][col] != None):
                return False
            row += rowstep
            col += colstep

        # No rule violations found. Move is valid.
        return True

    def _validKingMove(self, startPos, endPos):
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        if(abs(dx) > 1 or abs(dy) > 1):
            return False

        # TODO: Allow the special castling move.

        return True

    def _validCastleMovement(self, dx, dy):
        return dx == 0 or dy == 0

    def _validBishopMovement(self, dx, dy):
        return abs(dx) == abs(dy)

    def _validQueenMovement(self, dx, dy):
        return (self._validBishopMovement(dx, dy) or
            self._validCastleMovement(dx, dy))

class ChessBoard():
    # TODO: Rework these to fit within less than 80 characters per line.
    WHITE_PAWN = ChessPiece(Piece.PAWN, Color.WHITE, pygame.image.load("images/pieces/default-white/pawn.png"))
    WHITE_KNIGHT = ChessPiece(Piece.KNIGHT, Color.WHITE, pygame.image.load("images/pieces/default-white/knight.png"))
    WHITE_BISHOP = ChessPiece(Piece.BISHOP, Color.WHITE, pygame.image.load("images/pieces/default-white/bishop.png"))
    WHITE_CASTLE = ChessPiece(Piece.CASTLE, Color.WHITE, pygame.image.load("images/pieces/default-white/castle.png"))
    WHITE_QUEEN = ChessPiece(Piece.QUEEN, Color.WHITE, pygame.image.load("images/pieces/default-white/queen.png"))
    WHITE_KING = ChessPiece(Piece.KING, Color.WHITE, pygame.image.load("images/pieces/default-white/king.png"))
    BLACK_PAWN = ChessPiece(Piece.PAWN, Color.BLACK, pygame.image.load("images/pieces/default-black/pawn.png"))
    BLACK_KNIGHT = ChessPiece(Piece.KNIGHT, Color.BLACK, pygame.image.load("images/pieces/default-black/knight.png"))
    BLACK_BISHOP = ChessPiece(Piece.BISHOP, Color.BLACK, pygame.image.load("images/pieces/default-black/bishop.png"))
    BLACK_CASTLE = ChessPiece(Piece.CASTLE, Color.BLACK, pygame.image.load("images/pieces/default-black/castle.png"))
    BLACK_QUEEN = ChessPiece(Piece.QUEEN, Color.BLACK, pygame.image.load("images/pieces/default-black/queen.png"))
    BLACK_KING = ChessPiece(Piece.KING, Color.BLACK, pygame.image.load("images/pieces/default-black/king.png"))

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

    _rules = ChessRules(_chessBoard)

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
                    pieceRect = piece.image.get_rect().move(dx, dy)
                    screen.blit(piece.image, pieceRect)
                columnIndex += 1
            rowIndex += 1


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


chessBoard = ChessBoard()

pygame.init()
pygame.display.set_caption("python-chess")
screen = pygame.display.set_mode((440, 440))
board = pygame.image.load("images/boards/black-white.png")
boardRect = board.get_rect()

currentMouseSelect = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # TODO: Don't register clicks that are out of bounds.
            if currentMouseSelect is None:
                currentMouseSelect = pygame.mouse.get_pos()
                print(currentMouseSelect)
            else:
                newMouseSelect = pygame.mouse.get_pos()
                startBoardIndex = pygameToBoardIndex(currentMouseSelect)
                endBoardIndex = pygameToBoardIndex(newMouseSelect)
                print(startBoardIndex, endBoardIndex)
                if(chessBoard.validMove(startBoardIndex, endBoardIndex)):
                    chessBoard.movePiece(startBoardIndex, endBoardIndex)
                currentMouseSelect = None

        screen.blit(board, boardRect)
        chessBoard.pygameBlit(screen)
        pygame.display.flip()

# TODO: Allow selection between command line and GUI chess modes.
# while(True):
#     print(chessBoard)
#     move = input("move: ")
#     if(move == "exit" or move == "quit" or move == "q"):
#       exit()
#     moveIndex = inputToIndex(move)
#     if(moveIndex is not None):
#         chessBoard.movePiece(moveIndex[0], moveIndex[1])
#     else:
#         print("Invalid input")