import pygame
from button import Button


class VictoryScreen():
    def __init__(self, game):
        self.game = game
        self.playing = False
        self.window = self.game.window
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w

        self.base_language = self.game.config["puzzleslidegame"]["base_language"]

        pol = pygame.image.load(f'resources/assets/pol.png').convert_alpha()
        eng = pygame.image.load(f'resources/assets/eng.png').convert_alpha()

        pol = pygame.transform.scale(pol, (self.game.max_board_size*0.07, self.game.max_board_size*0.07))
        eng = pygame.transform.scale(eng, (self.game.max_board_size*0.07, self.game.max_board_size*0.07))
        
        pol = self.game.cut_rounded_image(pol, 15)
        eng = self.game.cut_rounded_image(eng, 15)

        
        self.pol_text = self.game.config["victory_screen"]["pol"]
        self.eng_text = self.game.config["victory_screen"]["eng"]

        self.text = None
        
        if self.base_language == 0:
            self.text = self.pol_text
        elif self.base_language == 1:
            self.text = self.eng_text
 
        arrow = pygame.image.load(f'resources/assets/arrow.png').convert_alpha()
        arrow = self.game.ui_color_change(arrow)
        arrow = pygame.transform.rotate(arrow, 90)
        self.img_rect = pygame.Rect(0, 0, self.game.max_board_size, self.game.max_board_size)
        
        if window_width > window_height:
            len = window_width - ((window_width-self.game.max_board_size)//2)
            self.continue_button = Button(
                self.window, 
                (self.game.max_board_size//10, self.game.max_board_size//10),
                (len, window_height//2),
                arrow,
                (self.game.max_board_size//20,
                self.game.max_board_size//20),
                True, 2, 25, self.game.lines_color)
        else:
            len =  window_height - ((window_height-self.game.max_board_size)//2)
            self.continue_button = Button(
                self.window,
                (self.game.max_board_size//10, self.game.max_board_size//10),
                (window_width//2, len),
                arrow,
                (self.game.max_board_size//20, self.game.max_board_size//20),
                True, 2, 25, self.game.lines_color)

        self.pol_button = Button(
            self.window, 
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            (window_width*0.91, window_height*0.96),
            pol, 
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            True, 2, 15, self.game.lines_color)
        self.eng_button = Button(
            self.window,
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            (window_width*0.97, window_height*0.96),
            eng,
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            True, 2, 15, self.game.lines_color)
        
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.continue_button.button_rect.collidepoint(pos):
                    self.playing = False
                    self.game.main_menu.playing = True
                elif self.pol_button.button_rect.collidepoint(pos):
                    self.text = self.pol_text
                elif self.eng_button.button_rect.collidepoint(pos):
                    self.text = self.eng_text
    

    def draw_screen(self):
        self.window.blit(self.game.image, self.img_rect)
        self.continue_button.draw()

        text = self.game.font.render(self.text[0], True, self.game.text_color) 
        text2 = self.game.font.render(self.text[1], True, self.game.text_color) 
        
        if self.game.config["victory_screen"]["is_victory_text_displayed"]:
            text_rect = text.get_rect(midbottom = self.continue_button.button_rect.midtop)
            self.window.blit(text, text_rect)
        
        if self.game.config["victory_screen"]["is_continue_text_displayed"]:
            text_rect2 = text2.get_rect(midtop = self.continue_button.button_rect.midbottom)
            self.window.blit(text2, text_rect2)
    
        if self.game.config["victory_screen"]["is_victory_text_displayed"] or self.game.config["victory_screen"]["is_continue_text_displayed"]:
            self.pol_button.draw()
            self.eng_button.draw()


    def victory_loop(self):
        while self.playing:
            self.window.fill(self.game.background_color)
            self.draw_screen()
            self.check_events()
            pygame.display.update()
