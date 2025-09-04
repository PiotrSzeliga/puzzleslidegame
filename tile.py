import pygame


class Tile():
    def __init__(self, game, id, position):
        self.game = game
        self.id = id
        self.blank = True if self.id == self.game.difficulty**2 else False
        self.clicked = False

        img_rect_x = (self.id-1)%self.game.difficulty
        img_rect_y = (self.id-1)//self.game.difficulty
        self.img_rect = pygame.Rect(
            img_rect_x * self.game.tile_size,
            img_rect_y * self.game.tile_size,
            self.game.tile_size,
            self.game.tile_size
        )

        self.pos_rect = pygame.Rect( 
            position,
            (self.game.tile_size, self.game.tile_size)
            )


    def draw(self):
        if not self.blank:
            self.game.window.blit(self.game.image, self.pos_rect, self.img_rect)  
            
            text = self.game.font.render(str(self.id), True, (255, 255, 255), (0, 0, 0))  
            self.game.window.blit(text, self.pos_rect.topleft, None, pygame.BLEND_SUB)
        # else:
        #     pygame.draw.rect(self.game.window, (0,0,255), self.pos_rect)