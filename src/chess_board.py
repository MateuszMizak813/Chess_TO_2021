import pygame
import constants as con
from chess_piece import *
from game_state import GameHistory
import random
"""
Klasa Szachownicy, odpowiedzialna za przechowywanie pionków, wszystkie aspekty graficzne, oraz funkcjonalność pomiędzy pionkami.
"""
class ChessBoard():
    def __init__(self, screen, light_color = 'white', dark_color = 'brown', againstAi = False) -> None:
        self.__screen = screen
        self.__colors = [light_color, dark_color]
        self.__againstAi = againstAi
        if self.__againstAi:
            self.__chess_bot = ChessBot(self)
        self.__pieces_list = self.generatePieceList()
        self.__kings = {"w": self.__pieces_list[7][4], "b": self.__pieces_list[0][4]}
        self.__special_moves = {"short_castle": [SavedMove((x,4),(x,6),self.__pieces_list[x][4],"x") for x in [0,7]],
                                "long_castle" : [SavedMove((x,4),(x,2),self.__pieces_list[x][4],"x") for x in [0,7]]}
        self.__selected_piece = False
        self.__game_history = GameHistory()
        self.__player_turn = "w"
        self.__game_ended = False
        self.__avaible_moves = self.checkForValidMoves(self.__player_turn)
        self.drawBoard()
        self.drawPieces()

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
        if self.__game_ended == False:
            clicked_field = self.__pieces_list[row][column]

            #Nacisnięto na własny pionek, wyświetlane są dostępne ruchy
            if self.__selected_piece == False and clicked_field != 'x' and clicked_field.getColor() == self.__player_turn:
                self.__selected_piece = clicked_field
                piece_moves = self.__selected_piece.getAvaibleMoves(self.__pieces_list)
                self.drawBoard()
                for move in self.__avaible_moves:
                    if move.getMoved() == self.__selected_piece:
                        end = move.getEnd()
                        if move.getCaptured() == "x":
                            pygame.draw.circle(self.__screen, "green", (end[1]*con.field_size + con.field_size/2, end[0]*con.field_size + con.field_size/2), 0.4*con.field_size)
                        else:
                            pygame.draw.circle(self.__screen, "crimson", (end[1]*con.field_size + con.field_size/2, end[0]*con.field_size + con.field_size/2), 0.4*con.field_size)
                start = self.__selected_piece.getField()
                pygame.draw.circle(self.__screen, "teal", (start[1]*con.field_size + con.field_size/2, start[0]*con.field_size + con.field_size/2), 0.4*con.field_size)
                self.drawPieces()

            #Naciśnięto ponownie ten sam pionek - odznaczenie pionka
            elif self.__selected_piece == clicked_field:
                self.__selected_piece = False
                self.drawBoard()
                self.drawPieces()
                
            #naciśnięto inne pole mając wcześniej zaznaczony pionek
            elif self.__selected_piece != False:
                move = SavedMove(self.__selected_piece.getField(),(row,column), self.__selected_piece, clicked_field)
                if move in self.__avaible_moves:
                    self.makeMove(move)

                    self.drawBoard()
                    self.drawPieces()
                    self.__game_history.clearForward()

                    self.endTurn()


    def makeMove(self, move:SavedMove):
        start = move.getStart()
        end = move.getEnd()
        moved = move.getMoved()
        captured = move.getCaptured()
        self.__pieces_list[start[0]][start[1]] = "x"
        self.__pieces_list[end[0]][end[1]] = moved
        moved.move(end)
        if captured != "x":
            captured.setAlive(False)
        #check for castle
        if move in self.__special_moves["short_castle"]:
            rook = self.__pieces_list[end[0]][end[1] + 1]
            if rook != "x":
                rook.move((end[0], end[1] - 1))
                self.__pieces_list[end[0]][end[1] - 1] = rook
                self.__pieces_list[end[0]][end[1] + 1] = "x"
        elif move in self.__special_moves["long_castle"]:
            rook = self.__pieces_list[end[0]][end[1] - 2]
            if rook != "x":
                rook.move((end[0], end[1] + 1))
                self.__pieces_list[end[0]][end[1] + 1] = rook
                self.__pieces_list[end[0]][end[1] - 2] = "x"

        self.__game_history.addMove(move)
        


    def undo(self, soft=False):
        move = self.__game_history.undoMove(soft)
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

            #check for castle
            if move in self.__special_moves["short_castle"]:
                rook = self.__pieces_list[end[0]][end[1] - 1]
                if rook != "x":
                    rook.undoMove((end[0], end[1] + 1))
                    self.__pieces_list[end[0]][end[1] - 1] = "x"
                    self.__pieces_list[end[0]][end[1] + 1] = rook
            elif move in self.__special_moves["long_castle"]:
                rook = self.__pieces_list[end[0]][end[1] + 1]
                if rook != "x":
                    rook.undoMove((end[0], end[1] - 2))
                    self.__pieces_list[end[0]][end[1] - 2] = rook
                    self.__pieces_list[end[0]][end[1] + 1] = "x"

            if not soft:
                self.drawBoard()
                self.drawPieces()
                self.endTurn(should_ai_move=False)
            

    def forward(self):
        move = self.__game_history.forwardMove()
        if move != None:
            start = move.getStart()
            end = move.getEnd()
            captured = move.getCaptured()
            moved = move.getMoved()
            self.__pieces_list[end[0]][end[1]] = moved
            self.__pieces_list[start[0]][start[1]] = "x"
            moved.move(end)

            if captured != "x":
                captured.setAlive(False)

            if move in self.__special_moves["short_castle"]:
                rook = self.__pieces_list[end[0]][end[1] + 1]
                if rook != "x":
                    rook.move((end[0], end[1] - 1))
                self.__pieces_list[end[0]][end[1] - 1] = rook
                self.__pieces_list[end[0]][end[1] + 1] = "x"
            elif move in self.__special_moves["long_castle"]:
                rook = self.__pieces_list[end[0]][end[1] - 2]
                if rook != "x":
                    rook.move((end[0], end[1] + 1))
                self.__pieces_list[end[0]][end[1] + 1] = rook
                self.__pieces_list[end[0]][end[1] - 2] = "x"

            self.drawBoard()
            self.drawPieces()
            self.endTurn(should_ai_move=False)

    def checkForChecks(self, color): #color = color of king to check
        check = False
        if color == "w":
            enemy = "b"
        else:
            enemy = "w"
        moves = self.checkForValidMoves(enemy)
        for move in moves:
            if move.getCaptured() == self.__kings[color]:
                check = True
        return check

    def checkForAvaibleMoves(self, color):
        avaible_moves = []
        for row in self.__pieces_list:
            for piece in row:
                if piece != "x" and piece.getColor() == color:
                    moves = piece.getAvaibleMoves(self.__pieces_list)
                    for move in moves:
                        avaible_moves.append(move)
        return avaible_moves

    def checkForValidMoves(self, color):
        if color == "w":
            enemy = "b"
        else:
            enemy = "w"
        #Wyszukanie bazowych możliwych ruchów
        avaible_moves = self.checkForAvaibleMoves(color)
        valid_moves = []
        for move in avaible_moves:
            self.makeMove(move)
            check = False
            enemy_moves = self.checkForAvaibleMoves(enemy)
            for enemy_move in enemy_moves:
                if enemy_move.getCaptured() == self.__kings[color]:
                    check = True
            if check == False:
                valid_moves.append(move)
            self.undo(soft=True)
        #Wyszukanie specjalnych ruchów:
        if not self.__kings[color].didMove():
            k_pos = self.__kings[color].getField()
            #short castling
            if self.__pieces_list[k_pos[0]][5] == "x" and self.__pieces_list[k_pos[0]][6] == "x":
                if self.__pieces_list[k_pos[0]][7] != "x" and not self.__pieces_list[k_pos[0]][7].didMove():
                    valid_moves.append(SavedMove(k_pos, (k_pos[0], 6), self.__kings[color], self.__pieces_list[k_pos[0]][6]))
            #long castling
            if self.__pieces_list[k_pos[0]][3] == "x" and self.__pieces_list[k_pos[0]][2] == "x" and self.__pieces_list[k_pos[0]][1] == "x":
                if self.__pieces_list[k_pos[0]][0] != "x" and not self.__pieces_list[k_pos[0]][0].didMove():
                    valid_moves.append(SavedMove(k_pos, (k_pos[0], 2), self.__kings[color], self.__pieces_list[k_pos[0]][2]))
            

        return valid_moves


    def endTurn(self,should_ai_move = True):
        if self.__player_turn == "w":
            self.__player_turn = "b"
        else:
            self.__player_turn = "w"
        self.__selected_piece = False

        self.__avaible_moves = self.checkForValidMoves(self.__player_turn)
        draw = self.__game_history.checkForDraw()

        if len(self.__avaible_moves) == 0:
            check = self.checkForChecks(self.__player_turn)
            if check:
                if self.__player_turn == "w":
                    txt = "Black"
                else:
                    txt = "White"
                print("Checkmate!",txt,"won!")
                self.__game_ended = True
            else:
                print("Stalemate!")
                self.__game_ended = True
        elif draw:
            print("Draw! 4 times same postion!")
            self.__game_ended = True
        else:
            self.__game_ended = False

        if should_ai_move and self.__againstAi:
            self.drawBoard()
            self.drawPieces()
            self.__chess_bot.AiToMove()
            self.drawBoard()
            self.drawPieces()
            
        
class ChessBot():
    def __init__(self, chess_board:ChessBoard) -> None:
        self.__chess_board = chess_board
        self.__piece_points = {"Pawn":1,"Knight":3,"Bishop":3,"Rook":5,"Queen":9,"King":999999}
        self.__my_turn = {True:'b',False:'w'}
    def AiToMove(self):
        valid_moves = {move: 0 for move in self.__chess_board.checkForValidMoves(self.__my_turn[True])}
        for move,points in valid_moves.items():
            points = self.getPointsForMove(move, 2, True)
            valid_moves[move] = points
        
        best_points = -999
        best_moves = []

        for move,points in valid_moves.items():
            if points > best_points:
                best_points = points
                best_moves.clear()
                best_moves.append(move)
            if points == best_points:
                best_moves.append(move)

        if len(best_moves) > 1:
            self.__chess_board.makeMove(random.choice(best_moves))
        else:
            self.__chess_board.makeMove(best_moves[0])
        self.__chess_board.endTurn(should_ai_move=False)
        
                    
    def getPointsForMove(self, move:SavedMove, depth, myTurn:bool):
        points = 0
        if myTurn:
            mod = 1
        else:
            mod = -2


        self.__chess_board.makeMove(move)

        if move.getCaptured() != "x":
            points += mod* self.__piece_points[move.getCaptured().getName()]

        if depth > 0:
            points_list =[]
            new_valid_moves = self.__chess_board.checkForValidMoves(self.__my_turn[not myTurn])
            if len(new_valid_moves) > 0:
                for new_move in new_valid_moves:
                    points_list.append(self.getPointsForMove(new_move, depth-1, not myTurn))
                if myTurn:
                    points += min(points_list)
                else:
                    points += max(points_list)

        self.__chess_board.undo(soft=True)

        return points
