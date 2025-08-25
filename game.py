import pygame
from random import shuffle
from sys import exit
from menu import Menu, MainMenu

class Game():
    def __init__(self):
        pygame.init()
        self.difficulty = 3
        self.running = True,
        self.playing = False
        flags = pygame.FULLSCREEN | pygame.RESIZABLE
        self.window = pygame.display.set_mode((0, 0), flags)
        self.tile_size = min(pygame.display.Info().current_h, pygame.display.Info().current_w)//self.difficulty       
        self.font = pygame.font.SysFont(None, self.tile_size//15)
        # self.board = None
        self.board_solved = False
        self.tileset = None
        self.empty_tile_position = [self.difficulty - 1, self.difficulty - 1]
        self.image = None
        self.menu = MainMenu(self)

    def is_solvable(self, list:list): 
            inversions = 0
            for i in range(0, self.difficulty ** 2 - 1):
                for j in range(i+1, self.difficulty ** 2 - 1):
                    if list[i] > list[j]:
                        inversions += 1
            if self.difficulty % 2 == 0:
                return inversions % 2 == 1
            else:
                return inversions % 2 == 0
            
    def generate_tileset(self):
            temp_tileset = [[] for i in range(self.difficulty)]
            id_list = [i for i in range(1, self.difficulty**2)]
            shuffle(id_list)
            while not self.is_solvable(id_list):
                shuffle(id_list)
            for row in range(self.difficulty):
                for column in range(self.difficulty):
                    if row == self.difficulty - 1 and column == self.difficulty - 1:
                        temp_tileset[row].insert(column, Game.Tile(self.difficulty**2, column, row, self.tile_size, self.difficulty))
                    else:
                        temp_tileset[row].insert(column, Game.Tile(id_list[-1], column, row, self.tile_size, self.difficulty))
                        id_list.pop()
            self.board_solved = False
            self.empty_tile_position = [self.difficulty - 1, self.difficulty - 1]
            return temp_tileset
    
    
    def move_tile(self, x, y):
            if self.empty_tile_position == [x, y]:
                return
            if self.empty_tile_position == [x + 1, y]:
                self.tileset[y][x], self.tileset[y][x + 1] = self.tileset[y][x + 1], self.tileset[y][x]
                self.tileset[y][x].x, self.tileset[y][x + 1].x = self.tileset[y][x + 1].x, self.tileset[y][x].x
                self.empty_tile_position = [x, y]
                return
            if self.empty_tile_position == [x - 1, y]:
                self.tileset[y][x], self.tileset[y][x - 1] = self.tileset[y][x - 1], self.tileset[y][x]
                self.tileset[y][x].x, self.tileset[y][x - 1].x = self.tileset[y][x - 1].x, self.tileset[y][x].x
                self.empty_tile_position = [x, y]
                return
            if self.empty_tile_position == [x, y + 1]:
                self.tileset[y][x], self.tileset[y + 1][x] = self.tileset[y + 1][x], self.tileset[y][x]
                self.tileset[y][x].y, self.tileset[y + 1][x].y = self.tileset[y + 1][x].y, self.tileset[y][x].y
                self.empty_tile_position = [x, y]
                return
            if self.empty_tile_position == [x, y - 1]:
                self.tileset[y][x], self.tileset[y - 1][x] = self.tileset[y - 1][x], self.tileset[y][x]
                self.tileset[y][x].y, self.tileset[y - 1][x].y = self.tileset[y - 1][x].y, self.tileset[y][x].y
                self.empty_tile_position = [x, y]
                return
            return
    
    def is_solved(self):
            temp_id = 1
            for row in range(self.difficulty):
                for column in range(self.difficulty):
                    if self.tileset[row][column].id != temp_id:
                        return 
                    else:
                        temp_id += 1
            self.board_solved = True
            return        
    
    def draw_board(self, surface, image, font):
            for row in self.tileset:
                for tile in row:
                    tile.draw(surface, image, font)
    
    def roll_board(self, image):
        self.tileset = self.generate_tileset()
        img = pygame.image.load(image).convert()
        temp_size = min(pygame.display.Info().current_h, pygame.display.Info().current_w)
        self.image = pygame.transform.scale(img, (temp_size, temp_size))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                tilex = x // (self.tile_size)
                tiley = y // (self.tile_size)
                if 0 <= tilex < self.difficulty and 0 <= tiley < self.difficulty:
                    self.move_tile(tilex, tiley)
            elif event.type == pygame.FINGERDOWN:
                x, y = event.x * self.window.get_height(), event.y * self.window.get_width()
                tilex = x // (self.tile_size)
                tiley = y // (self.tile_size)
                if 0 <= tilex < self.difficulty and 0 <= tiley < self.difficulty:
                    self.move_tile(tilex, tiley)
            self.is_solved()
            if self.board_solved:
                self.playing =  False
                self.menu.playing = True

    def gameloop(self):
        while self.playing:
            self.window.fill((255, 255, 255))
            self.draw_board(self.window, self.image, self.font)
            self.check_events() 
            pygame.display.update()
    
    class Tile():
        def __init__(self, id, x, y, tile_size, boardsize): 
            self.id = id
            self.x = x
            self.y = y
            self.tile_size = tile_size
            imagey = (self.id-1)//boardsize
            imagex = (self.id-1)%boardsize
            self.imagerect = pygame.Rect(
                imagex * tile_size, 
                imagey * tile_size, 
                tile_size, 
                tile_size 
            )

        def draw(self, surface, image, font):
            rect = pygame.Rect(
                self.x * self.tile_size, 
                self.y * self.tile_size, 
                self.tile_size, 
                self.tile_size 
            )
            
            # if self.id != self.board.size**2:
            surface.blit(image, rect, self.imagerect)
                
            # if self.id != self.board.size**2:
            text = font.render(str(self.id), True, (0, 0, 0))
            text_rect = text.get_rect(topleft=rect.topleft)   
            surface.blit(text, text_rect)

# class Game():
#     def __init__(self):
#         pygame.init()
#         self.difficulty = 1
#         self.running = True,
#         self.playing = False
#         flags = pygame.FULLSCREEN | pygame.RESIZABLE
#         self.window = pygame.display.set_mode((0, 0), flags)
#         self.tile_size = min(pygame.display.Info().current_h, pygame.display.Info().current_w)//(self.difficulty+2)        
#         self.font = pygame.font.SysFont(None, self.tile_size//15)
#         self.black = (0, 0, 0)
#         self.white = (255, 255, 255)
#         self.board = None
#         self.image = None
#         self.menu = MainMenu(self)
#         self.menu.playing = True

        
#     class Tile():
#         def __init__(self, id:int, x:int, y:int, board, tile_size, boardsize): 
#             self.id = id
#             self.x = x
#             self.y = y
#             self.board = board
#             self.tile_size = tile_size
#             imagey = (self.id-1)//boardsize
#             imagex = (self.id-1)%boardsize
#             self.imagerect = pygame.Rect(
#                 imagex * tile_size, 
#                 imagey * tile_size, 
#                 tile_size, 
#                 tile_size 
#             )

#         def __str__(self):
#             return f"|{self.id:>2},{self.x:>2},{self.y:>2}|"

#         def draw(self, surface, image, font):
#             rect = pygame.Rect(
#                 self.x * self.tile_size, 
#                 self.y * self.tile_size, 
#                 self.tile_size, 
#                 self.tile_size 
#             )
            
#             color = "white"
#             # if self.id != self.board.size**2:
#             surface.blit(image, rect, self.imagerect)
            
                
#             # if self.id != self.board.size**2:
#             text = font.render(str(self.id), True, (0, 0, 0))
#             text_rect = text.get_rect(topleft=rect.topleft)   
#             surface.blit(text, text_rect)
            


#     class Board:
#         def __init__(self, difficulty, game, tile_size):
#             self.game = game 
#             self.size = difficulty + 2
#             self.tile_size = tile_size
#             self.tileset = self.generate_tileset()
#             self.empty_tile_position = [self.size - 1, self.size - 1]
#             self.solved = False


        
#         def is_solvable(self, list:list): 
#             inversions = 0
#             for i in range(0, (self.size) ** 2 - 1):
#                 for j in range(i+1, (self.size) ** 2 - 1):
#                     if list[i] > list[j]:
#                         inversions += 1
#             if self.size % 2 == 0:
#                 return inversions % 2 == 1
#             else:
#                 return inversions % 2 == 0
        
#         def generate_tileset(self):
#             temp_tileset = [[] for i in range(self.size)]
#             id_list = [i for i in range(1, self.size**2)]
#             shuffle(id_list)
#             while not self.is_solvable(id_list):
#                 shuffle(id_list)
#             for row in range(self.size):
#                 for column in range(self.size):
#                     if row == self.size - 1 and column == self.size - 1:
#                         temp_tileset[row].insert(column, Game.Tile(self.size**2, column, row, self, self.tile_size, self.size))
#                     else:
#                         temp_tileset[row].insert(column, Game.Tile(id_list[-1], column, row, self, self.tile_size, self.size))
#                         id_list.pop()
#             return temp_tileset
        
#         def move_tile(self, x:int, y:int):
#             if self.empty_tile_position == [x, y]:
#                 return
#             if self.empty_tile_position == [x + 1, y]:
#                 self.tileset[y][x], self.tileset[y][x + 1] = self.tileset[y][x + 1], self.tileset[y][x]
#                 self.tileset[y][x].x, self.tileset[y][x + 1].x = self.tileset[y][x + 1].x, self.tileset[y][x].x
#                 self.empty_tile_position = [x, y]
#                 return
#             if self.empty_tile_position == [x - 1, y]:
#                 self.tileset[y][x], self.tileset[y][x - 1] = self.tileset[y][x - 1], self.tileset[y][x]
#                 self.tileset[y][x].x, self.tileset[y][x - 1].x = self.tileset[y][x - 1].x, self.tileset[y][x].x
#                 self.empty_tile_position = [x, y]
#                 return
#             if self.empty_tile_position == [x, y + 1]:
#                 self.tileset[y][x], self.tileset[y + 1][x] = self.tileset[y + 1][x], self.tileset[y][x]
#                 self.tileset[y][x].y, self.tileset[y + 1][x].y = self.tileset[y + 1][x].y, self.tileset[y][x].y
#                 self.empty_tile_position = [x, y]
#                 return
#             if self.empty_tile_position == [x, y - 1]:
#                 self.tileset[y][x], self.tileset[y - 1][x] = self.tileset[y - 1][x], self.tileset[y][x]
#                 self.tileset[y][x].y, self.tileset[y - 1][x].y = self.tileset[y - 1][x].y, self.tileset[y][x].y
#                 self.empty_tile_position = [x, y]
#                 return
#             return

#         def is_solved(self):
#             temp_id = 0
#             for row in range(self.size):
#                 for column in range(self.size):
#                     if self.tileset[column][row].id != temp_id:
#                         return 
#                     else:
#                         temp_id += 1
#             self.solved = True
#             return        

#         def draw_board(self, surface, image, font):
#             for row in self.tileset:
#                 for tile in row:
#                     tile.draw(surface, image, font)
            
#         def __str__(self):
#             string = ""
#             for row in self.tileset:
#                 for tile in row:
#                     string += str(tile)
#                 string += "\n"
#             return string

#     def roll_board(self, difficulty, image):
#         self.board = self.Board(self.difficulty, self, self.tile_size)  
#         img = pygame.image.load(image).convert()
#         temp_size = min(pygame.display.Info().current_h, pygame.display.Info().current_w)
#         self.image = pygame.transform.scale(img, (temp_size, temp_size))
    
#     def check_events(self):
#         if self.board.is_solved():
#             self.playing =  False
#             self.menu.playing = True
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.display.toggle_fullscreen()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 x, y = pygame.mouse.get_pos()
#                 tilex = x // (self.tile_size)
#                 tiley = y // (self.tile_size)
#                 if 0 <= tilex < self.board.size and 0 <= tiley < self.board.size:
#                     self.board.move_tile(tilex, tiley)
#             elif event.type == pygame.FINGERDOWN:
#                 x, y = event.x * self.window.get_height(), event.y * self.window.get_width()
#                 tilex = x // (self.tile_size)
#                 tiley = y // (self.tile_size)
#                 if 0 <= tilex < self.board.size and 0 <= tiley < self.board.size:
#                     self.board.move_tile(tilex, tiley)
                
#     def gameloop(self):
#         while self.playing:
#             self.window.fill(self.white)
#             self.board.draw_board(self.window, self.image, self.font)
#             self.check_events()
#             pygame.display.update()
