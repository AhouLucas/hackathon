import pygame as pg
from random import randint
from classes import Player, Drink

#### Pygame Initialisation ####

pg.font.init()

pg.init()
pg.display.set_caption("Hackathon : Edition 24H !")
clock = pg.time.Clock()
ASPECT_RATIO = 16/9
WIDTH = 1000; HEIGHT = WIDTH/ASPECT_RATIO
screen = pg.display.set_mode((WIDTH, HEIGHT))

###############################


#### Variables ####
running = True
# Set this to True to start the game
start = False

Player_1, Player_2 = Player((WIDTH/3, HEIGHT/3), "Player 1"), Player((2*WIDTH/3, HEIGHT/3), "Player 2")
Player1_drinks = []
Player2_drinks = []
###################

#### Functions ####
def spawn_drink(player: int):
    """Adds a drink to the players's drink list.

    Args:
        player (int): number of the player who will receive the drink.
    """
    if player == 1:
        Player1_drinks.append(Drink(randint(0, 2), [WIDTH / 3, HEIGHT]))
    elif player == 2:
        Player2_drinks.append(Drink(randint(0, 2), [2 * WIDTH / 3, HEIGHT]))

def play_music(filename):
    pg.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pg.init()
    pg.mixer.init()
    pg.mixer.music.load(filename)
    pg.mixer.music.play(loops=-1)

def start_menu():
    """Displays the start menu.
    """
    global start
    screen.fill((255, 0, 0))
    clock.tick(60)
    pg.display.flip()

def animate_drinks():
    for drink in Player1_drinks:
        if drink.drunk: Player1_drinks.remove(drink)
        drink.animate(screen)
            
    for drink in Player2_drinks:
        if drink.drunk: Player1_drinks.remove(drink)
        drink.animate(screen)

def write_to_screen(text, position, font_size, color):
    font = pg.font.Font(r"Fonts/font.ttf", font_size)
    text = font.render(text, True, color)
    screen.blit(text, position)

spawn_drink(1)
spawn_drink(2)

def main():
    global running, start
    play_music('Musics/Start Menu.mp3')
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif start == False and event.type == pg.MOUSEBUTTONDOWN:
                start = True
                pg.mixer.music.stop()
                play_music('Musics/Gameplay.mp3')

        
        # Game loop only if start is True
        # Start menu
        if not start:
            start_menu()
        else:
            screen.fill((255, 255, 255))
            Player_1.show(screen)
            Player_2.show(screen)
            animate_drinks()
            pg.display.flip()
            clock.tick(60)
            

if __name__ == "__main__":
    main()  