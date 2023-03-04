import pygame as pg
from classes import Player

#### Pygame Initialisation ####

pg.init()
pg.display.set_caption("Hackathon : Edition 24H !")
ASPECT_RATIO = 16/9
WIDTH = 1000; HEIGHT = WIDTH/ASPECT_RATIO
screen = pg.display.set_mode((WIDTH, HEIGHT))

###############################

Player_1, Player_2 = Player((WIDTH/3, HEIGHT/3), "Player 1"), Player((2*WIDTH/3, HEIGHT/3), "Player 2")
Player1_drinks = []
Player2_drinks = []

#### Functions ####
def spawn_drink(player: int):
    """Adds a drink to the players's drink list.

    Args:
        player (int): number of the player who will receive the drink.
    """
    if player == 1:
        Player1_drinks.append(Drink())
    elif player == 2:
        Player2_drinks.append(Drink())


def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        screen.fill((255, 255, 255))
        Player_1.show(screen)
        Player_2.show(screen)
        pg.display.flip()
            

if __name__ == "__main__":
    main()  