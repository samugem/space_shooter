import pygame
from random import randrange
import time
from player import *
from asteroid import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Space Shooter') 
        self.__window_size = 1280,720 
        self.__window = pygame.display.set_mode((self.__window_size))
        self.__pygame_clock = pygame.time.Clock()
        self.__new_game()
        self.__loop()

    #Draw countdown
    def __show_countdown(self):
        number = 5 - self.__get_time()
        if number >= 0:
                font = pygame.font.SysFont("Arial", 100)
                xcenter = self.__window_size[0] // 2
                text = font.render(f"{number}", True, (255, 255, 255))
                self.__window.blit(text, (xcenter - text.get_width()//2, 200))
        else:    
            self.__countdown = False
            self.__instructions = False
            self.__start_time = time.time()


    def __new_game(self):
        self.__player = Player(570, 600) #Creates a player ship
        self.__bullet = Bullet(570, 720) #Creates the bullet
        self.__asteroids = list()
        self.__create_asteroids(15) #Creates a selected number of asteroids
        self.__gameover = False
        self.__instructions = True
        self.__countdown = True
        self.__score = 0
        self.__timenow = 0
        self.__start_time = time.time()
        self.__game_over_sound = pygame.mixer.Sound('sounds/Game_Over.mp3')       


    #Draws UI with a score and a timer
    def __show_ui(self):
        if not self.__gameover and not self.__countdown: #If gameover and countdown are false, the get_time method retrieves the elapsed time in the game
            self.__timenow = self.__get_time()
        font = pygame.font.SysFont("Arial", 40)
        scoretext = font.render(f"Score:{self.__score}", True, (0, 0, 255))
        timertext = font.render(f"{self.__timenow}s", True, (255, 255, 255))
        self.__window.blit(scoretext, (0, 0))
        self.__window.blit(timertext, (1280-timertext.get_width(), 0))

    #Add one to the points
    def __add_score(self):
        self.__score+=1

    #Returns the time played in seconds, rounded to the nearest whole number
    def __get_time(self):
        timenow =  time.time() - self.__start_time
        return round(timenow) 

    #Draw gameover text and sequel instructions in the center of the screen
    def __show_game_over(self):
        font1 = pygame.font.SysFont("Arial", 84)
        font2 = pygame.font.SysFont("Arial", 64)
        xcenter = self.__window_size[0] // 2
        ycenter = self.__window_size[1] // 2
        text1 = font1.render("Game over!", True, (255, 0, 0))
        text2 = font2.render("Press enter to try again", True, (255, 255, 255))
        self.__window.blit(text1, (xcenter - text1.get_width()//2, ycenter-42))
        self.__window.blit(text2, (xcenter - text2.get_width()//2, ycenter+32))
    
    #Draws objects on the screen
    def __update_screen(self):
        self.__window.fill((0, 0, 0))
        #Draws UI
        self.__show_ui()
        #Draws a player's ship
        self.__window.blit(self.__player.img, (self.__player.get_x(), self.__player.get_y()))
        #Draws all the asteroids in the list
        for asteroid in self.__asteroids:
            self.__window.blit(asteroid.img, (asteroid.get_x(), asteroid.get_y()))
        #Draws a bullet
        self.__window.blit(self.__bullet.img, (self.__bullet.get_x(), self.__bullet.get_y()))
        #Invokes show_game_over method if the gameover is true
        if self.__gameover == True:
            self.__show_game_over()
        #Invokes show_instructions method if the __instructions is true
        if self.__instructions == True:
            self.__show_instructions()
        #Invokes show_countdown method if the show_countdown is true
        if self.__countdown == True:
            self.__show_countdown()
        pygame.display.flip()
        self.__pygame_clock.tick(60) #Screen refresh rate 60fps

    #Reads events
    def __check_events(self):
        for event in pygame.event.get():
            #Player controls
            if event.type == pygame.KEYDOWN: #If the key is pressed
                if not self.__player.is_destroyed() and not self.__countdown: #Works if the player's ship is not destroyed or a countdown is true
                    if event.key == pygame.K_LEFT:
                        self.__player.left = True
                    elif event.key == pygame.K_RIGHT:
                        self.__player.right = True
                    elif event.key == pygame.K_UP or pygame.K_SPACE:
                        self.__player.fire = True
                #Start a new game with enter
                if event.key == pygame.K_RETURN:
                    self.__new_game()

            elif event.type == pygame.KEYUP: #If the key is up
                if event.key == pygame.K_LEFT:
                    self.__player.left = False
                elif event.key == pygame.K_RIGHT:
                    self.__player.right = False
                elif event.key == pygame.K_UP or pygame.K_SPACE:
                    self.__player.fire = False
            #Exit the game with the x button on the window
            if event.type == pygame.QUIT:
                exit()
            #If the fire button is pressed and the bullet is not going up
            if self.__player.fire and self.__bullet.up == False:
                self.__bullet.set_y(self.__player.get_y()-self.__bullet.img.get_height()) #Place the bullet above the player's ship
                self.__bullet.up = True  #The bullet moves up
                self.__bullet.fire_sound()

    #Checks whether objects collide horizontally or vertically
    def __check_collide(sel, one, other):
        y_tolerance = 50 #The amount of hit detection tolerance on the y axis
        if one.get_x()+one.img.get_width() >= other.get_x() and one.get_x() <= other.get_x()+other.img.get_width() and one.get_y()+one.img.get_height() >= other.get_y() + y_tolerance: #or (other_x + other_width) >= self_left:
            return True
        else:
            return False

    #Moves the player's spaceship
    def __player_movement(self):
        #Check if the asteroid on the list collided with the player
        for asteroid in self.__asteroids: 
            if self.__check_collide(asteroid, self.__player):
                self.__player.move_down(asteroid.get_speed()) #Moves the player down
                if not self.__player.is_destroyed():
                    self.__player.destroy() #Destroys the player's ship
                #If the player has gone down from the bottom of the screen
                if(self.__player.get_y() > 700):
                    #If not already a gameover
                    if not self.__gameover:
                        pygame.mixer.Sound.play(self.__game_over_sound) #Play gameover sound
                        self.__gameover = True
        #To the right
        if self.__player.right and  self.__player.get_x()+self.__player.img.get_width() < 1280:
            self.__player.move_right()

        #To the left
        elif self.__player.left and self.__player.get_x() > 0:
            self.__player.move_left()

    #Moves the bullet
    def __bullet_movement(self):
        #Reads asteroids from the list
        for asteroid in self.__asteroids:
            #If an asteroid collides with a bullet and neither was above the top of the screen
            if not self.__player.is_destroyed():
                if self.__check_collide(asteroid, self.__bullet) and self.__bullet.get_y() > 0 and asteroid.get_y() > 0: 
                    asteroid.destroy()
                    self.__add_score()
        #If the bullet moves up and it is not above the top of the screen
        if self.__bullet.up and self.__bullet.get_y() + self.__bullet.img.get_height() >= 0:
            self.__bullet.move_up()
        #If the above does not apply, transfer the bullet back to the rocket
        else:
            self.__bullet.up = False
            self.__bullet.set_x(self.__player.get_x()+(self.__player.img.get_width()//2)-self.__bullet.img.get_width()//2) #Center the bullet in the center of the rocket on the x-axis
        #If the bullet is still in the rocket, it will move with the rocket
        if self.__bullet.up == False:
            #To the right
            if self.__player.right:
                self.__bullet.move_right(self.__player.get_speed())
            #To the left
            if self.__player.left:
                self.__bullet.move_left(self.__player.get_speed())

    def __create_asteroids(self, amount):
        #If the number of asteroids in the list is less than the desired number
        if len(self.__asteroids) < amount:
            asteroid = Asteroid(650, -50) #Create an asteroid
            randomx =randrange(0, 1280-asteroid.img.get_width()) #Random number between the number 0 and (width of the asteroid 1280)
            randomy =randrange(50, 670) #Random number between 50 and 670
            asteroid.set_x(randomx) #Converts the value of randomx to the x coordinate of asteroid
            asteroid.set_y(-randomy) #Converts the asteroid y coordinate to the negative value of randomy
            self.__asteroids.append(asteroid) #Add the asteroid to the list
            self.__create_asteroids(amount)
    
    #Draws game instructions on the screen
    def __show_instructions(self):
        font = pygame.font.SysFont("Arial", 44)
        xcenter = self.__window_size[0] // 2
        ycenter = self.__window_size[1] // 2
        text1 = font.render("Move with the left and right arrow key", True, (255, 255, 255))
        text2 = font.render("and shoot with the up arrow key or space", True, (255, 255, 255))
        self.__window.blit(text1, (xcenter - text1.get_width()//2, ycenter-44))
        self.__window.blit(text2, (xcenter - text2.get_width()//2, ycenter))
    
    #Repeat below, as long as true
    def __loop(self):
        while True:
            self.__check_events()
            self.__update_screen()
            if not self.__countdown:
                self.__player_movement()
                self.__bullet_movement()
                #If not a gameover
                if not self.__gameover:
                    #Invokes the method of moving each asteroid object
                    for asteroid in self.__asteroids: 
                        asteroid.asteroid_movement()
        
if __name__ == "__main__":
    Game() #Call the Game class
