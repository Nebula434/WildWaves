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
title_dir = r"E:\Personal Projects\WildWaves\assests\TitleTextures"
#
#Display Settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
PRETTYCOLOR = ( 232, 181,189)
#Border Constants
NEGATIVE_X_BORDER = -2500
NEGATIVE_Y_BORDER = -500
POSITIVE_X_BORDER = 2500
POSITIVE_Y_BORDER = 2500

# frame size for base player sheet, this is mostly the same for each sprite
FRAME_W = 192
FRAME_H = 192
# frame size for Title & Menu 
TITLEF_W = 512
TITLEF_H = 512
TITLE_GLIMMER_FRAMES=0
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
# Player Values, 
PSpeed = 5
PHealth = 20
PAttackDmg = 3
PReach = 50
# Base Constants 
BASE_HEALTH = 30
BaseHealth = BASE_HEALTH
#Enemy values
ESpeed = 3.8
EHealth = 12
EAttackDmg = 5

#




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


#loading title image - made this after looking at load_animation() for a very long time.
def loadtitle_image(path,TITLEF_W,TITLEF_H):
    titleimage = pygame.image.load(path)
    loadedimage = titleimage
    print("I have loaded the image")
    return loadedimage  # adding ,TITLE_GLIMMER_FRAME would be apart of the animation code later on.



#Handling animation for each sprite - after looking over this for a couple days im starting to understand it.

def load_animation(path, frame_w, frame_h, num_frames, row=0, spacing_x=0, margin_x=0): # animation helper
    # animation worker, works as such, we create the following variables in the function parameters above 
    sheet = pygame.image.load(path).convert_alpha()
    #here is where we are creating the animation sheet, at this point we ONLY have the whole row out
    frames = []
    #here we make the list of the frames, keeping tabs of what frame we are on
    print(f"Animation active, current {frames[0]}")
    x = margin_x # this is how we determine which frame to be on, (16,16) would be frame[0] , (32,16) would be frame [2 at this point]
    y = row * frame_h # if we had different animations under this png,this code might break. 
    for _ in range(num_frames):
        rect = pygame.Rect(x, y, frame_w, frame_h)
        frames.append(sheet.subsurface(rect).copy())
        x += frame_w + spacing_x
    return frames
    # the for loop has finished, are frame would be as such for reference
    # look at wizard_idle.png for exact refrence
    # (16,16) would be frame[0] , (32,16) would be frame [2] etc.
#Each animation is loaded in a list and attached to a string, 


images = {
    "title_image": loadtitle_image(os.path.join(title_dir,"title_placeholder.png"),TITLEF_W, TITLEF_H)
    "gameover": loadtitle_image(os.path.join(title_dir,"gameover_placeholder.png"), TITLEF_W, TITLEF_H)

# TODO: Each sprite is gonna be different later on im pretty sure, adjust FRAME_W and FRAME_H instead of being a const. const -> variable
}

animations = {
    "wizard_idle": load_animation(os.path.join(wizard_dir, "Idle.png"), FRAME_W, FRAME_H, WIZARD_IDLE_FRAMES),
    "wizard_run" : load_animation(os.path.join(wizard_dir, "Run.png"),  FRAME_W, FRAME_H, WIZARD_RUN_FRAMES),
    "enemy_idle": load_animation(os.path.join(enemy_dir, "Warrior_Idle.png"), FRAME_W, FRAME_H, ENEMY_IDLE_FRAMES),
    "enemy_run": load_animation(os.path.join(enemy_dir, "Warrior_Run.png"), FRAME_W, FRAME_H, ENEMY_RUN_FRAMES),
    "enemy_attack1": load_animation(os.path.join(enemy_dir, "Warrior_Attack1.png"), FRAME_W, FRAME_H, ENEMY_ATTACK_FRAMES),
    "enemy_attack2": load_animation(os.path.join(enemy_dir, "Warrior_Attack2.png"), FRAME_W, FRAME_H, ENEMY_ATTACK_FRAMES),
  #  "title_glimmer": load_animation(os.path.join(title_dir,title_glimmer.png),TITLEF_W, TITLEF_H, TITLE_GLIMMER_FRAMES)
  #TODO:
  #Create animated Picture, roughly 16 frames? It says Wild Waves, Wild as Greenery, Waves as an ocean-like bubbly text. the water would flow for the animation 
  #Create title_glimmer.png & title_dir 
  #Create TITLEF_W, TITLEF_H, TITLE_GLIMMER_FRAMES const 
  #
  #

  #
}

# Animation Speed - Higher = Slower Animation, Lower = Faster Animation
anim_speed_ms = { 
    "wizard_idle": 100,   # ~10 FPS
    "wizard_run" : 70,    # ~14 FPS (snappier)
    "enemy_idle" : 100,
    "enemy_run" : 70,
    "enemy_attack1" : 50,
    "enemy_attack2" : 60,
  #  "title_glimmer" : 80 # fps for title

}
#


#End of animation code
#Camera Code
class PlayerCamera:
    """
    Camera class that follows the player.
    
    Concept: The camera represents a "window" into the game world. When the player
    moves, the camera follows them so the player stays centered on screen. When drawing
    sprites, we subtract the camera position to convert world coordinates to screen coordinates.
    """
    def __init__(self):
        """Initialize camera at position (0, 0) - top-left corner of the world."""
        self.x = 0  # Camera's x position in the world
        self.y = 0  # Camera's y position in the world
    
    def update(self, target_rect):
        """
        Update camera position to follow the target (usually the player).
        Args:
            target_rect: pygame.Rect of the object to follow (player's rect)
        """
        # Get the center of the target (player)
        target_center_x = target_rect.centerx
        target_center_y = target_rect.centery
        
        # Center the camera on the target
        # Camera position = target position - half screen size
        self.x = target_center_x - SCREEN_WIDTH // 2
        self.y = target_center_y - SCREEN_HEIGHT // 2
    
    def apply(self, rect):
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            rect: pygame.Rect in world coordinates
        
        Returns:
            pygame.Rect: A new rect positioned for screen drawing
        Concept: To draw something at world position (x, y), we subtract the camera
        position to get where it should appear on screen.
        """
        return rect.move(-self.x, -self.y)
    
    def get_offset(self):
        """
        Get the camera offset as a tuple (x, y).
        Useful for manual position calculations.
        
        Returns:
            tuple: (camera_x, camera_y) offset values
        """
        return (self.x, self.y)
    







#

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

    def _handle_movement(self, keys):
        """
        Handle player movement based on keyboard input.
        Returns True if player is moving, False otherwise.
        
        Concept: After applying movement, we clamp the player's position to ensure
        the entire sprite stays within the world boundaries defined by the border constants.
        """
        moving = False
        # Apply movement based on key input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= PSpeed
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += PSpeed
            moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= PSpeed
            self.facing_left = True
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += PSpeed
            self.facing_left = False
            moving = True
        
        # Clamp player position to stay within world boundaries
        # We subtract PLAYER_WIDTH/HEIGHT to ensure the entire sprite stays within bounds
        self.rect.x = max(NEGATIVE_X_BORDER, min(POSITIVE_X_BORDER - PLAYER_WIDTH, self.rect.x))
        self.rect.y = max(NEGATIVE_Y_BORDER, min(POSITIVE_Y_BORDER - PLAYER_HEIGHT, self.rect.y))
        
        # max X and Y values player can go. (2308,2308) and (-2500,-500)
        #TODO: recenter the player at the middle value of this 

        return moving
    def _handle_input(self, keys):
        """Handle non-movement keyboard input (actions, debug, etc.)."""
        if keys[pygame.K_SPACE]:
            print("I have attacked!")
           # print(f"Ouch! I've taken {EAttackDmg} I am now at {PHealth}")
        if keys[pygame.K_F1]:
            print("The Game has been changed to playing")
        if keys[pygame.K_o]:
            print(f"This is ur Current Player Stats,\n{PHealth}HP\n{PSpeed}m/s\n{PAttackDmg}")
        if keys[pygame.K_LSHIFT] or keys[pygame.K_LCTRL]:
            print(f"Dash Is Being consumed")
            # Dash()
        if keys[pygame.K_F2]:
            print(f"Player is at {self.rect.x} and {self.rect.y}")
            print(f"The cursor is at ")
        # TODO: Add detection on where mouse is clicked and make player face that way 
        # TODO: Add check if been hit, if true then highlight character red AND take away subtract Damage from PlayerHealth 
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
    
    def draw(self, surface, camera=None):
        """
        Draw the player sprite to the given surface.
        
        Args:
            surface: The pygame surface to draw on
            camera: Optional PlayerCamera instance. If provided, applies camera offset.
        """
        if camera:
            # Apply camera offset to convert world position to screen position
            screen_rect = camera.apply(self.rect)
            surface.blit(self.image, screen_rect)
        else:
            # Draw without camera (for menu or fixed positions)
            surface.blit(self.image, self.rect)
#
class MainMenu: 
    def __init__(self):
        self.title = "title_image"
        self.image = self.title
      #  self.rect = self.image.get_rect()
        self._create_buttons()  # Initialize buttons when menu is created

    def title_image(self, name): # animation of game title handled here
         
        pass
    
    def _create_buttons(self):
        """Initialize the menu buttons (Play, Load, Quit)."""
        # Button dimensions - using constants to avoid magic numbers
        button_width = 200
        button_height = 60
        button_spacing = 80  # Space between buttons
        
        # Calculate starting y position to center buttons vertically
        start_y = SCREEN_HEIGHT // 2
        button_x = (SCREEN_WIDTH - button_width) // 2  # Center horizontally
        
        # Create button list with their positions and text
        self.buttons = []
        button_texts = ["Play", "Load", "Quit"]
        
        for index, text in enumerate(button_texts):
            button_y = start_y + (index * (button_height + button_spacing))
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.buttons.append({
                "text": text,
                "rect": button_rect,
                "hovered": False
            })
    
    def _check_button_hover(self, mouse_pos):
        """Check if mouse is hovering over any button and update hover state."""
        for button in self.buttons:
            button["hovered"] = button["rect"].collidepoint(mouse_pos)
    
    def _handle_button_click(self, mouse_pos):
        """Handle button clicks and return the action to perform."""
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["text"]
        return None
    
    def _draw_buttons(self, surface):
        """Draw all menu buttons with hover effects."""
        for button in self.buttons:
            # Choose color based on hover state
            if button["hovered"]:
                button_color = (100, 150, 200)  # Lighter blue when hovered
            else:
                button_color = (50, 100, 150)  # Darker blue when not hovered
            
            # Draw button rectangle
            pygame.draw.rect(surface, button_color, button["rect"])
            pygame.draw.rect(surface, (0, 0, 0), button["rect"], 3)  # Black border
            
            # Draw button text
            font = pygame.font.Font(None, 36)
            text_surface = font.render(button["text"], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            surface.blit(text_surface, text_rect)
    
    def _draw_title(self, surface):
        """Draw the game title image."""
        if self.title in images:
            title_image = images[self.title]
            title_x = (SCREEN_WIDTH - title_image.get_width()) // 2
            title_y = 100  # Position title near top of screen
            surface.blit(title_image, (title_x, title_y))
    
    def handle_event(self, event):
        """Handle menu events (mouse clicks, hover)."""
        if event.type == pygame.MOUSEMOTION:
            self._check_button_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                return self._handle_button_click(event.pos)
        return None
    
    def draw(self, surface):
        """Draw the entire main menu (title and buttons)."""
        self._draw_title(surface)
        self._draw_buttons(surface)

Player = MainPlayer()
Menu1 = MainMenu()
Camera = PlayerCamera()

# Game state management
# "menu" = showing main menu, "playing" = game is active, "gameover" = game over screen, only met once player health or base health = 0
game_state = "menu"

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "menu":
            # Handle menu events (button clicks, hover)
            action = Menu1.handle_event(event)
            if action == "Play":
                game_state = "playing"
            elif action == "Quit":
                running = False
            # "Load" button can be handled later when save/load is implemented
        elif game_state == "playing":
            # Handle game events (like Escape to return to menu)
            if event.type == pygame.KEYDOWN:  # checks if a key is pressed down
                if event.key == pygame.K_ESCAPE: #  checks if the key is the escape key
                    game_state = "menu" # executes code if the escape key is pressed
            if event.type == pygame.KEYDOWN:  # checks if a key is pressed down
                if event.key == pygame.K_F4: #  checks if the key is the escape key
                    PHealth -= EAttackDmg
                    print(f"Ouch! I've taken {EAttackDmg} I am now at {PHealth}")
            if PHealth <= 0 or BaseHealth <= 0:
                game_state = "over"
    #TODO: once enemies & projectiles are added, ensure pressing this freezes everything!!!


    # Clear screen ensures no ghosting is happening 
    screen.fill(PRETTYCOLOR)
    
    # Update and draw based on current game state
    if game_state == "menu":
        # Draw the main menu
        Menu1.draw(screen)
        
    elif game_state == "playing":
        # Update player state, this handles movement, animation, input etc. 
        Player.update()
        # Update camera to follow the player
        Camera.update(Player.rect)
        # Draw Player onto screen with camera offset
        Player.draw(screen, Camera)
    if game_state == "over":
        print("Game Over Screen is Drawn")
        #pygame.time.wait(10)
        game_state == "menu"
        #TODO: Add score function right here
        #Draw the menu
        Menu1.draw(screen)
        Menu1.handle_event(event)
    # Update display
    pygame.display.update()
    
    # Control frame rate
    clock.tick(60)

pygame.quit()