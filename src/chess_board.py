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
        self.__game_ended = False
        self.__avaible_moves = []
        self.drawBoard()
        self.drawPieces()


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
        
    def drawPieces(self):
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
                self.__avaible_moves = self.__selected_piece.getAvaibleMoves(self.__pieces_list)
                self.drawBoard()
                for move in self.__avaible_moves:
                    end = move.getEnd()
                    pygame.draw.circle(self.__screen, "green", (end[1]*con.field_size + con.field_size/2, end[0]*con.field_size + con.field_size/2), 0.4*con.field_size)
                self.drawPieces()

        elif self.__selected_piece == clicked_field:
            self.__selected_piece = False
            self.__avaible_moves.clear()
            self.drawBoard()
            self.drawPieces()
            

        elif self.__selected_piece != False:
            #przypisanie potrzebnych zmiennych
            start_position = self.__selected_piece.getField()
            captured_piece = self.__pieces_list[row][column]

            #Save planned Move and check if possible
            move = SavedMove(start_position,(row,column), self.__selected_piece, captured_piece)
            if move in self.__avaible_moves:
                #Zamiana pozycji
                self.__pieces_list[start_position[0]][start_position[1]] = "x"
                self.__pieces_list[row][column] = self.__selected_piece
                self.__selected_piece.move((row,column))
                
                #Zapisanie ruchu w historii
                self.__game_history.addMove(move)

                #"Zbicie" pionka jesli pole bylo zajmowane i odznaczenie pionka
                if captured_piece != "x":
                    captured_piece.setAlive(False)

                if self.__player_turn == "w":
                    check, king = self.checkForChecks("b")
                else:
                    check, king = self.checkForChecks("w")

                if self.__player_turn == "w":
                    self.__player_turn = "b"
                else:
                    self.__player_turn = "w"

                if check:
                    self.undo(True)
                    print("Niedozwolony ruch - zagrożony król")
                    self.__selected_piece = False
                    self.__avaible_moves.clear()
                    self.drawBoard()
                    pos = king.getField()
                    pygame.draw.circle(self.__screen, "red", (pos[1]*con.field_size + con.field_size/2, pos[0]*con.field_size + con.field_size/2), 0.4*con.field_size)
                    self.drawPieces()

                else:
                    self.__selected_piece = False
                    #Odświeżenie obrazu
                    self.drawBoard()
                    if self.__player_turn == "w":
                        check,king = self.checkForChecks("b")
                    else:
                        check,king = self.checkForChecks("w")
                    avaible = self.checkForAvaibleMoves(self.__player_turn)
                    if check:
                        self.drawBoard()
                        pos = king.getField()
                        pygame.draw.circle(self.__screen, "red", (pos[1]*con.field_size + con.field_size/2, pos[0]*con.field_size + con.field_size/2), 0.4*con.field_size)
                        self.drawPieces()
                        if avaible == False:
                            print(self.__player_turn,"Lost")
                    else:
                        self.drawBoard()
                        self.drawPieces()
                        if avaible == False:
                            print("Draw")
            else:
                print("Niedozwolony ruch")
                self.__avaible_moves.clear()
                self.__selected_piece = False
        self.__game_history.clearForward()


    def undo(self, ifcheck = False):
        move = self.__game_history.undoMove(ifcheck)
        if move != None:
            start = move.getStart()
            end = move.getEnd()
            captured = move.getCaptured()
            moved = move.getMoved()
            self.__pieces_list[start[0]][start[1]] = moved
            self.__pieces_list[end[0]][end[1]] = captured

            moved.undoMove(start)

            if captured != "x":
                captured.setAlive(True)
            self.drawBoard()
            self.drawPieces()

            #Zamiana Tury
            if self.__player_turn == "w":
                self.__player_turn = "b"
            else:
                self.__player_turn = "w"

    def forward(self):
        move = self.__game_history.forwardMove()
        if move != None:
            start = move.getStart()
            end = move.getEnd()
            captured = move.getCaptured()
            moved = move.getMoved()
            self.__pieces_list[end[0]][end[1]] = moved

            moved.move(end)

            if captured != "x":
                captured.setAlive(False)
            self.drawBoard()
            self.drawPieces()

            #Zamiana Tury
            if self.__player_turn == "w":
                self.__player_turn = "b"
            else:
                self.__player_turn = "w"

    def checkForChecks(self, color): #color = color of pieces that can check
        avaible_moves = []
        enemy_king = None
        check = False
        for row in self.__pieces_list:
            for piece in row:
                if piece != "x" and piece.getColor() != color and piece.getName() == "King":
                    enemy_king = piece
                elif piece != "x" and piece.getColor() == color:
                    moves = piece.getAvaibleMoves(self.__pieces_list)
                    for move in moves:
                        avaible_moves.append(move)
                        if move.getCaptured() != "x" and move.getCaptured().getName() == "King":
                            check = True
        if check == False:
            return check, enemy_king
        if check == True:
            return check, enemy_king

    def checkForAvaibleMoves(self, color):
        avaible_moves = []
        for row in self.__pieces_list:
            for piece in row:
                if piece != "x" and piece.getColor() == color:
                    moves = piece.getAvaibleMoves(self.__pieces_list)
                    for move in moves:
                        avaible_moves.append(move)
        print(len(avaible_moves))
        return len(avaible_moves) != 0


    def draw(self):
        pass

    def checkmate(self):
        pass