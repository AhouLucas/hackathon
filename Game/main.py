import pygame as pg
from random import randint
from classes import Player, Drink

#### Pygame Initialisation ####

pg.font.init()

pg.init()
pg.display.set_caption("Hackathon : Edition 24H !")
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

###############################


#### Variables ####

# Game
running = True
start = False
count_frame = 0 # Used to get the frame number for timing purposes

# Players
Player_1, Player_2 = Player((WIDTH/3, HEIGHT/3), "Player 1"), Player((2*WIDTH/3, HEIGHT/3), "Player 2")
Player1_drinks = []
Player2_drinks = []

# Images
background_1 = pg.image.load("Images/background/background1-large.png")
background_2 = pg.image.load("Images/background/background2-large.png")
background_1 = pg.transform.scale(background_1, (WIDTH, HEIGHT))
background_2 = pg.transform.scale(background_2, (WIDTH, HEIGHT))
background = [background_1, background_2]
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
    pass

def animate_background():
    """Animates the background by alternating between two images.
    """
    global count_frame
    first_image = True
    if count_frame % 60 == 0:
        first_image = True
    elif count_frame % 60 == 30:
        first_image = False
    
    if first_image:
        screen.blit(background[0], (0,0))
    else:
        screen.blit(background[1], (0,0))

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
    global running, start, count_frame
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


        screen.fill((0,0,0))
        animate_background()
        
        # Start menu
        if not start:
            start_menu()
        # Game loop only if start is True
        else:
            Player_1.show(screen)
            Player_2.show(screen)

        count_frame += 1
        animate_drinks()
        pg.display.update()
        clock.tick(60)
            

if __name__ == "__main__":
    main()  