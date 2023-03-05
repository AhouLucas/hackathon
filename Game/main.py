import pygame as pg
from random import randint
from classes import Player, Drink
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
players_time = [0, 0]

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
    
def animate_drinks():
    for drink in Player1_drinks:
        drink.animate(screen)
            
    for drink in Player2_drinks:
        drink.animate(screen)

def write_to_screen(text, position, font_size, color):
    font = pg.font.Font(r"Fonts/font.ttf", font_size)
    text = font.render(text, True, color)
    screen.blit(text, position)

def drinks_drink(player: int):
    if player == 1:
        pass
        #for drink in Player1_drinks:
            #Player_1.drink(drink)
            #Player1_drinks.remove(drink)
            #Player1_drinks.append(Drink(0, [-80, -HEIGHT/2]) )
            #Player_1.drink(Player1_drinks[-1])
            #Player1_drinks.append(Drink(randint(0, 2), [WIDTH / 3, HEIGHT]))
        
    elif player == 2:
        # for drink in Player2_drinks:
        #     Player_2.drink(drink)
        #     Player2_drinks.remove(drink)
        Player2_drinks.append(Drink(randint(0, 2), [2 * WIDTH / 3, HEIGHT/2]))
        Player_2.drink(Player2_drinks[-1])
        # Player2_drinks.append(Drink(randint(0, 2), [2 * WIDTH / 3, HEIGHT]))

def socket_send(data):
    data = json.dumps(data)
    client.send(bytes(data, "utf-8"))

def consume_data():
    global socket_data, players_connected, mic_active
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

def count_drink_time():
    global players_time
    count1, count2 = 0, 0
    if mic_active[0]:
        players_time[0] += 1
    if mic_active[1]:
        players_time[1] += 1

    if not mic_active[0]:
        count1 = players_time[0]
        players_time[0] = 0
    if not mic_active[1]:
        count2 = players_time[1]
        players_time[1] = 0

    return count1, count2


def main():
    global running, start, count_frame
    play_music('Musics/Start Menu.mp3')
    while running:
        # Get the user keyboard inputs
        keys = pg.key.get_pressed() 

        if keys[pg.K_ESCAPE]:
            running = False
            pg.quit()  

        if start == False and all(players_connected):
            start = True
            print("All players connected")
            socket_send({"type": "game_start"})
            pg.mixer.music.stop()
            play_music('Musics/Gameplay.mp3')


        animate_background()
        # Start menu
        if not start:
            start_menu()
        # Game loop only if start is True
        else:
            Player_1.show(screen)
            Player_2.show(screen)
            count_drink_time()
            print(players_time)
            if (players_state[0] or keys[pg.K_z]) and players_time[0] > 10:
                Player1_drinks.append(Drink(0, [-80, -HEIGHT/2]) )
                Player_1.drink(Player1_drinks[-1])

            elif (players_state[1] or keys[pg.K_m]) and players_time[1] > 10:
                Player2_drinks.append(Drink(0, [-80, -HEIGHT/2]) )
                Player_2.drink(Player2_drinks[-1])

        count_frame += 1
        animate_drinks()
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