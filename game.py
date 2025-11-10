#
import pygame, sys
from pygame.locals import *
import pygame_menu
import random 
import os 
# directories 
wizard_dir = r"E:/Personal Projects/WildWaves/assests/Units/Blue Units/Monk"
warrior_dir = r"E:/Personal Projects/WildWaves/assests/Units/Blue Units/Warrior"
enemy_dir = r"E:\Personal Projects\WildWaves\assests\Units\Red Units\Warrior"
terrain_assests_dir = r"E:\Personal Projects\WildWaves\assests\Terrain"
base_assests_dir = r"E:\Personal Projects\WildWaves\assests\Buildings\Blue Buildings"
tile_dir = r"E:\Personal Projects\WildWaves\assests\Terrain\Tiles"
#
#Display Settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
PRETTYCOLOR = ( 232, 181,189)
# frame size for base player sheet, this is mostly the same for each sprite
FRAME_W = 192
FRAME_H = 192
# This for the Wizard sprites only, warriors will be seperate. ADDING WIZARD_  might fix a conflicting problem later on
WIZARD_IDLE_FRAMES = 6
WIZARD_RUN_FRAMES  = 4
WIZARD_ATTACK_FRAMES = 11  # this is also the heal frames for wizards!!
WIZARD_CHARACTER_EFFECT_FRAMES = 11
PLAYER_HEIGHT = 192
PLAYER_WIDTH = PLAYER_HEIGHT

#Enemy Frames for the sprites, none of these have been tested 11/10
ENEMY_IDLE_FRAMES = 8
ENEMY_RUN_FRAMES = 6
ENEMY_ATTACK_FRAMES = 4
ENEMY_RETURNATTACK_FRAMES = 4
# Intial Player Constants
PLAYER_SPEED = 5
PLAYER_HEALTH = 20
PLAYER_DAMAGE = 3
PLAYER_RANGE = 50
#compat code
PlayerNewSpeed = PLAYER_SPEED
PlayerNewHealth = PLAYER_HEALTH
PlayerNewRange = PLAYER_RANGE
PlayerNewDamage = PLAYER_DAMAGE





#Set constants prior to this
#
# Initialize Pygame
pygame.init()
#start ticking 
clock = pygame.time.Clock()

# Set up the game window
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("WildWaves: Mage Mania")

# Screen is made, now we can load our animations
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
#Player Animation End


#End of animation code
#Player Code
class MainPlayer:
    def __init__(self):
        """Initialize player with animation and position."""
        super().__init__()
        self.animations = animations
        self.anim = "wizard_idle" 
        self.frames = self.animations[self.anim]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(640, 360))
        self.frame_delay_ms = 100
        self.last_update_ms = pygame.time.get_ticks() 
        self.facing_left = False
    
    def set_animation(self, name):
        """Switch to a different animation if needed."""
        if name != self.anim:
            self.anim = name
            self.frames = self.animations[self.anim]
            self.frame_index = 0
            self.last_update_ms = pygame.time.get_ticks()
            # Keep position while swapping images
            self.rect = self.image.get_rect(center=self.rect.center)
    
   # def _get_movement_bounds(self):
   #     """Calculate the bounds within which the player can move."""
    #    return LAND_RECT.inflate(GROUND_FEATHER, GROUND_FEATHER)
    
    def _handle_movement(self, keys):
        """
        Handle player movement based on keyboard input.
        Returns True if player is moving, False otherwise.
        """
        moving = False
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y = max(self.rect.y - PlayerNewSpeed, 0)
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y = min(self.rect.y + PlayerNewSpeed, SCREEN_HEIGHT - self.rect.height)
            moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - PlayerNewSpeed, 0)
            self.facing_left = True
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + PlayerNewSpeed, SCREEN_WIDTH - self.rect.width)
            self.facing_left = False
            moving = True
        
        return moving
    
    def _handle_input(self, keys):
        """Handle non-movement keyboard input (actions, debug, etc.)."""
        if keys[pygame.K_SPACE]:
            print("I have attacked!")
        if keys[pygame.K_F1]:
            print("The Game has been changed to playing")
        if keys[pygame.K_o]:
            print(f"This is ur Current Player Stats,\n{PlayerNewHealth}HP\n{PlayerNewSpeed}m/s\n{PlayerNewRange}cm\n{PlayerNewDamage}")
        if keys[pygame.K_LSHIFT] or keys[pygame.K_LCTRL]:
            print(f"Dash Is Being consumed")
            # Dash()
        if keys[pygame.K_F2]:
            print(f"I am at {self.rect.x} and {self.rect.y}")
        # TODO: Add detection on where mouse is clicked and make player face that way 
        # TODO: Add check if been hit, if true then highlight character red AND take away EnemyDamage. 
        # TODO: Add creation of sprites to hit enemies, magic missle is the first spell to make
    
    def _update_animation(self, moving):
        """
        Update animation frame based on movement state and timing.
        Handles frame progression and sprite flipping.
        """
        # Set animation based on movement state
        self.set_animation("wizard_run" if moving else "wizard_idle")
        
        # Advance frame if enough time has passed
        now = pygame.time.get_ticks()
        if now - self.last_update_ms > anim_speed_ms[self.anim]:
            self.last_update_ms = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        
        # Get current frame and flip if facing left
        self.image = self.frames[self.frame_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def update(self):
        """
        Main update method called each frame.
        Coordinates movement, input handling, and animation updates.
        """
        keys = pygame.key.get_pressed()
        
        # Handle movement and get movement state
        moving = self._handle_movement(keys)
        
        # Handle other input (actions, debug keys)
        self._handle_input(keys)
        
        # Update animation based on movement state
        self._update_animation(moving)
    
    def draw(self, surface):
        """Draw the player sprite to the given surface."""
        surface.blit(self.image, self.rect)
#
Player = MainPlayer()


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update player state, this handles movement, animation, input etc. 
    Player.update()
    
    # Clear screen ensures no ghosting is happening 
    screen.fill(PRETTYCOLOR)
    
    # Draw Player onto screen
    Player.draw(screen)
    
    # Update display
    pygame.display.update()
    
    # Control frame rate
    clock.tick(60)

pygame.quit()