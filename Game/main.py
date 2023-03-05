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
mic_active = [False, False]
player_time = [0, 0]
player1_hold_beer = False
player2_hold_beer = False
player1_drinking = False
player2_drinking = False

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
        
        elif data["type"] == "mic_high":
            mic_active[data["player"]] = True
        
        elif data["type"] == "mic_low":
            mic_active[data["player"]] = False

def count_time_drinking():
    count1, count2 = 0, 0
    if mic_active[0]:
        player_time[0] += 1
    if mic_active[1]:
        player_time[1] += 1

    if not mic_active[0]:
        count1 = player_time[0]
        player_time[0] = 0
    if not mic_active[1]:
        count2 = player_time[1]
        player_time[1] = 0

    return count1, count2

def main():
    global running, start, count_frame, player1_hold_beer, player2_hold_beer, socket_data, players_state, player1_drinking, player2_drinking
    play_music('Musics/Start Menu.mp3')
    while running:
        # Check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()   
        
        if start == False and all(players_connected):
            start = True
            socket_send({"type": "game_start"})
            pg.mixer.music.stop()
            play_music('Musics/Gameplay.mp3')


        animate_background()

        # Start menu
        if not start:
            start_menu()
        # Game loop only if start is True
        else:
            
            count_time_drinking()
            if players_state[0] and not player1_hold_beer:
                player1_hold_beer = True

            elif not players_state[0] and player1_hold_beer and not player1_drinking:
                player1_drinking = True
            
            elif player_time[0] > 3 and player1_hold_beer and player1_drinking:
                player1_hold_beer = False
                player1_drinking = False


            if players_state[1] and not player2_hold_beer:
                player2_hold_beer = True

            elif not players_state[1] and player2_hold_beer:
                player2_drinking = True
            elif player_time[1] > 3 and player2_hold_beer:
                player2_hold_beer = False
                player2_drinking = False


        if not player1_hold_beer and not player1_drinking:
            Player_1.normal(screen)
        elif player1_hold_beer and not player1_drinking:
            Player_1.normal(screen)
            Player_1.arm(screen)
        elif player1_drinking and player1_hold_beer:
            Player_1.drinking(screen)
    
        if not player2_hold_beer and not player2_drinking:
            Player_2.normal(screen)
        elif player2_hold_beer and not player2_drinking:
            Player_2.normal(screen)
            Player_2.arm(screen)
        elif player2_drinking and player2_hold_beer:
            Player_2.drinking(screen)


        count_frame += 1
        consume_data()
        pg.display.update()
        clock.tick(60)
            

if __name__ == "__main__":

    #Threads
    movement_control_thread = threading.Thread(target=controller_thread, args=(players_state,), daemon=True)
    socket_read_thread = threading.Thread(target=socket_read, args=(client, socket_data), daemon=True)
    movement_control_thread.start()
    socket_read_thread.start()

    main()  