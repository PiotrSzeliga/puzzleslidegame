import pygame


class Tile():
    def __init__(self, game, id, position, draw_id):
        self.game = game
        self.id = id
        self.blank = True if self.id == self.game.difficulty**2 else False
        self.clicked = False
        self.draw_id = draw_id

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
            if self.draw_id:
                text = self.game.font.render(str(self.id), True, self.game.config["tiles"]["id_display_color"])  
                self.game.window.blit(text, self.pos_rect.topleft, None)
