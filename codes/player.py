import pygame

class Player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__speed = 10
        self.img = pygame.image.load("images/spaceships/spaceship.png") 
        self.__collision_sound = pygame.mixer.Sound('sounds/Collision.mp3') 
        self.left = False
        self.right = False
        self.fire = False
        self.__is_destroyed = False

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_speed(self):
        return self.__speed

    def move_left(self):
        self.__x-= self.__speed
    
    def move_right(self):
        self.__x+= self.__speed
    
    def move_down(self, amount):
        self.__y+= amount

    def is_destroyed(self):
        return self.__is_destroyed

    def destroy(self):
        self.img = pygame.transform.rotate(self.img, 10) #Flips the rocket image to the left
        pygame.mixer.Sound.play(self.__collision_sound) #Plays a collision sound
        self.__is_destroyed = True

class Bullet:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.img = pygame.image.load("images/spaceships/laser.png") 
        self.__fire_sound = pygame.mixer.Sound('sounds/Fire_1.mp3')
        self.up = False

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    #Plays the shooting sound
    def fire_sound(self):
        pygame.mixer.Sound.play(self.__fire_sound) 

    
    def move_left(self, amount):
        self.__x-= amount
    
    def move_right(self, amount):
        self.__x+= amount
    
    #Moves the bullet upwards, accelerating according to the height of the bullet
    def move_up(self):
        speed = next(self.accelerate()) 
        self.__y -= speed
        if self.get_y() <= 200:
            speed = next(self.accelerate()) 
            self.__y -= speed
        if self.get_y() <= 500:
            speed = next(self.accelerate())
            self.__y -= speed
        if self.get_y() <= 700:
            speed = next(self.accelerate())
            self.__y -= speed
    
    #Accelerates until maximum speed is reached
    def accelerate(self):
        __start_speed = 20
        __max_speed = 100
        while __start_speed <= __max_speed:
            yield __start_speed
            __start_speed += 20
