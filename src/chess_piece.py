from distutils.sysconfig import customize_compiler
from turtle import color
import pygame
import constants as con

"""
Klasa reprezentująca pionka
"""
class ChessPiece():
    """
    Konstruktor ze wszystkimi potrzebnymi zmiennymi do definiowania poszczególnych pionków
    """
    def __init__(self, screen, row, column, color, piece_type):
        self.__screen = screen
        self.__row = row
        self.__column = column
        self.__alive = True
        self.__piece_type = piece_type(color)
        self.__has_moved = False
        self.__moved_recently = False


    def drawSelf(self):
        self.__screen.blit(self.__piece_type.getImage(), pygame.Rect(self.__column*con.field_size, self.__row*con.field_size, con.field_size, con.field_size))

    def getField(self):
        return self.__row, self.__column

    def move(self, new_positions):
        self.__row = new_positions[0]
        self.__column = new_positions[1]
        if self.__has_moved == False and self.__moved_recently == False:
            self.__moved_recently = True
        elif self.__has_moved == False and self.__moved_recently == True:
            self.__has_moved = True

    def setAlive(self, status):
        self.__alive = status

    def getName(self):
        return self.__piece_type.getName()

    def getColor(self):
        return self.__piece_type.getColor()

    def getAvaibleMoves(self, board):
        return self.__piece_type.avaibleMoves(self, board)

    def isAlive(self):
        return self.__alive

    def undoIfMoved(self):
        if self.__has_moved == False and self.__moved_recently == True:
            self.__moved_recently == False

    def didMove(self):
        return self.__moved_recently or self.__has_moved



class PieceType():
    def __init__(self,color):
        self._color = color
        self._img = None
    def getName(self):
        return type(self).__name__
    def getColor(self):
        return self._color
    def getImage(self):
        return self._img

class Pawn(PieceType):
    def __init__(self, color):
        super().__init__(color)
        self._img = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_pwn.png"), (con.field_size, con.field_size))
    def avaibleMoves(self, piece, board):
       pass
        
    
class Bishop(PieceType):
    def __init__(self, color):
        super().__init__(color)
        self._img = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_bsp.png"), (con.field_size, con.field_size))
    def avaibleMoves(self, piece, board):
       pass

class Knight(PieceType):
    def __init__(self, color):
        super().__init__(color)
        self._img = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_knt.png"), (con.field_size, con.field_size))
    def avaibleMoves(self, piece, board):
        list_of_moves = []
        s_row, s_col = piece.getField()
        for r,c in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            if 0 <= s_row + r < 8 and 0 <= s_col + c < 8:
                if board[s_row + r][s_col + c] == "x" or board[s_row + r][s_col +c].getColor() != piece.getColor():
                    list_of_moves.append(SavedMove((s_row,s_col),(s_row + r, s_col + c), piece, board[s_row + r][s_col + c]))
        return list_of_moves

class Rook(PieceType):
    def __init__(self, color):
        super().__init__(color)
        self._img = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_rok.png"), (con.field_size, con.field_size))
    def avaibleMoves(self, piece, board):
        list_of_moves = []
        s_row, s_col = piece.getField()
        for row in range(s_row + 1, 8):
            if board[row][s_col] == "x":
                list_of_moves.append(SavedMove((s_row,s_col),(row, s_col),piece, board[row][s_col]))
            elif board[row][s_col].getColor() != piece.getColor():
                list_of_moves.append(SavedMove((s_row,s_col),(row, s_col),piece, board[row][s_col]))
                break
            else:
                break
        for col in range(s_col +1, 8):
            if board[s_row][col] == "x":
                list_of_moves.append(SavedMove((s_row,s_col),(s_row, col),piece, board[s_row][col]))
            elif board[s_row][col].getColor() != piece.getColor():
                list_of_moves.append(SavedMove((s_row,s_col),(s_row, col),piece, board[s_row][col]))
                break
            else:
                break
        for row in range(s_row - 1, -1, -1):
            if board[row][s_col] == "x":
                list_of_moves.append(SavedMove((s_row,s_col),(row, s_col),piece, board[row][s_col]))
            elif board[row][s_col].getColor() != piece.getColor():
                list_of_moves.append(SavedMove((s_row,s_col),(row, s_col),piece, board[row][s_col]))
                break
            else:
                break
        for col in range(s_col -1, -1, -1):
            if board[s_row][col] == "x":
                list_of_moves.append(SavedMove((s_row,s_col),(s_row, col),piece, board[s_row][col]))
            elif board[s_row][col].getColor() != piece.getColor():
                list_of_moves.append(SavedMove((s_row,s_col),(s_row, col),piece, board[s_row][col]))
                break
            else:
                break
        return list_of_moves
            


class Queen(PieceType):
    def __init__(self, color):
        super().__init__(color)
        self._img = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_qnn.png"), (con.field_size, con.field_size))
    def avaibleMoves(self, piece, board):
       pass

class King(PieceType):
    def __init__(self, color):
        super().__init__(color)
        self._img = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_kng.png"), (con.field_size, con.field_size))
    def avaibleMoves(self, piece, board):
        list_of_moves = []
        s_row, s_col = piece.getField()
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r == c == 0:
                    continue
                elif 0 <= s_row + r < 8 and 0 <= s_col +c < 8 and board[s_row][s_col].getColor() != piece.getColor():
                    list_of_moves.append(SavedMove((s_row,s_col),(s_row +r,s_col + c),piece, board[s_row + r][s_col + c]))
        return list_of_moves




class SavedMove():
    def __init__(self, start_position, end_position, moved_piece, captured_piece):
        self.__start_position = start_position
        self.__end_position = end_position
        self.__moved_piece = moved_piece
        self.__captured_piece = captured_piece
    def getStart(self):
        return self.__start_position
    def getEnd(self):
        return self.__end_position
    def getCaptured(self):
        return self.__captured_piece
    def getMoved(self):
        return self.__moved_piece
    def __eq__(self,other):
        if isinstance(other, SavedMove):
            return self.__start_position == other.getStart() and self.__end_position == other.getEnd()


