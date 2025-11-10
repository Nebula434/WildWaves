# Example file showing a basic pygame "game loop"
import pygame, sys
from pygame.locals import *
import pygame_menu
import random 
import os 
#le color white
WHITE = (255, 255, 255)
PRETTYCOLOR = ( 232, 181,189)
# directories 
wizard_dir = r"E:/Personal Projects/WildWaves/assests/Units/Blue Units/Monk"
warrior_dir = r"E:/Personal Projects/WildWaves/assests/Units/Blue Units/Warrior"
enemy_dir = r"E:\Personal Projects\WildWaves\assests\Units\Red Units\Warrior"
terrain_assests_dir = r"E:\Personal Projects\WildWaves\assests\Terrain"
base_assests_dir = r"E:\Personal Projects\WildWaves\assests\Buildings\Blue Buildings"
tile_dir = r"E:\Personal Projects\WildWaves\assests\Terrain\Tiles"
#placeholder assests for enemies for the time being



# important py game stuff, fps, game state, screen
pygame.init()
clock = pygame.time.Clock()
game_running = True
STATE_MENU = "menu"
STATE_GAME = "game"
game_state = STATE_MENU
GameOver = False 
# When this is true -> go to game over screen 


#Display Settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wild Waves")
FONT = pygame.font.Font(None, 80)
#TILE VARIABLES
TILE_SIZE = 64


# Player Stats & Health, need a better way to categorize this
MainSpeed = 3
MainHealth = 20 
MainDamage = 5 
MainSpread= 3 # So the player is able to swing in roughly 3 cm wide, like cutting in half
ClassChoice = ["none","warrior","wizard"]


#Enemy Stats
EnemyDamage = 0
EnemyHealth = 20
# Ideally make a way that the enemy varies from warrior our wizard our lancer. 


# Base Variables, ideally this variable will be subtracted from later, once BaseHealth = 0 -> Game Over screen
BaseHealth = 15
if BaseHealth == 0:
        GameOver = True
# Non Dynamic Images 
background_image = pygame.image.load(os.path.join(terrain_assests_dir,"Water Background color.png"))
tile_image = pygame.image.load(os.path.join(tile_dir),"Tilemap_color4.png")

#Player Sprite Animation BS bro oh my fuckin god

def load_animation(path, frame_w, frame_h, num_frames, row=0, spacing_x=0, margin_x=0): # animation helper 
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
# This for the Wizard sprites only, warriors will be seperate. ADDING WIZARD_  might fix a conflicting problem later on
WIZARD_IDLE_FRAMES = 6
WIZARD_RUN_FRAMES  = 4
WIZARD_ATTACK_FRAMES = 11  # this is also the heal frames for wizards!!
WIZARD_CHARACTER_EFFECT_FRAMES = 11
PLAYER_HEIGHT = 192
PLAYER_WIDITH = 192

#Enemy Frames for the sprites, none of these have been tested 11/10
ENEMY_IDLE_FRAMES = 8
ENEMY_RUN_FRAMES = 6
ENEMY_ATTACK_FRAMES = 4
ENEMY_RETURNATTACK_FRAMES = 4
animations = {
    "wizard_idle": load_animation(os.path.join(wizard_dir, "Idle.png"), FRAME_W, FRAME_H, WIZARD_IDLE_FRAMES),
    "wizard_run" : load_animation(os.path.join(wizard_dir, "Run.png"),  FRAME_W, FRAME_H, WIZARD_RUN_FRAMES),
    "enemy_idle": load_animation(os.path.join(enemy_dir, "Warrior_Idle.png"), FRAME_W, FRAME_H, ENEMY_IDLE_FRAMES),
    "enemy_run": load_animation(os.path.join(enemy_dir, "Warrior_Run.png"), FRAME_W, FRAME_H, ENEMY_RUN_FRAMES),
    "enemy_attack1": load_animation(os.path.join(enemy_dir, "Warrior_Attack1.png"), FRAME_W, FRAME_H, ENEMY_ATTACK_FRAMES),
    "enemy_attack2": load_animation(os.path.join(enemy_dir, "Warrior_Attack2.png"), FRAME_W, FRAME_H, ENEMY_ATTACK_FRAMES),
}
anim_speed_ms = {
    "wizard_idle": 100,   # ~10 FPS
    "wizard_run" : 70,    # ~14 FPS (snappier)
    "enemy_idle" : 100,
    "enemy_run" : 70,
    "enemy_attack1" : 50,
    "enemy_attack2" : 60,
}
#Character Abilities, to start, Dash, Magic Missle, Thunder Storm (finds enemies in radius around player, casts a lighting bolt on them, 60 second cooldown)

    
# MainPlayer consists of all the things the player does & handles the animation within, maybe should make a animation class?
class MainPlayer:
    def __init__(self):
            super().__init__()
            self.animations = animations
            self.anim = "wizard_idle" 
            self.frames = self.animations[self.anim]
            self.frame_index = 0
            self.image = self.frames[self.frame_index] # image is decided after running through which frame to pick from above
            self.rect = self.image.get_rect(center=(640,360)) #Character is drawn here each time th game is started 
            self.frame_delay_ms = 100          #how fast the animation runs, 10 fps
            self.last_update_ms = pygame.time.get_ticks() 
            self.facing_left = False
    def set_animation(self, name):
        if name != self.anim:
            self.anim = name
            self.frames = self.animations[self.anim] # 
            self.frame_index = 0
            self.last_update_ms = pygame.time.get_ticks()
            # keep position while swapping images
            self.rect = self.image.get_rect(center=self.rect.center) # image is decided again after 
    def update(self): #everything that needs to happen in each frame for character to do as they should 
#       ~ Movement, really simple for the most part, adjusting self.facing_left to assume which direction to face the character ~
        Keys = pygame.key.get_pressed()
        moving = False
        if Keys[pygame.K_w] or Keys[pygame.K_UP]:
            print("Pressed W or Up arrow")
           # self.rect.move_ip(0,-MainSpeed)
            Player.rect.y = max(Player.rect.y - MainSpeed, -100) # -100 since thats when the top part ends

            moving = True
          #  if Player.rect.y < -100:
          #      Player.rect.y = -100
        
        if Keys[pygame.K_s] or Keys[pygame.K_DOWN]:
            print("Pressed S or Down arrow")
            #self.rect.move_ip(0,MainSpeed)
            moving = True
            Player.rect.y = min(Player.rect.y + MainSpeed, ((SCREEN_HEIGHT - PLAYER_HEIGHT)+50)) # +50 b/c the boundry cuts off early for some reason? 
        if Keys[pygame.K_a] or Keys[pygame.K_LEFT]:
            print("Pressed A or Left arrow")
            #self.rect.move_ip(-MainSpeed,0)
            Player.rect.x =max(Player.rect.x - MainSpeed, -50)
            self.facing_left = True
            moving = True
        if Keys[pygame.K_d] or Keys[pygame.K_RIGHT]:
            print("Pressed D or Right arrow")
            #self.rect.move_ip(MainSpeed,0)
            Player.rect.x =min(Player.rect.x + MainSpeed,((SCREEN_WIDTH - PLAYER_HEIGHT)+50))
            self.facing_left = False
            moving = True 
        if Keys[pygame.K_SPACE]:
            print("I have attacked!")
        if Keys[pygame.K_F1]:
             print("The Game has been changed to playing")
        if Keys[pygame.K_o]:
            print(f"This is ur Current Player Stats,\n{MainHealth}HP\n{MainSpeed}m/s\n{MainSpread}cm\n{MainDamage}")
        if Keys[pygame.K_LSHIFT] or Keys[pygame.K_LCTRL]:
            print(f"Dash Is Being consumed")
            Dash()

        #Add detection on where mouse is clicked and make player face that way 
        #Add check if been hit, if true then high light character red AND take away EnemyDamage. 
        #Add creation of sprites to hit enemies, magic missle is the first spell to make


        
        # Animation code i didnt make, not too sure how it works 
        self.set_animation("wizard_run" if moving else "wizard_idle")  
        now = pygame.time.get_ticks()
        if now - self.last_update_ms > anim_speed_ms[self.anim]:
            self.last_update_ms = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        # pick current frame, then flip if needed 
        self.image = self.frames[self.frame_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        # ---- #

    #draws the player
    def draw(self, surface):
        #clears previous area than draws over it
        #surface.fill(PRETTYCOLOR, self.rect)  # keeping this removed for now, just causes a shading problem around the background.
        screen.blit(background_image,(0,0)) # this is what is layered over the background
        surface.blit(self.image, self.rect) # character is drawn

class Enemy:
      def __init__(self):
            
            pass
#Map Creation and Tile Code
class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self,x,y,TILE_SIZE,TILE_SIZE)
        self.image = image

         

def create_map():
    for i in range(4):
        tile = Tile(Player.rect.x + i*TILE_SIZE, Player.rect.y + TILE_SIZE*2,tile_image)
        tiles.append(tile)
#

#Super sloppy menu code
menu = pygame_menu.Menu('Wild Waves', 600, 400, theme=pygame_menu.themes.THEME_BLUE)
def start_game():
     global game_state
     game_state = STATE_GAME 
def quit_game():
    pygame.event.post(pygame.event.Event(pygame.QUIT)) #if im calling a pygame event in a function it looks like this why???
menu.add.text_input('Name :', default='John Doe')
menu.add.button(f'Play', start_game)
menu.add.button('Quit', quit_game)
menu.center_content()
#Menu Code ^^^^^^


#Establishing a variable for classes
Player = MainPlayer()
WaveEnemy = Enemy()
tiles = []
create_map()
#
#
while game_running: # every frame the stuff below is happening
    # pygame.QUIT event means the user clicked X to close your window
    # GameState = [0]
    events = pygame.event.get()
    for event in events:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_state == STATE_GAME:
            game_state = STATE_MENU

    if game_state == STATE_MENU:
        screen.fill((25, 25, 30))
        menu.update(events)     #non-blocking menu 
        menu.draw(screen)
    else:
        Player.update()
        screen.fill(PRETTYCOLOR)
        Player.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()