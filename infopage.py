import pygame
from button import Button


class InfoPage():
    def __init__(self, game):
        self.game = game
        self.playing = False
        self.page_surface = pygame.Surface((self.game.max_board_size, self.game.max_board_size))
        self.page = pygame.Rect((0,0),(self.game.max_board_size, self.game.max_board_size))
        self.base_language = self.game.config["puzzleslidegame"]["base_language"]
        
        instruction = pygame.image.load(f'resources/assets/instruction.png').convert_alpha()
        self.instruction_img = pygame.transform.scale(instruction, (self.game.max_board_size, self.game.max_board_size))
        self.instruction_img_rect = pygame.Rect(self.game.max_board_size*0.07, self.game.max_board_size*0.07, self.game.max_board_size*0.9, self.game.max_board_size*0.9)
        
        pol = pygame.image.load(f'resources/assets/pol.png').convert_alpha()
        eng = pygame.image.load(f'resources/assets/eng.png').convert_alpha()

        pol = pygame.transform.scale(pol, (self.game.max_board_size*0.07, self.game.max_board_size*0.07))
        eng = pygame.transform.scale(eng, (self.game.max_board_size*0.07, self.game.max_board_size*0.07))
        
        pol = self.game.cut_rounded_image(pol, 15)
        eng = self.game.cut_rounded_image(eng, 15)

        self.pol_button = Button(
            self.page_surface, 
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            (self.game.max_board_size*0.05, self.game.max_board_size*0.05),
            pol, 
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            True, 2, 15, self.game.lines_color)
        self.eng_button = Button(
            self.page_surface,
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            (self.game.max_board_size*0.13, self.game.max_board_size*0.05),
            eng,
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            True, 2, 15, self.game.lines_color)
        
        self.pol_text = self.game.config["info_screen"]["pol"]
        self.eng_text = self.game.config["info_screen"]["eng"]

        self.text = None
        
        if self.base_language == 0:
            self.text = self.pol_text
        elif self.base_language == 1:
            self.text = self.eng_text
    
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game.playing = False
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.pol_button.button_rect.collidepoint(pos):
                    self.text = self.pol_text
                elif self.eng_button.button_rect.collidepoint(pos):
                    self.text = self.eng_text
                elif not self.page.collidepoint(pos):
                    self.playing = False

    
    def draw_page(self):
        self.pol_button.draw()
        self.eng_button.draw()
        text = self.game.font.render(self.text[0], True, self.game.text_color) 
        text2 = self.game.font.render(self.text[1], True, self.game.text_color) 
        self.page_surface.blit(text, (self.game.max_board_size*0.1, self.game.max_board_size*0.2))
        self.page_surface.blit(text2, (self.game.max_board_size*0.1, self.game.max_board_size*0.9))
        self.page_surface.blit(self.instruction_img, self.instruction_img_rect)
    
    
    def infopageloop(self):
        while self.playing:
            self.page_surface.fill(self.game.background_color)
            pygame.draw.rect(self.page_surface, self.game.lines_color, self.page, 4)
            self.draw_page()
            self.check_events()
            self.game.window.blit(self.page_surface, (0,0))
            pygame.display.update()

