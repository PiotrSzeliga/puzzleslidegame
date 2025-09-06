import pygame
from button import Button


class InfoPage():
    def __init__(self, game):
        self.game = game
        self.playing = False
        self.page_surface = pygame.Surface((self.game.max_board_size, self.game.max_board_size))
        self.page = pygame.Rect((0,0),(self.game.max_board_size, self.game.max_board_size))
        self.base_language = 0
        
        instruction = pygame.image.load(f'resources/assets/instruction.png').convert_alpha()
        self.instruction_img = pygame.transform.scale(instruction, (self.game.max_board_size, self.game.max_board_size))
        self.instruction_img_rect = pygame.Rect(self.game.max_board_size*0.07, self.game.max_board_size*0.07, self.game.max_board_size*0.9, self.game.max_board_size*0.9)
        
        pol = pygame.image.load(f'resources/assets/pol.png').convert_alpha()
        eng = pygame.image.load(f'resources/assets/eng.png').convert_alpha()

        pol = pygame.transform.scale(pol, (self.game.max_board_size*0.1, self.game.max_board_size*0.1))
        eng = pygame.transform.scale(eng, (self.game.max_board_size*0.1, self.game.max_board_size*0.1))
        
        pol = self.game.cut_rounded_image(pol, 15)
        eng = self.game.cut_rounded_image(eng, 15)

        self.pol_button = Button(
            self.page_surface, 
            (self.game.max_board_size//8, self.game.max_board_size//8),
            (self.game.max_board_size*0.07, self.game.max_board_size*0.07),
            pol, 
            (self.game.max_board_size//8, self.game.max_board_size//8),
            True, 2, 15, (0,0,0))
        self.eng_button = Button(
            self.page_surface,
            (self.game.max_board_size//8, self.game.max_board_size//8),
            (self.game.max_board_size*0.20, self.game.max_board_size*0.07),
            eng,
            (self.game.max_board_size//8, self.game.max_board_size//8),
            True, 2, 15, (0,0,0))

        self.pol_text = "Celem łamigłówki jest stworzenie obrazu poprzez ułożenie kafelków w odpowiedniej kolejności"
        self.pol_text2 = "Zmień stan planszy przesuwając kafelki w pustą przestrzeń układanki"
        
        self.eng_text = "The goal of the puzzle is to complete the picture by rearranging tiles in a correct order"
        self.eng_text2 = "Change the state of the board by sliding tiles into an empty space"
        
        self.text = None
        self.text2 = None
        
        if self.base_language == 0:
            self.text = self.pol_text
            self.text2 = self.pol_text2
            # = self.game.font.render(str(self.id), True, (0, 0, 0), (255, 255, 255))  
        elif self.base_language == 1:
            self.text = self.eng_text
            self.text2 = self.eng_text2
        

        
    
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
                    self.text2 = self.pol_text2
                elif self.eng_button.button_rect.collidepoint(pos):
                    self.text = self.eng_text
                    self.text2 = self.eng_text2
                elif not self.page.collidepoint(pos):
                    self.playing = False

    
    def draw_page(self):
        self.pol_button.draw()
        self.eng_button.draw()
        text = self.game.font.render(self.text, True, (0, 0, 0)) 
        text2 = self.game.font.render(self.text2, True, (0, 0, 0)) 
        self.page_surface.blit(text, (self.game.max_board_size*0.1, self.game.max_board_size*0.2))
        self.page_surface.blit(text2, (self.game.max_board_size*0.1, self.game.max_board_size*0.9))
        self.page_surface.blit(self.instruction_img, self.instruction_img_rect)
    
    
    def infopageloop(self):
        while self.playing:
            self.page_surface.fill((255,255,255))
            pygame.draw.rect(self.page_surface, (0,0,0), self.page, 4)
            self.draw_page()
            self.check_events()
            self.game.window.blit(self.page_surface, (0,0))
            pygame.display.update()

