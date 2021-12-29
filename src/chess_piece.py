import pygame
import constants as con

"""
Klasa po której dziedziczą wszystkie konkretne rodzaję pionków
"""
class ChessPiece():
    """
    Konstruktor ze wszystkimi potrzebnymi zmiennymi do definiowania poszczególnych pionków
    """
    def __init__(self, screen, row, column, color, alive = True) -> None:
        self._screen = screen
        self._row = row
        self._column = column
        self._alive = alive
        self._color = color
        self._image = None
        self._name = "piece"
        self._has_moved = False

    """
    Funkcja wspólna dla wszystkich pionków, opowiedzialna za wyświetlanie swojego obrazka
    """
    def drawSelf(self):
        self._screen.blit(self._image, pygame.Rect(self._column*con.field_size, self._row*con.field_size, con.field_size, con.field_size))


    """
    Sprawdzanie czy pionek żyje
    """
    def isAlive(self):
        return self._alive


    ###################
    def moveToField(self, destination):
        pass

    #####################
    def showAvaibleMoves(self):
        pass

    """
    Zwraca nazwe pionka
    """
    def returnName(self):
        return self._name


class Pawn(ChessPiece):
    def __init__(self, screen, row, column, color, alive=True) -> None:
        super().__init__(screen, row, column, color, alive=alive)
        self._image = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_pwn.png"), (con.field_size, con.field_size))
        self._name = "Pawn"
    def showAvaibleMoves(self):
        avaible_moves = []
        print("my color is",self._color)
        if self._color == 'b':
            print("dupa")
            mod = 1
        else:
            mod = -1
        print(mod)
        if self._has_moved == False:
            for i in [1,2]:
                if 7 >= self._row + i*mod >= 0:
                    avaible_moves.append((self._row + i*mod, self._column))
        else:
            if 7 >= self._row + mod >= 0:
                    avaible_moves.append((self._row + mod, self._column))

        
        return avaible_moves
        



class Bishop(ChessPiece):
    def __init__(self, screen, row, column, color, alive=True) -> None:
        super().__init__(screen, row, column, color, alive=alive)
        self._image = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_bsp.png"), (con.field_size, con.field_size))
        self._name = "Bishop"

class Knight(ChessPiece):
    def __init__(self, screen, row, column, color, alive=True) -> None:
        super().__init__(screen, row, column, color, alive=alive)
        self._image = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_knt.png"), (con.field_size, con.field_size))
        self._name = "Knight"

class Rook(ChessPiece):
    def __init__(self, screen, row, column, color, alive=True) -> None:
        super().__init__(screen, row, column, color, alive=alive)
        self._image = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_rok.png"), (con.field_size, con.field_size))
        self._name = "Rook"

class Queen(ChessPiece):
    def __init__(self, screen, row, column, color, alive=True) -> None:
        super().__init__(screen, row, column, color, alive=alive)
        self._image = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_qnn.png"), (con.field_size, con.field_size))
        self._name = "Queen"

class King(ChessPiece):
    def __init__(self, screen, row, column, color, alive=True) -> None:
        super().__init__(screen, row, column, color, alive=alive)
        self._image = pygame.transform.scale(pygame.image.load("./img/"+self._color+"_kng.png"), (con.field_size, con.field_size))
        self._name = "King"