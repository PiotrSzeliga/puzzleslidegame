import pygame

class Button():
    def __init__(self, surface, button_size, button_location, image, image_size, border=False, thickness=-1, border_radius=0, border_color=(255,255,255)):   
        self.surface = surface
        self.button_rect = pygame.Rect((0,0),button_size)
        self.button_rect.center = button_location
        self.image = pygame.transform.scale(image, image_size)
        self.image_rect = self.image.get_rect(center=self.button_rect.center)

        self.border = border
        self.thickness = thickness
        self.border_radius = border_radius
        self.border_color = border_color

    
    def draw(self):
        self.surface.blit(self.image, self.image_rect)
        if self.border:
            pygame.draw.rect(self.surface, self.border_color, self.button_rect, self.thickness, self.border_radius)
