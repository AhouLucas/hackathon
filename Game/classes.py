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
    armKey = 30
    drinkingKey = 20

    hOffset = -400
    vOffset = -50

    def __init__(self, position, pseudo, image=None, victory_scream=None):
        self.position = position
        self.pseudo = pseudo
        self.image = image
        self.dead = False
        self.width, self.height = 850, 650
        self.rect = pg.Rect(position, (self.width, self.height))
        self.drunkness_level = Gauge((position[0]-200, position[1]-50), (50, 200), (0, 255, 0), 1000)
        self.animationStatus = Player.initKey
        self.drinkInHand = None
        self.lastAddedDrink = 0
        
        self.images = {
            "vomit": pg.transform.scale(pg.image.load("Images/sprites/vomit.png"), (self.width, self.height)),
            "normal": pg.transform.scale(pg.image.load("Images/sprites/happy.png"), (self.width, self.height)),
            "arm": pg.transform.scale(pg.image.load("Images/sprites/arm.png"), (self.width, self.height)),
            "drinking": pg.transform.scale(pg.image.load("Images/sprites/drinking.png"), (self.width, self.height)),
        }

    def show(self, screen):
        if Player.initKey < self.animationStatus <= Player.vomitingKey:
            img = self.images["vomit"]
            screen.blit(img, (self.position[0] + Player.hOffset, self.position[1] + Player.vOffset))
            
            self.animationStatus -= 1
        
        if Player.normalKey <= self.animationStatus <= Player.initKey:
            img = self.images["normal"]
            screen.blit(img, (self.position[0] + Player.hOffset, self.position[1] + Player.vOffset))
        
            if self.animationStatus < Player.initKey: self.animationStatus -= 1
            
        if Player.armKey <= self.animationStatus < Player.normalKey:
            img = self.images["normal"]
            screen.blit(img, (self.position[0] + Player.hOffset, self.position[1] + Player.vOffset))
            
            self.drinkInHand.position[1] -= 70
            self.drinkInHand.show(screen)
            self.drinkInHand.position[1] += 70
            
            img = self.images["arm"]
            screen.blit(img, (self.position[0] + Player.hOffset + 10, self.position[1] + 100))
            
            self.animationStatus -= 1
            
        if self.animationStatus < Player.armKey:
            img = self.images["drinking"]
            screen.blit(img, (self.position[0] + Player.hOffset - 25, self.position[1] - 62))

            self.drinkInHand.position = (300, 300)
            self.drinkInHand.show(screen)
            # self.drinkInHand.position[1] += 100
            
            self.animationStatus -= 1
            
        if self.animationStatus == Player.drinkingKey:
            self.drunkness_level.add(self.drinkInHand.type.alcohol)
            self.animationStatus = Player.initKey
        
        self.drunkness_level.show(screen)

    def drink(self, drink):
        # self.drunkness_level.add(drink.type.alcohol)
        self.animationStatus = Player.initKey - 1
        # self.drinkInHand = Drink(Drink.TYPE.index(drink.type), drink.position)
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
        DrinkType(r"Images/sprites/small glass.png", 10),
        DrinkType(r"Images/sprites/bottle.png", 20),
        DrinkType(r"Images/sprites/gordon.png", 30)
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
 