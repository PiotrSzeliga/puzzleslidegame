import pygame


class VictoryScreen():
    def __init__(self, game):
        self.game = game
        self.playing = False
        self.window = self.game.window
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w

        
        self.img_rect = pygame.Rect(0, 0, self.game.max_board_size, self.game.max_board_size)
        self.continue_button_rect = pygame.Rect(0, 0, self.game.max_board_size//10, self.game.max_board_size//10)
        if window_width > window_height:
            len = window_width - ((window_width-self.game.max_board_size)//2)
            self.continue_button_rect.center = (len , window_height//2)
        else:
            len =  window_height - ((window_height-self.game.max_board_size)//2)
            self.continue_button_rect.center = (window_width//2, len)
    

        arrow = pygame.image.load(f'resources/assets/arrow.png').convert_alpha()
        arrow = pygame.transform.scale(arrow, (self.game.max_board_size//20, self.game.max_board_size//20))
        self.arrow = pygame.transform.rotate(arrow, 90)
        self.arrow_rect = arrow.get_rect(center = self.continue_button_rect.center)
    
    
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
                if self.continue_button_rect.collidepoint(pos):
                    self.playing = False
                    self.game.main_menu.playing = True
    
    
    def draw_screen(self):
        self.window.blit(self.game.image, self.img_rect)
        pygame.draw.rect(self.window, (0, 0, 0), self.continue_button_rect, 2, 30)
        self.window.blit(self.arrow, self.arrow_rect)

    
    def victory_loop(self):
        while self.playing:
            self.window.fill((255, 255, 255))
            self.draw_screen()
            self.check_events()
            pygame.display.update()
