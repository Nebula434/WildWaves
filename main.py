# Example file showing a basic pygame "game loop"
import pygame, sys
from pygame.locals import *
import random 
import os 
# pygame setup
pygame.init()
#le color white
WHITE = (255, 255, 255)
# directories 
wizard_dir = r"E:/Personal Projects/WildWaves/assests/Units/Blue Units/Monk"
warrior_dir = r"E:/Personal Projects/WildWaves/assests/Units/Blue Units/Warrior"
#enemies_dir = r"C:/Users/playa/Desktop/MaybeASillyLittleGame/assests/Units/Red Units" # this must be changed later on !!!

# important py game stuff
clock = pygame.time.Clock()
running = True
GameOver = False # When this is true -> go to game over screen 
GameState = ["menu","paused","playing"] # When player is playing match, set this to Playing, if playing and Keys[K_escape]: GameState "paused"


#Display Settings
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Wild Waves")


# Player Stats & Health
MainSpeed = 3
MainHealth = 20 
MainDamage = 5 
MainSpread= 3 # So the player is able to swing in roughly 3 cm wide, like cutting in half
ClassChoice = ["none","warrior","wizard"]
# Important inventory stats like 
#Weapon Stats this could be done better but I can't apply the matters i want into it 


#Enemy Stats
EnemyDamage = 0
EnemyHealth = 20
# Base Variables, ideally this variable will be subtracted from later, once BaseHealth = 0 -> Game Over screen
BaseHealth = 15
if BaseHealth == 0:
        GameOver = True
#Player Sprite Animation BS bro oh my fuckin god
# loads the base player sheet, probably should change this later
PlayerSpriteSheetPath = os.path.join(wizard_dir,"Idle.png")
PlayerSpriteSheet = pygame.image.load(PlayerSpriteSheetPath).convert_alpha()
# Animation helper? im not too sure how this works, gotta research it
def load_animation(path, frame_w, frame_h, num_frames, row=0, spacing_x=0, margin_x=0):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    x = margin_x
    y = row * frame_h
    for _ in range(num_frames):
        rect = pygame.Rect(x, y, frame_w, frame_h)
        frames.append(sheet.subsurface(rect).copy())
        x += frame_w + spacing_x
    return frames

# frame size for base player sheet, this is mostly the same for each sprite
FRAME_W = 192
FRAME_H = 192
frame_width = FRAME_W
frame_height = FRAME_H
# This for the Wizard sprites only, warriors will be seperate 
IDLE_FRAMES = 6
RUN_FRAMES  = 4

animations = {
    "idle": load_animation(os.path.join(wizard_dir, "Idle.png"), FRAME_W, FRAME_H, IDLE_FRAMES),
    "run" : load_animation(os.path.join(wizard_dir, "Run.png"),  FRAME_W, FRAME_H, RUN_FRAMES),
}
anim_speed_ms = {
    "idle": 100,   # ~10 FPS
    "run" : 70,    # ~14 FPS (snappier)
}

num_frames = IDLE_FRAMES 
# Says its slicing the sprite sheet into individual frames
frames = []
for i in range(num_frames):
    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
    frame = PlayerSpriteSheet.subsurface(frame_rect).copy()
    frames.append(frame)

class MainPlayer:
    def __init__(self):
            super().__init__()
            self.animations = animations
            self.anim = "idle"
            self.frames = self.animations[self.anim]
            self.frame_index = 0
            self.image = frames[self.frame_index]
            self.rect = self.image.get_rect(center=(640,360))
            self.frame_delay_ms = 100          # ~10 fps
            self.last_update_ms = pygame.time.get_ticks()
            self.facing_left = False
    def set_animation(self, name):
        if name != self.anim:
            self.anim = name
            self.frames = self.animations[self.anim]
            self.frame_index = 0
            self.last_update_ms = pygame.time.get_ticks()
            # keep position while swapping images
            self.rect = self.image.get_rect(center=self.rect.center)
    def UpdateDamage(self):
            print(f"Damage Taken \n{EnemyDamage}")
    def update(self): #frame update !!
#       ~ Movement, really simple for the most part, adjusting self.facing_left to assume which direction to face the character ~
        Keys = pygame.key.get_pressed()
        moving = False

        if Keys[pygame.K_a]:
            print("Pressed A or Left arrow")
            self.rect.move_ip(-MainSpeed,0)
            self.facing_left = True
            moving = True
        if Keys[pygame.K_d]:
            print("Pressed D or Right arrow")
            self.rect.move_ip(MainSpeed,0)
            self.facing_left = False
            moving = True 
        #if Keys[pygame.K_space]:
            #print("I have attacked!")
        if Keys[pygame.K_o]:
            print(f"This is ur Current Player Stats,\n{MainHealth}HP\n{MainSpeed}m/s\n{MainSpread}cm\n{MainDamage}")
         #   if GameState[2] and Keys[K_escape]: 
           #     GameState = [1]
        
        # --- choose animation based on movement ---
        self.set_animation("run" if moving else "idle")  
        # --- advance animation on its own speed ---
        now = pygame.time.get_ticks()
        if now - self.last_update_ms > anim_speed_ms[self.anim]:
            self.last_update_ms = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        # --- pick current frame, then flip if needed ---
        self.image = self.frames[self.frame_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
    def draw(self, surface):

        surface.fill(WHITE, self.rect)
        surface.blit(self.image, self.rect)

class Enemy:
      def __init__(self):
            
            pass
Player = MainPlayer()
WaveEnemies = Enemy()


while running: # every frame the stuff below is happening
    # pygame.QUIT event means the user clicked X to close your window
    # GameState = [0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    Player.update()
    Player.draw(screen)





    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()