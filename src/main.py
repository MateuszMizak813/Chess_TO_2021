import pygame
from chess_board import ChessBoard
import constants as con
import sys

"""
Główna klasa odpowiedzialna za uruchominie i zarządzanie oknem gry, eventami oraz przygotowująco wszystkie niezbędne elementy
"""
class main():
    """
    Kontruktor klasy głównej, tworzy instancje okna gry, szchownicy i innych niezbędnych rzeczy oraz zawiera główną pętle programu
    """
    def __init__(self) -> None:
        # Inicjalizacja biblioteki pygame
        pygame.init()

        # Ustawienia ekranu i zainicjowanie niezbędnych elementów
        self.__chess_window = pygame.display.set_mode((640,640))
        self.__chess_window.fill((255,255,255))
        self.__clock = pygame.time.Clock()
        self.__chess_board = ChessBoard(self.__chess_window)

        # Wejście do pętli głównej
        self.mainLoop()


    """
    Główna pętla programu odpowiedzialna za przechwytywanie eventów
    """
    def mainLoop(self):
        # Ustawienie warunku zakończenia pętli
        self.__loop = True

        # Główna pętla programu 
        while self.__loop:

            # Przechwytywanie wydarzeń na ekranie
            for event in pygame.event.get():

                # Nacisnięcie X - wyłączenie programu
                if event.type == pygame.QUIT:
                    self.__loop = False

                # Naciśnięcie przycisku myszy
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    position = pygame.mouse.get_pos()

                    # Przycisk myszy naciśnięty w obrębie szachownicy
                    if position[0] <= con.field_size * 8 and position[1] <= con.field_size *8:
                        column = position[0] // con.field_size
                        row = position[1] // con.field_size
                        self.__chess_board.leftClickOnChessBoard(row,column)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.__chess_board.undo()
                    if event.key == pygame.K_RIGHT:
                        self.__chess_board.forward()
        
            # Odświeżanie obrazu
            self.__clock.tick(15)
            pygame.display.flip()
    
# Uruchomienie Programu
if __name__ == "__main__":
    main()