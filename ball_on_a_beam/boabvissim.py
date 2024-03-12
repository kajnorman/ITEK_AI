import pygame, sys
from pygame.locals import *
import pygame_widgets
from pygame_widgets.slider import Slider
import random

import numpy as np
import tensorflow as tf
import keras


def init():
    global model,slider,acc,speed,angle,text,textRect,screen,red,white,green,blue,black,bg,Press,downwards,x,clock,sound1,sound2,sound3,b1,b2,es
    pygame.init()
    screen = pygame.display.set_mode((1500, 500))
    slider = Slider(screen, 100, 30, 800, 20, min=0, max=99, step=1)
    pygame.display.set_caption("Ball on a Beam")
    sound1 =  pygame.mixer.Sound("womp.wav")
    clock = pygame.time.Clock()
    speed = 1
    acc=0
    x = 500
    angle = 0
    done = False
    white=(255,255,255)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    black = (0,0,0)
    bg = (127,127,127)
    model = keras.models.load_model('file2.keras')


def run():
     global model,slider,acc,speed,angle,text,textRect,screen, red, white, green,blue,black, bg, Press, downwards, x,clock,sound1,sound2,sound3,b1,b2,es



#endten bruger man slideren#####################################
     #angle = (slider.getValue()-50)     ####################################    <<<<<<<<<<<<<<<<<<<<===============================   Set angle



#eller også bruger man det neurale netværk
     angle = model.predict([(float(x),speed)],verbose=0)
     angle = angle[0][0]



##Dynamiske ligninger som giver bolden accelleration hastighed og position.##########################
     acc = angle/30
     nois = 1 * (random.random()-0.5)
     speed=speed+acc  + nois # støj kan lægges til +
     x = x + speed


##############disse linjer kan generere CSV-data på konsol.
#     print(x, ',', angle)      ##############<<<<<<<<<<<<<<<<<<<<<<<<<   CSV
#     print(x, ',', angle,',',speed)      ##############<<<<<<<<<<<<<<<<<<<<<<<<<   CSV




     if (x < 5):
      speed= - speed
      sound1.play()
     if (x > 1200):
      speed= - speed
      sound1.play()


# draw elements in the screen    #########################
     screen.fill(bg)
     pygame.draw.rect(screen, red, pygame.Rect(100, 200, 1300, 100), 49)  # beam
     pygame.draw.circle(screen, green, [750,400],100)  #support
     pygame.draw.rect(screen, green, pygame.Rect(650, 400, 200, 100), 49)  # support
     pygame.draw.circle(screen, blue, [x+100,150],50)  #The Ball

     font = pygame.font.Font('freesansbold.ttf', 32)
     text = font.render('Beam Angle : '+str(angle)+' deg', True, green, blue)
     textRect = text.get_rect()
     textRect.center = (400, 400)
     screen.blit(text, textRect)

     events = pygame.event.get()
     for event in  events :
         pass
         if event.type == pygame.QUIT:
             done = True
             # deactivates the pygame library
             pygame.quit()
             # quit the program.
             quit()
     pygame_widgets.update(events)  # hmmm
     pygame.display.update()
     clock.tick(20)   #20 fps
     #print(clock.get_fps())
