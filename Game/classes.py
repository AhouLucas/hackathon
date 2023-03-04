import pygame as pg


class Gauge:
    def __init__(self, position, size, color, max_value):
        self.position = position
        self.size = size
        self.color = color
        self.max_value = max_value
        self.value = 50

    def show(self, screen):
        pg.draw.rect(screen, self.color, (self.position, (self.size[0], self.size[1] * self.value / self.max_value)), border_radius=self.size[0])

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
        self.drunkness_level = Gauge((position[0]-100, position[1]), (50, 200), (0, 255, 0), 100)
        

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
        DrinkType(r"Images/drink0.png", 10),
        DrinkType(r"Images/drink1.png", 20),
        DrinkType(r"Images/drink2.png", 30)
    )
    
    def __init__(self, type, position):
        self.type = Drink.TYPE[type]
        self.position = position
        self.img = pg.image.load(self.type.image)
        self.drunk = False

    def show(self, screen):
        screen.blit(self.img, self.position)
        
    def animate(self, screen):
        if self.position[1] > 3 * screen.get_size()[1] // 4:
            self.position[1] -= 5
        self.show(screen)
            