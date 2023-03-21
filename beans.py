import random
import pygame
from pygame.locals import *

# importing audio mixer
from pygame import mixer 

# initializing audio mixer

mixer.init()

pygame.init()

# set up the window

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Garbanzo Beanz')

bg = pygame.image.load('kitchenLandscape.png')

# fill background

background = pygame.Surface(screen.get_size())

background = background.convert()

background.fill((0, 0, 0))

# blit everything to the screen

screen.blit(background, (0, 0))

pygame.display.flip()

# create character function
# character is a circle object

def reset():
    #deletes highscore file if wave count is higher than the highscore
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
        if my_character.flying_object_wave_count > highscore:
            f = open("highscore.txt", "w")
            f.write(str(my_character.flying_object_wave_count))
            f.close()
        f.close()
        
        
    #resets game to beggining
    my_character.flying_object_wave_count = 0
    my_character.flying_object_counter = 0
    my_character.flying_object_threshold = 5 * my_character.flying_object_wave_count
    my_character.flying_objects = pygame.sprite.Group()
    my_character.rect.centerx = 100
    my_character.rect.centery = 100
    my_character.velocity = 0

class character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image = pygame.image.load("angryChef.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 150)
        self.velocity = 0
        
       
        
        self.flying_object_counter = 0  # counter for creating flying objects
        self.flying_object_wave_count = 0  # current number of flying objects
        self.flying_object_threshold = 5 * self.flying_object_wave_count  # maximum number of flying objects
        
        self.flying_objects = pygame.sprite.Group()

    def move_up(self):
        self.rect.centery -= 4

    def move_down(self):
        self.rect.centery += 4 

    def move_left(self):
        self.rect.centerx -= 6.5

    def move_right(self):
        self.rect.centerx += 4

    def gravity(self):
        

        if self.rect.bottom >= screen.get_rect().bottom:
            self.rect.bottom = screen.get_rect().bottom
            self.velocity = 0

        self.rect.centery += self.velocity
        
        
        
        
    def create_flying_object(self):
        if self.flying_object_counter % 50 <= self.flying_object_wave_count:
                        # create a new flying object using bean.png
            flying_object = pygame.sprite.Sprite()
            
            #randomly selects one of the images for enemy beans things that you dodge
            ran = random.randint(0,2)
            if ran == 0:
                flying_object.image = pygame.image.load("bean.jpg").convert_alpha()
                resized_image = pygame.transform.scale(flying_object.image, (45, 30)) # resize the image
                
                
            elif ran == 1:
                flying_object.image = pygame.image.load("bean2.jpg").convert_alpha()
                resized_image = pygame.transform.scale(flying_object.image, (100, 60)) # resize the image

            elif ran == 2:
                flying_object.image = pygame.image.load("bean3.jpg").convert_alpha()
                resized_image = pygame.transform.scale(flying_object.image, (40, 50)) # resize the image
            
            
            
            resized_image = pygame.transform.rotate(resized_image, random.randint(0, 4) * 90)
                
                
            flying_object.image = resized_image
            
            flying_object.rect = flying_object.image.get_rect()
            flying_object.rect.x = 800
            flying_object.rect.y = random.randint(0, 800)
            
            # add the flying object to the group
            self.flying_objects.add(flying_object)
        
        
        
        
    def update_flying_objects(self):
        # update the position of the flying objects
        for flying_object in self.flying_objects:
            flying_object.rect.x -= 5
            
            # check for collision with the player
            if pygame.sprite.collide_rect(flying_object, self):
                reset()
  
# remove the flying object if it goes off the screen
            if flying_object.rect.x < -100:
                self.flying_objects.remove(flying_object)




# create character instance
my_character = character()

font = pygame.font.Font('freesansbold.ttf', 12)






# initialize movement flags
move_up = False
move_down = False
move_left = False
move_right = False
gravity = True

# initialize clock
clock = pygame.time.Clock()

# set the desired frame rate
FPS = 60

def jump(character):
    if character.rect.bottom == screen.get_rect().bottom:
        character.velocity = -10


# loading music file
mixer.music.load('song.mp3')
# setting volume
mixer.music.set_volume(0.3)
mixer.music.play()

        
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
    my_character.create_flying_object()
    my_character.update_flying_objects()
    
    my_character.flying_object_counter += 2
    
    if my_character.flying_object_counter % 2000 == 0 :
        my_character.flying_object_wave_count += 1
            
         
        
        
        
        
    # draw everything
    text = font.render(str(my_character.flying_object_wave_count), True, (255, 255, 255))
    screen.blit(bg, (0, 0))
    screen.blit(my_character.image, my_character.rect)
    for flying_object in my_character.flying_objects:
        screen.blit(flying_object.image, flying_object.rect)
    screen.blit(text, (0, 0))
    pygame.display.flip()
    
    # update the clock
    clock.tick(FPS)
    
#reset function
    
    #pygame install command: python -m pip install -U pygame==2.3.0 --user
