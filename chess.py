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


class ChessState():
    def __init__(self, chessBoard):
        self.chessBoard = chessBoard
        self.turn = Color.WHITE
        self.kingMoved = {Color.WHITE: False, Color.BLACK: False}
        self.castle1Moved = {Color.WHITE: False, Color.BLACK: False}
        self.castle2Moved = {Color.WHITE: False, Color.BLACK: False}


class ChessRules():
    def __init__(self, chessBoard, pieces):
        self._boardWidth = 8
        self._boardHeight = 8
        self._state = ChessState(chessBoard)
        self._pieces = pieces

    def _switchTurn(self):
        if(self._state.turn == Color.WHITE):
            self._state.turn = Color.BLACK
        else:
            self._state.turn = Color.WHITE

    def _setPiecesMoved(self, piece, startPos):
        if(piece.pieceType == Piece.KING):
            self._state.kingMoved[piece.color] = True
        elif(piece.pieceType == Piece.CASTLE):
            if(startPos == (7, 0)):
                self._state.castle1Moved[piece.color] = True
            elif(startPos == (7, 7)):
                self._state.castle2Moved[piece.color] = True

    def _kingPos(self, color):
        for row in range(self._boardHeight):
            for col in range(self._boardWidth):
                piece = self._state.chessBoard[row][col]
                if(piece != None and
                    piece.pieceType == Piece.KING and
                    piece.color == color):
                    return (row, col)

    def _promotePawnColored(self, color, row):
        for col in range(self._boardWidth):
            piece = self._state.chessBoard[row][col]
            if(piece != None and
                piece.color == color and
                piece.pieceType == Piece.PAWN):
                if(color == Color.WHITE):
                    self._state.chessBoard[row][col] = self._pieces.WHITE_QUEEN
                else:
                    self._state.chessBoard[row][col] = self._pieces.BLACK_QUEEN

    def _promotePawnIfEighthRank(self):
        whiteUpgradeRow = 0
        blackUpgradeRow = self._boardHeight - 1
        self._promotePawnColored(Color.WHITE, whiteUpgradeRow)
        self._promotePawnColored(Color.BLACK, blackUpgradeRow)

    def _moveCastledPieces(self, row, direction):
        if(direction < 0):
            startCol, endCol = 0, 3
        else:
            startCol, endCol = 7, 5
        piece = self._state.chessBoard[row][startCol]
        self._state.chessBoard[row][startCol] = None
        self._state.chessBoard[row][endCol] = piece

    def movePiece(self, startPos, endPos):
        isCastling = self._validKingCastleMove(startPos, endPos)
        piece = self._state.chessBoard[startPos[0]][startPos[1]]
        if(self._isCheckAfterMove(piece.color, startPos, endPos)):
            return
        self._state.chessBoard[startPos[0]][startPos[1]] = None
        self._state.chessBoard[endPos[0]][endPos[1]] = piece
        self._setPiecesMoved(piece, startPos)
        self._promotePawnIfEighthRank()
        if(isCastling):
            direction = numpy.sign(endPos[1] - startPos[1])
            row = startPos[0]
            self._moveCastledPieces(row, direction)
        self._switchTurn()

    def _basicValidMove(self, startPos, endPos):
        if(startPos[0] >= self._boardHeight or startPos[0] < 0 or
            startPos[1] >= self._boardWidth or startPos[1] < 0 or
            endPos[0] >= self._boardHeight or endPos[0] < 0 or
            endPos[1] >= self._boardWidth or endPos[1] < 0):
            return False
        startPiece = self._state.chessBoard[startPos[0]][startPos[1]]
        endPiece = self._state.chessBoard[endPos[0]][endPos[1]]
        if(startPos == endPos or
            startPiece == None or
            startPiece.color != self._state.turn or
            (endPiece != None and startPiece.color == endPiece.color)):
            return False

        return True

    def validMove(self, startPos, endPos):
        return (self._validMovement(startPos, endPos) or
            self._validKingCastleMove(startPos, endPos))

    def _validMovement(self, startPos, endPos):
        if(not self._basicValidMove(startPos, endPos)):
            return False

        startPiece = self._state.chessBoard[startPos[0]][startPos[1]]
        endPiece = self._state.chessBoard[endPos[0]][endPos[1]]

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

    def _isCheckAfterMove(self, color, startPos, endPos):
        # Try moving the pieces to see if will be in check.
        tempBoard = self._boardCopy()
        endPiece = self._state.chessBoard[endPos[0]][endPos[1]]
        startPiece = self._state.chessBoard[startPos[0]][startPos[1]]
        self._state.chessBoard[endPos[0]][endPos[1]] = startPiece
        self._state.chessBoard[startPos[0]][startPos[1]] = None

        isCheckAfterMove = self.isCheck(color)

        # Restore the original state.
        self._loadBoard(tempBoard)

        return isCheckAfterMove

    def _validPawnMove(self, startPos, endPos):
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        endPiece = self._state.chessBoard[endPos[0]][endPos[1]]
        startPiece = self._state.chessBoard[startPos[0]][startPos[1]]
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
        elif(dx == 2 and dy == 0 and
            ((startPiece.color == Color.WHITE and startPos[0] == 6) or
                (startPiece.color == Color.BLACK and startPos[0] == 1))):
            return True

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
            if(self._state.chessBoard[row][col] != None):
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
            if(self._state.chessBoard[row][col] != None):
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
            if(self._state.chessBoard[row][col] != None):
                return False
            row += rowstep
            col += colstep

        # No rule violations found. Move is valid.
        return True

    def _validKingMove(self, startPos, endPos):
        startPiece = self._state.chessBoard[startPos[0]][startPos[1]]
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        if(abs(dx) > 1 or abs(dy) > 1):
            return False

        return True

    def _validKingCastleMove(self, startPos, endPos):
        if(not self._basicValidMove(startPos, endPos)):
            return False
        startPiece = self._state.chessBoard[startPos[0]][startPos[1]]
        color = startPiece.color
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        kingMoved = self._state.kingMoved[color]
        castle1Moved = self._state.castle1Moved[color]
        castle2Moved = self._state.castle2Moved[color]
        castleMoved = castle1Moved if dy < 0 else castle2Moved

        if(startPiece.pieceType != Piece.KING or
            kingMoved or castleMoved or
            abs(dy) != 2 or dx != 0):
            return False

        # Check mid pieces. Any piece between castle and king is invalid.
        row = startPos[0]
        midColIndexes = range(5, 6) if dy > 0 else range(1, 3)
        for col in midColIndexes:
            if(self._state.chessBoard[row][col] != None):
                return False

        # Determine if the king will be in check at any point through the move.
        direction = numpy.sign(dy)
        midPos = (startPos[0], startPos[1] + direction)
        if(self.isCheck(color) or
            self._isCheckAfterMove(color, startPos, midPos) or
            self._isCheckAfterMove(color, startPos, endPos)):
            return False

        return True

    def _validCastleMovement(self, dx, dy):
        return dx == 0 or dy == 0

    def _validBishopMovement(self, dx, dy):
        return abs(dx) == abs(dy)

    def _validQueenMovement(self, dx, dy):
        return (self._validBishopMovement(dx, dy) or
            self._validCastleMovement(dx, dy))

    def isCheck(self, color):
        kingPos = self._kingPos(color)
        isCheck = False
        tempTurn = self._state.turn
        if(self._state.turn == color):
            self._switchTurn()

        for row in range(self._boardHeight):
            for col in range(self._boardWidth):
                if(self.validMove((row, col), kingPos)):
                    isCheck = True

        self._state.turn = tempTurn
        return isCheck

    def isCheckmate(self, color):
        # TODO: Detect checkmate conditions.
        return False

    def _boardCopy(self):
        newBoard = []
        for row in self._state.chessBoard:
            newRow = []
            for col in row:
                newRow.append(col)
            newBoard.append(newRow)
        return newBoard

    def _loadBoard(self, board):
        for row in range(self._boardHeight):
            for col in range(self._boardWidth):
                self._state.chessBoard[row][col] = board[row][col]


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
        _pieces.WHITE_PAWN: pygame.image.load(_whiteDir + "/pawn.png"),
        _pieces.WHITE_KNIGHT: pygame.image.load(_whiteDir + "/knight.png"),
        _pieces.WHITE_BISHOP: pygame.image.load(_whiteDir + "/bishop.png"),
        _pieces.WHITE_CASTLE: pygame.image.load(_whiteDir + "/castle.png"),
        _pieces.WHITE_QUEEN: pygame.image.load(_whiteDir + "/queen.png"),
        _pieces.WHITE_KING: pygame.image.load(_whiteDir + "/king.png"),
        _pieces.BLACK_PAWN: pygame.image.load(_blackDir + "/pawn.png"),
        _pieces.BLACK_KNIGHT: pygame.image.load(_blackDir + "/knight.png"),
        _pieces.BLACK_BISHOP: pygame.image.load(_blackDir + "/bishop.png"),
        _pieces.BLACK_CASTLE: pygame.image.load(_blackDir + "/castle.png"),
        _pieces.BLACK_QUEEN: pygame.image.load(_blackDir + "/queen.png"),
        _pieces.BLACK_KING: pygame.image.load(_blackDir + "/king.png")
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