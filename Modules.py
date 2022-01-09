from pygame import Rect, draw, Surface, mouse, transform, SRCALPHA
from Constants import FONT

class Button:
    def __init__(self, display, position, size, text, scale):
        self.display = display
        self.x, self.y = position
        self.width, self.height = size
        self.text = text
        self.over = False
        self.scale = 1
        self.widthScale, self.heightScale = scale

        self.rect = Rect(position, size)
        self.image = Surface(size, SRCALPHA)
        self.image.fill((100, 100, 100, 200))
        self.textImage = FONT.render(self.text, 0, (0, 0, 0))

    def Update(self):
        self.rect.width, self.rect.height = int(self.width * self.scale), int(self.height * self.scale)
        self.relHeight = self.y - (self.rect.height - self.height) / 2
        self.rect.y = self.relHeight
        self.display.blit(transform.scale(self.image, (self.rect.width, self.rect.height)), (self.x, self.relHeight))
        self.StextImage = transform.scale(self.textImage, (int(self.textImage.get_width() * self.scale), int(self.textImage.get_height() * self.scale)))
        self.display.blit(self.StextImage, self.StextImage.get_rect(center=(self.x + self.rect.width / 2, self.relHeight + self.rect.height / 2)))
        draw.rect(self.display, (0, 0, 0), self.rect, 5)
        mousepos = mouse.get_pos()
        if self.rect.collidepoint((int(mousepos[0]*self.widthScale), int(mousepos[1]*self.heightScale))):
            if self.scale < 1.5: self.scale += 0.1; self.over = True
        else:
            if self.scale > 1: self.scale -= 0.1; self.over = False