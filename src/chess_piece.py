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
        self.__piece_type = piece_type
        self.__color = color
        self.__has_moved = 0


    def drawSelf(self):
        self.__screen.blit(self.__piece_type.getImage(self.__color), pygame.Rect(self.__column*con.field_size, self.__row*con.field_size, con.field_size, con.field_size))

    def getField(self):
        return self.__row, self.__column

    def move(self, new_positions):
        self.__row = new_positions[0]
        self.__column = new_positions[1]
        self.__has_moved += 1

    def setAlive(self, status):
        self.__alive = status

    def getName(self):
        return self.__piece_type.__name__

    def getColor(self):
        return self.__color

    def getAvaibleMoves(self, board):
        return self.__piece_type.avaibleMoves(self, board)

    def isAlive(self):
        return self.__alive

    def undoMove(self, last_positions):
        self.__row = last_positions[0]
        self.__column = last_positions[1]
        self.__has_moved -= 1


    def didMove(self):
        return self.__has_moved != 0 




class PieceType():
    def getImage(color):
        return None

class Pawn(PieceType):
    def getImage(color):
        return pygame.transform.scale(pygame.image.load("./img/"+color+"_pwn.png"), (con.field_size, con.field_size))
    def avaibleMoves(piece:ChessPiece, board):
        list_of_moves = []
        s_row, s_col = piece.getField()
        clr = piece.getColor()
        if clr == "b":
            mod = 1
        else:
            mod = -1
        if piece.didMove():
            if 8 > s_row + mod > -1 and board[s_row + mod][s_col] == "x":
                list_of_moves.append(SavedMove((s_row, s_col), (s_row + mod, s_col), piece, board[s_row + mod][s_col]))
        else:
            for i in [1,2]:
                if -1 < s_row + mod*i < 8 and board[s_row + mod*i][s_col] == "x":
                    list_of_moves.append(SavedMove((s_row, s_col), (s_row + mod*i, s_col), piece, board[s_row + mod*i][s_col]))
        for i in [-1,1]:
            if -1 < s_col +i < 8 and -1 < s_row + mod < 8:
                if board[s_row + mod][s_col + i] != "x" and board[s_row + mod][s_col + i].getColor() != piece.getColor():
                    list_of_moves.append(SavedMove((s_row, s_col), (s_row + mod, s_col + i), piece, board[s_row + mod][s_col + i]))
        return list_of_moves
            
class Bishop(PieceType):
    def getImage(color):
        return pygame.transform.scale(pygame.image.load("./img/"+color+"_bsp.png"), (con.field_size, con.field_size))
    def avaibleMoves(piece, board):
        list_of_moves =[]
        s_row, s_col = piece.getField()

        for mod in [(1,1,8,8),(-1,-1,-1,-1),(1,-1,8,-1),(-1,1,-1,8)]:
            tmp_row = s_row + mod[0]
            tmp_col = s_col + mod[1]
            while(-1 != tmp_row != 8 and -1 != tmp_col != 8):
                if board[tmp_row][tmp_col] =="x":
                    list_of_moves.append(SavedMove((s_row,s_col),(tmp_row, tmp_col),piece, board[tmp_row][tmp_col]))
                    tmp_col += mod[1]
                    tmp_row += mod[0]
                elif board[tmp_row][tmp_col].getColor() != piece.getColor():
                    list_of_moves.append(SavedMove((s_row,s_col),(tmp_row, tmp_col),piece, board[tmp_row][tmp_col]))
                    break
                else:
                    break
        return list_of_moves


class Knight(PieceType):
    def getImage(color):
        return pygame.transform.scale(pygame.image.load("./img/"+color+"_knt.png"), (con.field_size, con.field_size))
    def avaibleMoves(piece, board):
        list_of_moves = []
        s_row, s_col = piece.getField()
        for r,c in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            if 0 <= s_row + r < 8 and 0 <= s_col + c < 8:
                if board[s_row + r][s_col + c] == "x" or board[s_row + r][s_col +c].getColor() != piece.getColor():
                    list_of_moves.append(SavedMove((s_row,s_col),(s_row + r, s_col + c), piece, board[s_row + r][s_col + c]))
        return list_of_moves

class Rook(PieceType):
    def getImage(color):
        return pygame.transform.scale(pygame.image.load("./img/"+color+"_rok.png"), (con.field_size, con.field_size))
    def avaibleMoves(piece, board):
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
    def getImage(color):
        return pygame.transform.scale(pygame.image.load("./img/"+color+"_qnn.png"), (con.field_size, con.field_size))
    def avaibleMoves(piece, board):
        list_of_moves = Bishop.avaibleMoves(piece,board) + Rook.avaibleMoves(piece,board)
        return list_of_moves

class King(PieceType):
    def getImage(color):
        return pygame.transform.scale(pygame.image.load("./img/"+color+"_kng.png"), (con.field_size, con.field_size))
    def avaibleMoves(piece, board):
        list_of_moves = []
        s_row, s_col = piece.getField()
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r == c == 0:
                    continue
                if 0 <= s_row + r < 8 and 0 <= s_col +c < 8 and (board[s_row+ r][s_col+ c] == "x" or board[s_row+ r][s_col+ c].getColor() != piece.getColor()):
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


