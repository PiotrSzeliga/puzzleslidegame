from game import Game
from menu import Menu, MainMenu

g = Game()

while g.running:
    g.main_menu.menuloop()
    g.diff_menu.menuloop()
    g.gameloop()
