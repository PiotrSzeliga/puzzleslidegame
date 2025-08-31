import pygame
from random import shuffle
from sys import exit
from menu import Menu, MainMenu, DifficultyMenu

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
        self.main_menu = MainMenu(self)
        self.is_difficulty_menu = True
        if self.is_difficulty_menu:
            self.diff_menu = DifficultyMenu(self)

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
            self.tileset = temp_tileset
    
    
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
        temp_size = min(pygame.display.Info().current_h, pygame.display.Info().current_w)
        self.image = pygame.transform.scale(image, (temp_size, temp_size))

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
            self.boardsize = boardsize
            imagey = (self.id-1)//self.boardsize
            imagex = (self.id-1)%self.boardsize
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
            
            if self.id != self.boardsize**2:
                text = font.render(str(self.id), True, (255, 255, 255), (0, 0, 0))
                # text_rect = text.get_rect(topleft=self.imagerect.topleft)   
                image.blit(text, self.imagerect.topleft, None, pygame.BLEND_SUB)
            
            if self.id != self.boardsize**2:
                surface.blit(image, rect, self.imagerect)
                

            
