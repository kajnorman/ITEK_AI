import pygame, sys, random, math
from pygame.locals import *
import pygame_widgets
from pygame_widgets.slider import Slider
import random
import numpy as np
import tensorflow as tf
import keras


def init():
    global model, slider, acc, speed, angle, screen, red, white, green, blue, black, bg, clock, sound1, x, normalized_x
    pygame.init()
    screen = pygame.display.set_mode((1500, 500))
    slider = Slider(screen, 100, 30, 800, 20, min=0, max=99, step=1)
    pygame.display.set_caption("Ball on a Beam")
    sound1 = pygame.mixer.Sound("womp.wav")
    clock = pygame.time.Clock()
    speed = 1
    acc = 0
    x = 500
    normalized_x = 5.0
    angle = 0
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    bg = (127, 127, 127)

    # Indlæs neuralt netværk (håndter fejl, hvis filen mangler)
    try:
        model = keras.models.load_model('old_file.keras')
    except Exception as e:
        print(f"Fejl ved indlæsning af model: {e}")
        model = None


def run():
    global model, slider, acc, speed, angle, screen, red, white, green, blue, black, bg, x, normalized_x, clock, sound1

    # Beregn acceleration og hastighed
    acc = angle / 30
    nois = 1 * (random.random() - 0.5)
    speed = speed + acc + nois
    x = x + speed
    normalized_x = x / 100

    # Sæt bjælkens vinkel fra slideren
    angle = slider.getValue() - 50

    ###################  TRÆNINGSDATA
    ##############denne linje kan generere CSV-data på konsol.
    ##############kopier dem og læg dem ind i en CSV-fil
    #  print(normalized_x, ',', angle, ',', speed)



    # Begrænsning: Hvis bolden rammer enderne, skal den hoppe tilbage
    if x < 70 or x > 1400:
        speed = -speed
        sound1.play()

    # Tegn baggrund
    screen.fill(bg)

    # Beregn bjælkens rotation
    beam_length = 1300
    center_x, center_y = 750, 250  # Midten af bjælken
    angle_rad = math.radians(angle)  # Konverter grader til radianer

    # Beregn endepunkter for den roterede bjælke
    x1 = center_x - (beam_length // 2) * math.cos(angle_rad)
    y1 = center_y - (beam_length // 2) * math.sin(angle_rad)
    x2 = center_x + (beam_length // 2) * math.cos(angle_rad)
    y2 = center_y + (beam_length // 2) * math.sin(angle_rad)


    pygame.draw.circle(screen, green, [750, 300], 50)  # support
    pygame.draw.rect(screen, green, pygame.Rect(650, 300, 200, 100), 49)  # support

    # Tegn den roterede bjælke
    pygame.draw.line(screen, red, (x1, y1), (x2, y2), 10)

    # Flyt bolden i forhold til bjælkens hældning
    ball_x = center_x + (x - 750) * math.cos(angle_rad)
    ball_y = center_y + (x - 750) * math.sin(angle_rad) - 50 #-80
    pygame.draw.circle(screen, blue, [int(ball_x), int(ball_y)], 50)

    # Tekst med bjælkens vinkel
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'Beam Angle: {angle} deg', True, green, blue)
    textRect = text.get_rect()
    textRect.center = (400, 400)
    screen.blit(text, textRect)

    #########Ved generering at træningsdata kan følgende måske bruges
    '''
    if (x < 700) and (x > 500) and (speed < 0.5) and (speed > -0.5):
        n = 0
        x = 100 + 1000 * random.random()
        speed = 5 * (random.random() - 0.5)
    '''





    # Håndter lukning af programmet
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame_widgets.update(events)
    pygame.display.update()
    clock.tick(30)  # Kør ved 30 FPS

