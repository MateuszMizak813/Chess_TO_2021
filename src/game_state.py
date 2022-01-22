import pygame
import constants as con


"""
Klasa odpowiedzialna za przechowywanie stanu gry w celu umożliwienia zapisu i odczytu wybranych tur 
NOT IMPLEMENTED YET
"""
class GameHistory():
    def __init__(self):
        self.__move_list = []
        self.__undone_moves = []

    def addMove(self, move):
        self.__move_list.append(move)
    
    def undoMove(self, soft=False):
        if len(self.__move_list) > 0:
            move = self.__move_list.pop(-1)
            if soft==False:
                self.__undone_moves.append(move)
            return move

    def forwardMove(self):
        if len(self.__undone_moves) > 0:
            move = self.__undone_moves.pop(-1)
            self.__move_list.append(move)
            return move
    
    def clearForward(self):
        self.__undone_moves.clear()

    def checkForDraw(self):
        draw = False
        if len(self.__move_list) > 0:
            last_move = self.__move_list[-1]
            count = 0
            for move in self.__move_list:
                if move.getMoved() == last_move.getMoved() and move.getEnd() == last_move.getEnd():
                    count += 1
            if count > 3:
                draw = True
        return draw
