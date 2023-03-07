# makes a window with pygame
# with movable character

# Path: character.py
# makes a character with pygame

import random
import pygame
from pygame.locals import *


pygame.init()

# set up the window

screen = pygame.display.set_mode((400, 300))

pygame.display.set_caption('Pygame window')

# fill background

background = pygame.Surface(screen.get_size())

background = background.convert()

background.fill((0, 0, 0))

# blit everything to the screen

screen.blit(background, (0, 0))

pygame.display.flip()

# create character function
# character is a circle object

class character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 150)
        self.velocity = 0
        
        self.flying_objects = pygame.sprite.Group()

    def move_up(self):
        self.rect.centery -= 3

    def move_down(self):
        self.rect.centery += 3

    def move_left(self):
        self.rect.centerx -= 3

    def move_right(self):
        self.rect.centerx += 3

    def gravity(self):
        

        if self.rect.bottom >= screen.get_rect().bottom:
            self.rect.bottom = screen.get_rect().bottom
            self.velocity = 0

        self.rect.centery += self.velocity
        
        
    def create_flying_object(self):
        # create a new flying object
        flying_object = pygame.sprite.Sprite()
        flying_object.image = pygame.Surface((3, 3))
        flying_object.image.fill((0, 255, 0))
        flying_object.rect = flying_object.image.get_rect()
        flying_object.rect.x = 800
        flying_object.rect.y = random.randint(0, 400)
        
        # add the flying object to the group
        self.flying_objects.add(flying_object)
        
    def update_flying_objects(self):
        # update the position of the flying objects
        for flying_object in self.flying_objects:
            flying_object.rect.x -= 5
            
            # check for collision with the player
            if pygame.sprite.collide_rect(flying_object, self):
                pygame.quit()
                
            # remove the flying object if it goes off the screen
            if flying_object.rect.x < -30:
                self.flying_objects.remove(flying_object)

# create character instance
my_character = character()

# initialize movement flags
move_up = False
move_down = False
move_left = False
move_right = False
gravity = True

# initialize clock
clock = pygame.time.Clock()

# set the desired frame rate
FPS = 20

def jump(character):
    if character.rect.bottom == screen.get_rect().bottom:
        character.velocity = -10

# event loop
while True:
    # character movement and window close
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                move_up = True
            elif event.key == K_DOWN:
                move_down = True
            elif event.key == K_LEFT:
                move_left = True
            elif event.key == K_RIGHT:
                move_right = True
            elif event.key == K_SPACE:
                jump(my_character)
        elif event.type == KEYUP:
            if event.key == K_UP:
                move_up = False
            elif event.key == K_DOWN:
                move_down = False
            elif event.key == K_LEFT:
                move_left = False
            elif event.key == K_RIGHT:
                move_right = False

    # move the character
    if(my_character.rect.top > 0):
        if move_up:
            my_character.move_up()
    if(my_character.rect.bottom < screen.get_rect().bottom):
        if move_down:
            my_character.move_down()
            
        if gravity:
            my_character.gravity()
            
            
    if(my_character.rect.left > 0):
        if move_left:
            my_character.move_left()
    if(my_character.rect.right < screen.get_rect().right):
        if move_right:
            my_character.move_right()
        
            
    if((move_up == False)):
        gravity = True
    else:
        gravity = False
        
    my_character.create_flying_object()
    my_character.update_flying_objects()
        
    # draw everything
    screen.blit(background, (0, 0))
    screen.blit(my_character.image, my_character.rect)
    for flying_object in my_character.flying_objects:
        screen.blit(flying_object.image, flying_object.rect)
    pygame.display.flip()
    
    # update the clock
    clock.tick(FPS)
    
    

