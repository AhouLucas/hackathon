import pygame as pg

class Player:
    def __init__(self, position, pseudo, image=None, victory_scream=None):
        self.pseudo = pseudo
        self.image = image
        self.drunkness_level = 0
        self.dead = False
        self.rect = pg.Rect(position, (50, 100))

    def show(self, surface):
        pg.draw.rect(surface, (255, 0,0), self.rect)
