import pygame
from os import listdir
from button import Button


class Menu():
    def __init__(self, game):
        self.game = game
        self.playing = False
        self.window = self.game.window
        

    def draw_menu(self):
        pass
    

    def event_handle(self):
        pass
    

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.difficulty_menu.playing = False
                self.playing = False
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.event_handle(x, y)

    
    def menuloop(self):
        while self.playing:
            self.window.fill(self.game.background_color)
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

        self.rect_mid = pygame.Rect(0, 0, self.len*8//10, self.len*8//10)
        self.rect_mid.center = (window_width//2, window_height//2)
       
        play_img = pygame.image.load("resources/assets/play.png").convert_alpha()
        self.play_img = pygame.transform.scale(play_img, (self.len*0.1, self.len*0.1))
        self.play_img_rect = pygame.Rect((0,0), (self.len*0.1, self.len*0.1))
        self.play_img_rect.center = self.rect_mid.center
        
        arrow = pygame.image.load("resources/assets/arrow.png").convert_alpha()
        arrow_l = pygame.transform.rotate(arrow, -90)
        arrow_r = pygame.transform.rotate(arrow, 90)
        
        if window_width > window_height:
            self.left_arrow_button = Button(
                self.window,
                (self.len//10, self.len//10),
                (window_width*0.1, window_height//2),
                arrow_l,
                (self.len//10, self.len//10))
            self.right_arrow_button = Button(
                self.window,
                (self.len//10, self.len//10),
                (window_width*0.9, window_height//2),
                arrow_r,
                (self.len//10, self.len//10))
        else:
            self.left_arrow_button = Button(
                self.window,
                (self.len//10, self.len//10),
                (window_width*0.3, window_height*0.8),
                arrow_l,
                (self.len//10, self.len//10))
            self.right_arrow_button = Button(
                self.window,
                (self.len//10, self.len*0/8),
                (window_width*0.8, window_height//2),
                arrow_r,
                (self.len//10, self.len//10))


    def draw_menu(self):
        self.window.blit(self.imglist[self.imglist_index], self.rect_mid)
        self.window.blit(self.play_img, self.play_img_rect)
        self.left_arrow_button.draw()
        self.right_arrow_button.draw()

        
    def event_handle(self, x, y):   
        if self.rect_mid.collidepoint(x, y):
            self.game.image = pygame.transform.scale(self.imglist[self.imglist_index], (self.game.max_board_size, self.game.max_board_size))
            self.game.difficulty_menu.playing = True
            if not self.game.enable_difficulty_menu:
                self.game.tile_size = self.game.max_board_size//self.game.difficulty       
                self.game.font = pygame.font.SysFont(None, self.game.tile_size//15)
                self.game.generate_tileset()
                self.game.difficulty_menu.playing = False
            self.playing = False
        elif self.left_arrow_button.button_rect.collidepoint(x, y):
            if self.imglist_index == 0:
                self.imglist_index = len(self.imglist)-1
            else:
                self.imglist_index -= 1
        elif self.right_arrow_button.button_rect.collidepoint(x, y):
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
        self.rect_left = pygame.Rect(0, 0, self.len//5, self.len//5)
        self.rect_left.center = (window_width*0.3, window_height//2)
        self.rect_right = pygame.Rect(0, 0,self.len//5, self.len//5)
        self.rect_right.center = (window_width*0.7, window_height//2)
        self.rect_list = [self.rect_left, self.rectmid, self.rect_right]
    
        star = pygame.image.load('resources/assets/star.png').convert_alpha()
        self.star = pygame.transform.scale(star, (self.len//20, self.len//20))

        star_rect_0 = self.star.get_rect(center = self.rect_left.center)
        star_rect_1 = self.star.get_rect(midright = self.rectmid.center)
        star_rect_2 = self.star.get_rect(midleft = self.rectmid.center)
        star_rect_3 = self.star.get_rect(midbottom = self.rect_right.center)
        star_rect_4 = self.star.get_rect(topright = self.rect_right.center)
        star_rect_5 = self.star.get_rect(topleft = self.rect_right.center)
        self.star_rect_list = [star_rect_0, star_rect_1, star_rect_2, star_rect_3, star_rect_4, star_rect_5]
    
    
    def draw_menu(self):
        for rect in self.rect_list:
            pygame.draw.rect(self.window, self.game.lines_color, rect, 2, 50)

        for rect in self.star_rect_list:
            self.window.blit(self.star, rect)
         

    def event_handle(self, x, y):   
        for i in self.rect_list:
            if i.collidepoint(x, y):
                self.game.difficulty = self.rect_list.index(i) + 3
                self.game.tile_size = self.game.max_board_size//self.game.difficulty       
                self.game.font = pygame.font.SysFont(None, self.game.tile_size//15)
                self.game.generate_tileset()
                self.playing = False
                self.game.playing = True
