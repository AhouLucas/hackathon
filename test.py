from drink import Drink
import pygame

WIDTH, HEIGHT = 800, 600

gameObjects = [
    Drink(2, (300, 200)),
    Drink(1, (100, 100))
]

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
while running: 
    screen.fill((200, 200, 200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for gameObject in gameObjects:
        gameObject.show(screen)
    
    pygame.display.update()
    
pygame.quit()