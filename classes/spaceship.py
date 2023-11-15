import pygame.transform
import os

from classes.gameobject import GameObject

X, Y = 1200, 720


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, image, spaceshipX, spaceshipY, speed, fuel, gravity_x, gravity_y):
        self.image = image
        self.spaceshipX = spaceshipX
        self.spaceshipY = spaceshipY
        self.speed = speed
        self.fuel = fuel
        self.gravity_x = gravity_x
        self.gravity_y = gravity_y
        self.rect = self.image.get_rect()

    def update(self, screen):
        if self.image != None:
            self.rect = self.image.get_rect()
            self.rect.move_ip(int(self.spaceshipX), int(self.spaceshipY))
            screen.blit(self.amountoffuel(), (40, 40))
            screen.blit(self.image, (self.spaceshipX, self.spaceshipY))
            self.gravity()
            self.amountoffuel()
            if self.fuel != 0:
                self.changePosition()

    def changePosition(self):
        keys = pygame.key.get_pressed()

        # if left arrow key is pressed
        if keys[pygame.K_LEFT] and self.spaceshipX > 0:
            self.spaceshipX -= self.speed

        # if left down key is pressed
        if keys[pygame.K_RIGHT] and self.spaceshipX < X - 60:
            # increment in y co-ordinate
            self.spaceshipX += self.speed

        # if up arrow key is pressed
        if keys[pygame.K_UP] and self.spaceshipY > 0:
            # decrement in y co-ordinate
            self.spaceshipY -= self.speed

        # if left down key is pressed
        if keys[pygame.K_DOWN] and self.spaceshipY < Y - 100:
            # increment in y co-ordinate
            self.spaceshipY += self.speed

    def amountoffuel(self):
        keys = pygame.key.get_pressed()

        # Kijkt of er nog brandstof
        if self.fuel > 0:
            if keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP]:
                self.fuel -= .5

        amount = str(self.fuel)
        amountfuel = pygame.font.Font("assets/font.ttf", 23).render('Hoeveelheid brandstof :' + amount, True, "White")
        return amountfuel

    def gravity(self):
        if self.spaceshipY < Y - 100 and self.spaceshipX < X - 60 and self.spaceshipX > 0:
            self.spaceshipY += self.gravity_y
            self.spaceshipX += self.gravity_x

    def collided_with(self, other_object):
        return self.rect.colliderect(other_object.rect)
