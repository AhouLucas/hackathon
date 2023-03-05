import pygame as pg
from random import randint
from classes import Player
from controller import controller_thread
from network import socket_read
import threading, sys, time
import socket
import json

# from Controller import controller

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
Player_1 = Player((-400, 0),(WIDTH, HEIGHT), "Player 1")
Player_2 = Player((400, 0), (WIDTH, HEIGHT), "Player 2")
Player1_drinks = []
Player2_drinks = []
players_state = [False, False]
players_connected = [False, False]

# Images
background_1 = pg.image.load("Images/sprites/background1.png")
background_2 = pg.image.load("Images/sprites/background2.png")
background_1 = pg.transform.scale(background_1, (WIDTH, HEIGHT))
background_2 = pg.transform.scale(background_2, (WIDTH, HEIGHT))
background = [background_1, background_2]

# Newtork
hostname = "146.190.125.98"
port = 8081
client = socket.socket()
client.connect((hostname, port))
socket_data = []
###################

#### Functions ####

def spawn_drink(player: int):
    """Adds a drink to the players's drink list.

    Args:
        player (int): number of the player who will receive the drink.
    """
    if player == 1:
        Player1_drinks.append(Drink(randint(0, 2), [0, 0]))
    elif player == 2:
        Player2_drinks.append(Drink(randint(0, 2), [0,0]))

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
    global count_frame, background

    if count_frame % 30 == 0:
        background[0], background[1] = background[1], background[0]
    elif count_frame % 60 == 0:
        background[0], background[1] = background[1], background[0]

    screen.blit(background[0], (0,0))
    

def write_to_screen(text, position, font_size, color):
    font = pg.font.Font(r"Fonts/font.ttf", font_size)
    text = font.render(text, True, color)
    screen.blit(text, position)

def socket_send(data):
    data = json.dumps(data)
    client.send(bytes(data, "utf-8"))

def consume_data():
    global socket_data
    while len(socket_data):
        data = socket_data.pop(0)
        if data["type"] == "player_connected":
            players_connected[data["player"]] = True
        elif data["type"] == "player_disconnected":
            players_connected[data["player"]] = False

def main():
    global running, start, count_frame
    play_music('Musics/Start Menu.mp3')
    while running:
        # Get the user keyboard inputs
        keys = pg.key.get_pressed() 

        # Check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()   
            elif start == False and all(players_connected):
                start = True
                socket_send({"type": "game_start"})
                pg.mixer.music.stop()
                play_music('Musics/Gameplay.mp3')


        animate_background()
        start = True

        # Start menu
        if not start:
            start_menu()
        # Game loop only if start is True
        else:
            
            if keys[pg.K_a]:
                Player_1.normal(screen)
                Player_1.arm(screen)
            elif keys[pg.K_b]:
                Player_1.drinking(screen)
            else:
                Player_1.normal(screen)


            if keys[pg.K_a]:
                Player_2.normal(screen)
                Player_2.arm(screen)
            elif keys[pg.K_b]:
                Player_2.drinking(screen)
            else:
                Player_2.normal(screen)

                


        count_frame += 1
        consume_data()
        pg.display.update()
        clock.tick(10)
            

if __name__ == "__main__":

    #Threads
    movement_control_thread = threading.Thread(target=controller_thread, args=(players_state,))
    socket_read_thread = threading.Thread(target=socket_read, args=(client, socket_data))
    movement_control_thread.daemon = True
    socket_read_thread.daemon = True
    movement_control_thread.start()
    socket_read_thread.start()

    main()  