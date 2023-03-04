import pygame as pg


class Gauge:
    def __init__(self, position, size, color, max_value):
        self.position = position
        self.size = size
        self.color = color
        self.max_value = max_value
        self.value = 0

    def show(self, screen):
        pg.draw.rect(screen, self.color, (self.position, (self.size[0], self.size[1] * self.value / self.max_value)))

    def add(self, value):
        self.value += value
        if self.value > self.max_value:
            self.value = self.max_value

    def update(self, value):
        self.value = value

    def is_empty(self):
        return self.value <= 0

class Player:
    def __init__(self, position, pseudo, image=None, victory_scream=None):
        self.pseudo = pseudo
        self.image = image
        self.dead = False
        self.rect = pg.Rect(position, (50, 100))
        self.drunkness_level = Gauge((0, 0), (50, 100), (0, 255, 0), 100)
        

    def show(self, screen):
        pg.draw.rect(screen, (255, 0,0), self.rect)
        self.drunkness_level.show(screen)

    def drink(self, drink):
        self.drunkness_level.add(drink.type.alcohol)


class DrinkType:
    def __init__(self, image, alcohol):
        self.image = image
        self.alcohol = alcohol

class Drink:
    TYPE = (
        DrinkType(r"images/drink0.png", 10),
        DrinkType(r"images/drink1.png", 20),
        DrinkType(r"images/drink2.png", 30)
    )
    
    def __init__(self, type, position):
        self.type = Drink.TYPE[type]
        self.position = position
        
        self.drunk = False

    def show(self, screen):
        img = pg.image.load(self.type.image)
        screen.blit(img, self.position)
        
    def animate(self, screen):
        if self.position[1] > screen.get_size()[1] // 4:
            self.show(screen)
            self.position[1] -= 1
            