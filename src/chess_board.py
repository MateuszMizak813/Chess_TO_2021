import pygame
import constants as con
from chess_piece import *

"""
Klasa Szachownicy, odpowiedzialna za przechowywanie pionków, wszystkie aspekty graficzne, oraz funkcjonalność pomiędzy pionkami.
"""
class ChessBoard():
    def __init__(self, screen, light_color = 'white', dark_color = 'gray') -> None:
        self.__screen = screen
        self.__colors = [light_color, dark_color]
        self.__pieces_list = self.generatePieceList()
        self.__selected_piece = False
        self.drawBoard()
        self.drawAllPieces()


    """
    Generuje poczatkowa liste pionków na szachownicy
    """
    def generatePieceList(self):
        list_of_pieces = [
            [Rook(self.__screen, 0,0,'b'), Knight(self.__screen, 0,1, 'b'), Bishop(self.__screen, 0,2, 'b'), Queen(self.__screen, 0,3, 'b'),
            King(self.__screen, 0,4, 'b'), Bishop(self.__screen, 0,5, 'b'), Knight(self.__screen, 0,6, 'b'), Rook(self.__screen,0,7,'b')],
            [Pawn(self.__screen, 1,x, 'b') for x in range(8)],
            ['x' for x in range(8)],
            ['x' for x in range(8)],
            ['x' for x in range(8)],
            ['x' for x in range(8)],
            [Pawn(self.__screen, 6,x, 'w') for x in range(8)],
            [Rook(self.__screen,7,0,'w'), Knight(self.__screen, 7,1, 'w'), Bishop(self.__screen, 7,2, 'w'), Queen(self.__screen, 7,3, 'w'),
            King(self.__screen, 7,4, 'w'), Bishop(self.__screen, 7,5, 'w'), Knight(self.__screen, 7,6, 'w'), Rook(self.__screen,7,7,'w')]
        ]
        return list_of_pieces


    """
    Rysuje szachownice, służy do restartu obrazu po zmianie pozycji pionków
    """
    def drawBoard(self):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.__screen, self.__colors[(i+j)%2], pygame.Rect(i*con.field_size, j*con.field_size, con.field_size, con.field_size))


    """
    U każdego pionka z listy self.__pieces_list wywołuje funkcje rusującą na ekranie.
    """
    def drawAllPieces(self):
        for row in self.__pieces_list:
            for piece in row:
                if piece != 'x' and piece.isAlive():
                    piece.drawSelf()



    """
    Funkcja lewego przycisku myszy na szachownicy wywoływana w mainlooop
    """
    def leftClickOnChessBoard(self, row, column):
        clicked_field = self.__pieces_list[row][column]

        if self.__selected_piece == False and clicked_field != 'x':
            avaible = clicked_field.showAvaibleMoves()
            self.drawBoard()
            for pos in avaible:
                pygame.draw.rect(self.__screen, (150,150,0), pygame.Rect(pos[1]*con.field_size, pos[0]*con.field_size, con.field_size, con.field_size))
            self.drawAllPieces()

            self.__selected_piece = clicked_field

        elif self.__selected_piece == clicked_field:
            self.__selected_piece = False
            self.drawBoard()
            self.drawAllPieces()

        elif self.__selected_piece != False:
            print("Chcesz ruszyć na ",row+1,column+1)

