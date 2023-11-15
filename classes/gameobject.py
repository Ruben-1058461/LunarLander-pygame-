import os
import random
import pygame

X, Y = 1200, 720


class GameObject:
    def __init__(self, x, y, x_speed, y_speed, name, current_path=os.path.abspath(os.curdir)):
        self.image = pygame.image.load(os.path.join(current_path, "assets\\" + name + ".png"))
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.name = name
        self.rect = self.image.get_rect()

    def move(self):
        # Verander de x en de y waarde van het object
        if self.x >= X:
            self.x = 0
            self.y = random.randrange(150, Y - 230)
        if self.x_speed != 0:
            self.x += self.x_speed


    def display(self, screen):
        if self.x_speed != 0:
            self.move()
        self.rect = self.image.get_rect()
        self.rect.move_ip(int(self.x), int(self.y))
        screen.blit(self.image, (int(self.x), int(self.y)))

    def collided_with(self, other_object):
        return self.rect.colliderect(other_object.rect)