import pygame
import yaml
from random import shuffle
from menu import Menu, MainMenu, DifficultyMenu
from tile import Tile
from victoryscreen import VictoryScreen
from button import Button
from infopage import InfoPage


class Game():
    def __init__(self):
        pygame.init()
        
        flags = pygame.FULLSCREEN | pygame.RESIZABLE
        self.window = pygame.display.set_mode((0,0), flags)

        self.clock = pygame.time.Clock()
        
        self.running = True
        self.playing = False

        with open("config.yml", 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        
        self.difficulty = self.config["difficulty_menu"]["base_difficulty"]
        
        self.background_color = self.config["puzzleslidegame"]["color_background"]
        self.lines_color = self.config["puzzleslidegame"]["color_lines"]
        
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w
        self.max_board_size =  min(window_height, window_width)
        self.board = pygame.Rect(0, 0, self.max_board_size, self.max_board_size)
        self.tile_size = self.max_board_size//self.difficulty
        self.tileset = None
        self.tileset_blank_index = None
        self.is_tileset_solved = False
        self.image = None
        self.tile_draw_id = self.config["tiles"]["is_id_displayed"]

        self.font = pygame.font.SysFont(self.config["puzzleslidegame"]["font_name"], self.tile_size//15)
       
        self.main_menu = MainMenu(self)
        self.main_menu.playing = True
        
        self.enable_difficulty_menu = self.config["difficulty_menu"]["is_difficulty_menu"]
        self.difficulty_menu = DifficultyMenu(self)
        if self.enable_difficulty_menu:
            self.difficulty_menu.playing = True
        
        self.victory_screen = VictoryScreen(self)

        home = pygame.image.load(f'resources/assets/home.png').convert_alpha()
        reset = pygame.image.load(f'resources/assets/reset.png').convert_alpha()
        info = pygame.image.load(f'resources/assets/info.png').convert_alpha()
        
        if window_width > window_height:
            len = window_width - ((window_width-self.max_board_size)//2)
            self.home_button = Button(
                self.window, 
                (self.tile_size//3, self.tile_size//3), 
                (len , window_height*0.3), 
                home, 
                (self.tile_size//10, self.tile_size//10), 
                True, 2, 25, self.background_color)
            self.reset_button = Button(
                self.window, 
                (self.tile_size//3, self.tile_size//3), 
                (len , window_height*0.5), 
                reset, 
                (self.tile_size//10, self.tile_size//10), 
                True, 2, 25, self.background_color)
            self.info_button = Button(
                self.window, 
                (self.tile_size//3, self.tile_size//3), 
                (len , window_height*0.7), 
                info, 
                (self.tile_size//10, self.tile_size//10), 
                True, 2, 25, self.background_color)
        else:
            len =  window_height - ((window_height-self.max_board_size)//2)
            self.home_button = Button(
                self.window, 
                (self.tile_size//3, self.tile_size//3), 
                (window_height*0.3, len), 
                home, 
                (self.tile_size//10, self.tile_size//10), 
                True, 2, 25, self.background_color)
            self.reset_button = Button(
                self.window, 
                (self.tile_size//3, self.tile_size//3), 
                (window_height*0.5, len), 
                reset, 
                (self.tile_size//10, self.tile_size//10), 
                True, 2, 25, self.background_color)
            self.info_button = Button(
                self.window, 
                (self.tile_size//3, self.tile_size//3), 
                (window_height*0.7, len), 
                info, 
                (self.tile_size//10, self.tile_size//10), 
                True, 2, 25, self.background_color)

        self.infopage = InfoPage(self)

    
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
        temp_tileset = []
        id_list = [i for i in range(1, self.difficulty**2)]
        shuffle(id_list)
        while not self.is_solvable(id_list):
            shuffle(id_list)
        id_list.insert(0, self.difficulty**2)
        for i in range(self.difficulty):
            for j in range(self.difficulty):
                temp_tileset.append(Tile(self, id_list[-1], (self.board.x + j*self.tile_size, self.board.y + i*self.tile_size), self.tile_draw_id))
                id_list.pop()
        self.is_tileset_solved = False
        self.tileset = temp_tileset
        self.tileset_blank_index = self.difficulty**2-1


    def tileset_blank_swap(self, tile:Tile, blank:Tile):
        index_tile = self.tileset.index(tile)
        self.tileset[index_tile], self.tileset[self.tileset_blank_index] = self.tileset[self.tileset_blank_index], self.tileset[index_tile]
        self.tileset_blank_index = index_tile
        
        x = (index_tile)%self.difficulty
        y = (index_tile)//self.difficulty
        
        self.tileset[index_tile].pos_rect.topleft = (x*self.tile_size, y*self.tile_size)

    
    def is_solved(self):
        temp_id = 1
        for tile in self.tileset:
            if tile.id != temp_id:
                return
            else:
                temp_id += 1
        self.is_tileset_solved = True


    def draw_board(self):
        for tile in self.tileset:
            tile.draw()


    def draw_buttons(self):
        self.home_button.draw()
        self.reset_button.draw()
        self.info_button.draw()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.home_button.button_rect.collidepoint(pos):
                    self.main_menu.playing = True
                    self.playing = False
                elif self.reset_button.button_rect.collidepoint(pos):
                    self.generate_tileset()
                elif self.info_button.button_rect.collidepoint(pos):
                    self.infopage.playing = True
                else:
                    for tile in self.tileset:
                        if tile.pos_rect.collidepoint(pos) and not tile.blank:
                            tile.clicked = True
                            pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                for tile in self.tileset:
                    tile.clicked = False
            
        for tile in self.tileset:
            if tile.clicked:
                x, y = pygame.mouse.get_rel()
                rect_move_x = tile.pos_rect.move(x, 0)
                rect_move_y = tile.pos_rect.move(0, y)
                if not self.board.contains(rect_move_x):
                    x = 0
                else:
                    collisions_x = rect_move_x.collideobjectsall(self.tileset, key=lambda t: t.pos_rect)
                    for tile_x in collisions_x:
                        if not tile_x.blank and tile_x.id != tile.id:
                            x = 0
                if not self.board.contains(rect_move_y):
                    y = 0
                else:
                    collisions_y = rect_move_y.collideobjectsall(self.tileset, key=lambda t: t.pos_rect)
                    for tile_y in collisions_y:
                        if not tile_y.blank and tile_y.id != tile.id:
                            y=0
                
                tile_far = False
                tile_perfect_x = (self.tileset.index(tile))%self.difficulty*self.tile_size
                tile_perfect_y = (self.tileset.index(tile))//self.difficulty*self.tile_size
                
                if (tile.pos_rect.x - tile_perfect_x)**2 + (tile.pos_rect.y -tile_perfect_y )**2 > (self.tile_size//20)**2:
                    tile_far = True         
    
                tile.pos_rect.move_ip(x, y)

                if (tile.pos_rect.x - self.tileset[self.tileset_blank_index].pos_rect.x)**2 + (tile.pos_rect.y - self.tileset[self.tileset_blank_index].pos_rect.y)**2 <= (self.tile_size//20)**2:
                    tile.pos_rect.topleft = self.tileset[self.tileset_blank_index].pos_rect.topleft
                    self.tileset_blank_swap(tile, self.tileset[self.tileset_blank_index])
                if (tile.pos_rect.x - tile_perfect_x)**2 + (tile.pos_rect.y - tile_perfect_y)**2 <= (self.tile_size//20)**2 and tile_far == True:
                    tile.pos_rect.topleft = (tile_perfect_x, tile_perfect_y)

        self.is_solved()
        if self.is_tileset_solved:
            self.playing =  False
            self.victory_screen.playing = True


    def cut_rounded_image(self, image, radius):
        w, h = image.get_size()

        mask = pygame.Surface((w,h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255,255,255,255), (0,0,w,h), border_radius=radius)

        rounded = pygame.Surface((w,h), pygame.SRCALPHA)
        rounded.blit(image, (0,0))

        rounded.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        return rounded


    def gameloop(self):
        while self.playing:
            self.window.fill(self.background_color)
            self.draw_board()
            self.draw_buttons()
            self.check_events() 
            self.infopage.infopageloop()
            # self.playing = False
            # self.victory_screen.playing = True
            pygame.display.update()
            