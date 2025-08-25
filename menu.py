import pygame
from os import listdir
from sys import exit

class Menu():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.running = True
        self.playing = True
        flags = pygame.FULLSCREEN | pygame.RESIZABLE
        self.window = pygame.display.set_mode((0, 0), flags)
        
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
        self.images = listdir('resources/images/')
        self.imagesindex = 0
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w
        self.len = min(window_height, window_width)
        self.rectmid = pygame.Rect(0, 0, self.len*8//10, self.len*8//10)
        self.rectmid.center = (window_width//2, window_height//2)
        self.rectleft = pygame.Rect(0, 0, self.len//10, self.len//10)
        self.rectleft.center = (window_width*0.1, window_height//2)
        self.rectright = pygame.Rect(0, 0,self.len//10, self.len//10)
        self.rectright.center = (window_width*0.9, window_height//2)
        self.rectlist = [self.rectmid, self.rectleft, self.rectright]
        self.mainimgpath = None

    def draw_menu(self):
        for i in self.rectlist:
            pygame.draw.rect(self.window, (255, 255, 255), i)
            imgpath = f'resources/images/{self.images[self.imagesindex]}'
            img = pygame.image.load(imgpath).convert()
            img = pygame.transform.scale(img, (self.len*8//10, self.len*8//10))
            self.window.blit(img, self.rectmid)
            arrow = pygame.image.load(f'resources/assets/arrow.png').convert_alpha()
            arrow = pygame.transform.scale(arrow, (self.len//10, self.len//10))
            arrow_l = pygame.transform.rotate(arrow, -90)
            arrow_r = pygame.transform.rotate(arrow, 90)
            self.window.blit(arrow_l, self.rectleft)
            self.window.blit(arrow_r, self.rectright)
            self.mainimgpath = imgpath
        
    def event_handle(self, x, y):   
        if self.rectmid.collidepoint(x, y):
            self.game.roll_board(self.mainimgpath)
            self.playing = False
            self.game.playing = True
        elif self.rectleft.collidepoint(x, y):
            if self.imagesindex == 0:
                self.imagesindex = len(self.images)-1
            else:
                self.imagesindex -= 1
        elif self.rectright.collidepoint(x, y):
            if self.imagesindex == len(self.images)-1:
                self.imagesindex = 0
            else:
                self.imagesindex += 1




        