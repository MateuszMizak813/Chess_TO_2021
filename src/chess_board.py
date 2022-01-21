import pygame
import constants as con
from chess_piece import *
from game_state import GameHistory
import time

"""
Klasa Szachownicy, odpowiedzialna za przechowywanie pionków, wszystkie aspekty graficzne, oraz funkcjonalność pomiędzy pionkami.
"""
class ChessBoard():
    def __init__(self, screen, light_color = 'white', dark_color = 'brown') -> None:
        self.__screen = screen
        self.__colors = [light_color, dark_color]
        self.__pieces_list = self.generatePieceList()
        self.__selected_piece = False
        self.__game_history = GameHistory()
        self.__player_turn = "w"
        self.drawBoard()


    """
    Generuje poczatkowa liste pionków na szachownicy
    """
    def generatePieceList(self):
        list_of_pieces = [
            [ChessPiece(self.__screen, 0,0,'b', Rook), ChessPiece(self.__screen, 0,1, 'b', Knight), ChessPiece(self.__screen, 0,2, 'b', Bishop), ChessPiece(self.__screen, 0,3, 'b', Queen),
            ChessPiece(self.__screen, 0,4, 'b', King), ChessPiece(self.__screen, 0,5, 'b', Bishop), ChessPiece(self.__screen, 0,6, 'b', Knight), ChessPiece(self.__screen, 0,7, 'b', Rook)],
            [ChessPiece(self.__screen, 1,x,'b', Pawn) for x in range(8)],
            ['x' for x in range(8)],
            ['x' for x in range(8)],
            ['x' for x in range(8)],
            ['x' for x in range(8)],
            [ChessPiece(self.__screen, 6,x,'w', Pawn) for x in range(8)],
            [ChessPiece(self.__screen, 7,0,'w', Rook), ChessPiece(self.__screen, 7,1, 'w', Knight), ChessPiece(self.__screen, 7,2, 'w', Bishop), ChessPiece(self.__screen, 7,3, 'w', Queen),
            ChessPiece(self.__screen, 7,4, 'w', King), ChessPiece(self.__screen, 7,5, 'w', Bishop), ChessPiece(self.__screen, 7,6, 'w', Knight), ChessPiece(self.__screen, 7,7, 'w', Rook)]
        ]
        return list_of_pieces


    """
    Rysuje szachownice, służy do restartu obrazu po zmianie pozycji pionków
    """
    def drawBoard(self):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.__screen, self.__colors[(i+j)%2], pygame.Rect(i*con.field_size, j*con.field_size, con.field_size, con.field_size))
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
            if clicked_field.getColor() == self.__player_turn:
                self.__selected_piece = clicked_field
                print("Zaznaczyłeś "+clicked_field.getName())

        elif self.__selected_piece == clicked_field:
            self.__selected_piece = False
            self.drawBoard()
            

        elif self.__selected_piece != False:
            print("Chcesz ruszyć z",self.__selected_piece.getField(),"na ", (row,column))
            #przypisanie potrzebnych zmiennych
            start_position = self.__selected_piece.getField()
            captured_piece = self.__pieces_list[row][column]

            #Save planned Move and check if possible
            move = SavedMove(start_position,(row,column), self.__selected_piece, captured_piece)
            list_of_moves = self.__selected_piece.getAvaibleMoves(self.__pieces_list)
            print(list_of_moves)
            if move in list_of_moves:
                #Zamiana pozycji
                self.__pieces_list[start_position[0]][start_position[1]] = "x"
                self.__pieces_list[row][column] = self.__selected_piece
                self.__selected_piece.move((row,column))
                
                #Odświeżenie obrazu
                self.drawBoard()

                #Zapisanie ruchu w historii
                self.__game_history.addMove(move)

                #"Zbicie" pionka jesli pole bylo zajmowane i odznaczenie pionka
                self.__selected_piece = False
                if captured_piece != "x":
                    captured_piece.setAlive(False)

                if self.__player_turn == "w":
                    self.__player_turn = "b"
                else:
                    self.__player_turn = "w"
            else:
                print("Niedozwolony ruch")


    def undo(self):
        move = self.__game_history.undoMove()
        start = move.getStart()
        end = move.getEnd()
        captured = move.getCaptured()
        moved = move.getMoved()
        self.__pieces_list[start[0]][start[1]] = moved
        self.__pieces_list[end[0]][end[1]] = captured
        moved.move(start)
        moved.undoIfMoved()
        if captured != "x":
            captured.setAlive(True)
        self.drawBoard()



