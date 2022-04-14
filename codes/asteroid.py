import pygame
from random import randrange

class Asteroid:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.img = pygame.image.load("images/asteroids/asteroid.png")
        self.__Rock_break_sound = pygame.mixer.Sound('sounds/Rock_break.mp3') #Load the break sound from the folder
        self.__destroyed = False
        self.down = True
        self.__speed = 2

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y
    
    def get_speed(self):
        return self.__speed
    
    def add_speed(self):
        self.__speed+=0.5 
    
    def is_destroyed(self):
        return self.__destroyed

    def destroy(self):
        pygame.mixer.Sound.play(self.__Rock_break_sound) #Play the break sound
        self.__destroyed = True

    def asteroid_movement(self):         
        ##If the asteroid is at the bottom of the screen or destroyed
        if self.__y+self.img.get_height() > 800 or self.__destroyed:
            rand_y = randrange(50, 670) 
            self.set_y(-rand_y) 
            self.set_x(randrange(0, 1280-self.img.get_width())) 
            self.add_speed() #Accelerates the asteroid
            self.__destroyed = False
        else:
            #Moves the asteroid down
            self.__y += self.__speed
