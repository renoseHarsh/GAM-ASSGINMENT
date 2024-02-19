import pygame

class Trap:
    def __init__(self, pos):
        self.position = pos

class Player:
    def __init__(self, num):
        self.num = num
        self.name = "Player " + str(num)
        self.traps = 0
        self.position = 1
        self.set_color()
        self.trapped = False

    def set_color(self):
        if self.num == 1:
            self.color = pygame.Color(0, 255, 0)
        elif self.num == 2:
            self.color = pygame.Color(255, 0, 0)
        elif self.num == 3:
            self.color = pygame.Color(0, 0, 255)
        else:
            self.color = pygame.Color(0, 255, 255)

    def move(self, roll):
        if (self.trapped) and roll > 0 and roll !=6:
            self.trapped = False
            return
        if self.position + roll < 1:
            self.position = 1
        elif self.position + roll >= 100:
            self.position = 100
            return f"{self.num}"
        elif self.position + roll == 25:
            self.position = 50
        elif self.position + roll == 34:
            self.position = 1
        else:
            self.position += roll
            if (self.position == 10):
                return "B"
            if roll == 1:
                self.traps += 1
        return "C"
    
    def trap_available(self):
        if self.traps > 0:
            return True
        return False



class Button:
    def __init__(self, text, position, size=(100, 50), color=(0, 255, 0), text_color=(0, 0, 0)):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(position, size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
