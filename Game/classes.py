import pygame as pg
from colorsys import hsv_to_rgb

class Gauge:
    def __init__(self, position, size, color, max_value):
        self.position = position
        self.size = size
        self.color = color
        self.max_value = max_value
        self.value = 0

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
    vomitingKey = 90
    initKey = 70
    normalKey = 40
    armKey = 20
    drinkingKey = 0

    def __init__(self, position, pseudo, image=None, victory_scream=None):
        self.position = position
        self.pseudo = pseudo
        self.image = image
        self.dead = False
        self.rect = pg.Rect(position, (50, 100))
        self.drunkness_level = Gauge((position[0]-100, position[1]), (50, 200), (0, 255, 0), 1000)
        self.animationStatus = Player.initKey
        self.drinkInHand = None

    def show(self, screen):
        if Player.initKey < self.animationStatus <= Player.vomitingKey:
            print(self.drinkInHand)
            if self.drinkInHand: self.drinkInHand.show(screen)
            
            img = pg.image.load("Images/sprites/vomit.png")
            img = pg.transform.scale(img, (650, 500))
            screen.blit(img, (self.position[0] - 150, self.position[1] + 74))
            
            self.animationStatus -= 1
        
        if Player.normalKey <= self.animationStatus <= Player.initKey:
            
            img = pg.image.load("Images/sprites/normal.png")
            img = pg.transform.scale(img, (650, 500))
            screen.blit(img, (self.position[0] - 150, self.position[1] + 74))
        
            if self.animationStatus < Player.initKey: self.animationStatus -= 1
            
        elif Player.armKey <= self.animationStatus < Player.normalKey:
            
            img = pg.image.load("Images/sprites/normal.png")
            img = pg.transform.scale(img, (650, 500))
            screen.blit(img, (self.position[0] - 150, self.position[1] + 74))
            
            img = pg.image.load("Images/sprites/arm.png")
            img = pg.transform.scale(img, (650, 500))
            screen.blit(img, (self.position[0] - 150, self.position[1] + 74))
            
            self.animationStatus -= 1
            
        if self.animationStatus < Player.armKey:
            self.drinkInHand.img = pg.transform.flip(self.drinkInHand.img, False, True)
            
            img = pg.image.load("Images/sprites/drinking.png")
            img = pg.transform.scale(img, (650, 500))
            screen.blit(img, (self.position[0] - 150, self.position[1] + 74))

            self.animationStatus -= 1
            
        if self.animationStatus == Player.drinkingKey:
            self.animationStatus = Player.initKey
        
        self.drunkness_level.show(screen)

    def drink(self, drink):
        self.drunkness_level.add(drink.type.alcohol)
        self.animationStatus = Player.initKey - 1
        self.drinkInHand = drink
        
    def vomit(self):
        self.animationStatus = Player.vomitingKey
        self.drunkness_level.add(-50)

class DrinkType:
    def __init__(self, image, alcohol):
        self.image = image
        self.alcohol = alcohol

class Drink:
    TYPE = (
        DrinkType(r"Images/sprites/bottle.png", 10),
        DrinkType(r"Images/sprites/gordon.png", 20),
        DrinkType(r"Images/sprites/big-glass.png", 30)
    )
    
    def __init__(self, type, position):
        self.type = Drink.TYPE[type]
        self.position = position
        self.img = pg.image.load(self.type.image)
        self.drunk = False

    def show(self, screen):        
        self.img = pg.transform.scale(self.img, (500, 500))
        screen.blit(self.img, (self.position[0] - 150, self.position[1]))
        
    def animate(self, screen):
        if self.position[1] > 3 * screen.get_size()[1] // 5:
            self.position[1] -= 15
        self.show(screen)
 