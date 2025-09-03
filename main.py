import pygame
import sys
from game import Game
from menu import Menu, MainMenu

g = Game()

while g.running:
    g.main_menu.menuloop()
    g.difficulty_menu.menuloop()
    g.gameloop()
    g.clock.tick(60)

pygame.display.quit()
pygame.quit()
sys.exit()