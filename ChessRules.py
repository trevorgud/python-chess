from ChessState import ChessState
from Color import Color
from Piece import Piece

class ChessRules():
    def __init__(self, chessBoard, pieces):
        self._boardWidth = 8
        self._boardHeight = 8
        self._state = ChessState(chessBoard)
        self._pieces = pieces

    def _getPiece(self, pos):
        return self._state.chessBoard[pos[0]][pos[1]]

    def _setPiece(self, pos, piece):
        self._state.chessBoard[pos[0]][pos[1]] = piece

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
                piece = self._getPiece((row, col))
                if(piece != None and
                    piece.pieceType == Piece.KING and
                    piece.color == color):
                    return (row, col)

    def _promotePawnColored(self, color, row):
        for col in range(self._boardWidth):
            piece = self._getPiece((row, col))
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
        piece = self._getPiece((row, startCol))
        self._setPiece((row, startCol), None)
        self._setPiece((row, endCol), piece)

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
        endPiece = self._getPiece(endPos)
        startPiece = self._getPiece(startPos)
        self._setPiece(endPos, startPiece)
        self._setPiece(startPos, None)

        isCheckAfterMove = self.isCheck(color)

        # Restore the original state.
        self._loadBoard(tempBoard)

        return isCheckAfterMove

    def _validPawnMove(self, startPos, endPos):
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        endPiece = self._getPiece(endPos)
        startPiece = self._getPiece(startPos)
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
            if(self._getPiece((row, col)) != None):
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
            if(self._getPiece((row, pos)) != None):
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
            if(self._getPiece((row, col)) != None):
                return False
            row += rowstep
            col += colstep

        # No rule violations found. Move is valid.
        return True

    def _validKingMove(self, startPos, endPos):
        startPiece = self._getPiece(startPos)
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        if(abs(dx) > 1 or abs(dy) > 1):
            return False

        return True

    def _validKingCastleMove(self, startPos, endPos):
        if(not self._basicValidMove(startPos, endPos)):
            return False
        startPiece = self._getPiece(startPos)
        color = startPiece.color
        dx = endPos[0] - startPos[0]
        dy = endPos[1] - startPos[1]
        kingMoved = self._state.kingMoved[color]
        castleMoved = (self._state.castle1Moved[color] if dy < 0
            else self._state.castle2Moved[color])

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
                self._setPiece((row, col), board[row][col])
