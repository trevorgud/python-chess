#!/usr/bin/env python3

from enum import Enum
import math
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