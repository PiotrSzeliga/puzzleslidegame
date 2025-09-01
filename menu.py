import pygame
from os import listdir
from sys import exit

class Menu():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.running = True
        self.playing = True
        self.window = self.game.window
        
    def draw_menu(self):
        pass
    
    def event_handle(self):
        pass
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.event_handle(x, y)
            elif event.type == pygame.FINGERDOWN:
                x, y = event.x * self.window.get_height(), event.y * self.window.get_width()
                self.event_handle(x, y)
    
    def menuloop(self):
        while self.playing:
            self.window.fill((255, 255, 255))
            self.draw_menu()
            self.check_events()
            pygame.display.update()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w
        self.len = min(window_height, window_width)
        
        images = listdir('resources/images/')
        self.imglist = []
        self.imglist_index = 0
        for i in images:
            img = pygame.image.load(f'resources/images/{i}').convert_alpha()
            img = pygame.transform.scale(img, (self.len*8//10, self.len*8//10))
            self.imglist.append(img)

        self.rectmid = pygame.Rect(0, 0, self.len*8//10, self.len*8//10)
        self.rectmid.center = (window_width//2, window_height//2)
        self.rectleft = pygame.Rect(0, 0, self.len//10, self.len//10)
        self.rectleft.center = (window_width*0.1, window_height//2)
        self.rectright = pygame.Rect(0, 0,self.len//10, self.len//10)
        self.rectright.center = (window_width*0.9, window_height//2)
        self.rectlist = [self.rectmid, self.rectleft, self.rectright]
        
        arrow = pygame.image.load(f'resources/assets/arrow.png').convert_alpha()
        arrow = pygame.transform.scale(arrow, (self.len//10, self.len//10))
        self.arrow_l = pygame.transform.rotate(arrow, -90)
        self.arrow_r = pygame.transform.rotate(arrow, 90)
    
    def draw_menu(self):
        for i in self.rectlist:
            pygame.draw.rect(self.window, (255, 255, 255), i)
        self.window.blit(self.imglist[self.imglist_index], self.rectmid)
        self.window.blit(self.arrow_l, self.rectleft)
        self.window.blit(self.arrow_r, self.rectright)
        
    def event_handle(self, x, y):   
        if self.rectmid.collidepoint(x, y):
            self.game.roll_board(self.imglist[self.imglist_index])
            self.playing = False
            self.game.playing = True
        elif self.rectleft.collidepoint(x, y):
            if self.imglist_index == 0:
                self.imglist_index = len(self.imglist)-1
            else:
                self.imglist_index -= 1
        elif self.rectright.collidepoint(x, y):
            if self.imglist_index == len(self.imglist)-1:
                self.imglist_index = 0
            else:
                self.imglist_index += 1

class DifficultyMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w
        self.len = min(window_height, window_width)
        
        self.rectmid = pygame.Rect(0, 0, self.len//5, self.len//5)
        self.rectmid.center = (window_width//2, window_height//2)
        self.rectleft = pygame.Rect(0, 0, self.len//5, self.len//5)
        self.rectleft.center = (window_width*0.3, window_height//2)
        self.rectright = pygame.Rect(0, 0,self.len//5, self.len//5)
        self.rectright.center = (window_width*0.7, window_height//2)
        self.rect_list = [self.rectleft, self.rectmid, self.rectright]
    
        star = pygame.image.load(f'resources/assets/star.png').convert_alpha()
        self.star = pygame.transform.scale(star, (self.len//20, self.len//20))

        star_rect_0 = self.star.get_rect(center = self.rectleft.center)
        star_rect_1 = self.star.get_rect(midright = self.rectmid.center)
        star_rect_2 = self.star.get_rect(midleft = self.rectmid.center)
        star_rect_3 = self.star.get_rect(midbottom = self.rectright.center)
        star_rect_4 = self.star.get_rect(topright = self.rectright.center)
        star_rect_5 = self.star.get_rect(topleft = self.rectright.center)
        self.star_rect_list = [star_rect_0, star_rect_1, star_rect_2, star_rect_3, star_rect_4, star_rect_5]
    
    def draw_menu(self):
        for rect in self.rect_list:
            rect2 = rect.inflate(2, 2)
            pygame.draw.rect(self.window, (0, 0, 0), rect2)
            pygame.draw.rect(self.window, (255, 255, 255), rect)

        for rect in self.star_rect_list:
            self.window.blit(self.star, rect)
         
    def event_handle(self, x, y):   
        for i in self.rect_list:
            if i.collidepoint(x, y):
                self.game.difficulty = self.rect_list.index(i) + 3
                self.game.tile_size = min(pygame.display.Info().current_h, pygame.display.Info().current_w)//self.game.difficulty       
                self.game.font = pygame.font.SysFont(None, self.game.tile_size//15)
                self.game.empty_tile_position = [self.game.difficulty - 1, self.game.difficulty - 1]
                self.game.generate_tileset()
                self.playing = False
                self.game.playing = True
