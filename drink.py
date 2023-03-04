import pygame

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

    def show(self, screen):
        img = pygame.image.load(self.type.image)
        screen.blit(img, self.position)

