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
# Non Dynamic Images 
background_image = pygame.image.load(os.path.join(terrain_assests_dir,"Background.png"))
tile_image = pygame.image.load(os.path.join(tile_dir,"Tilemap_color4.png"))
# Water textures
water_tile = pygame.image.load(os.path.join(terrain_assests_dir, "Water Background color.png")).convert()
# foam strip/sheet; update the filename to your asset
water_foam_sheet = pygame.image.load(os.path.join(terrain_assests_dir, "waterfoam.png")).convert_alpha()

BORDER_THICKNESS = 192
TILE_SIZE = 192
TILE_OVERLAP = 16
TILE_STEP = TILE_SIZE - TILE_OVERLAP
# land extends one tile further toward the water
LAND_MARGIN = max(0, BORDER_THICKNESS - TILE_SIZE)
# land rectangle used by fade and collisions
LAND_RECT = pygame.Rect(
    LAND_MARGIN, LAND_MARGIN,
    SCREEN_WIDTH - 2 * LAND_MARGIN,
    SCREEN_HEIGHT - 2 * LAND_MARGIN
)
def get_rect_tile(sheet, x, y, w, h):
    return sheet.subsurface(pygame.Rect(x, y, w, h)).copy()
# Ground tile (top-left)
ground_tile = get_rect_tile(tile_image, 0 * 192, 0 * 192, 192, 192)

# Top-left tile (192x192) from the tileset
single_tile_image = get_rect_tile(tile_image, 0, 0, 192, 192)
# DAMAGE CONSTANTS YIPPPIEEE
WATER_DAMAGE = 2
WATER_DAMAGE_INTERVAL_MS = 800 
last_water_damage_ms = 0
def touching_water(rect):
    # Inside land?
    if LAND_RECT.contains(rect):
        return False
    # In the shoreline fade band (slightly larger than land)?
    band_rect = LAND_RECT.inflate(GROUND_FEATHER * 2, GROUND_FEATHER * 2)
    return band_rect.colliderect(rect)
def apply_water_damage(now_ms):
    global MainHealth, last_water_damage_ms
    if touching_water(Player.rect):
        if now_ms - last_water_damage_ms >= WATER_DAMAGE_INTERVAL_MS:
            MainHealth = max(0, MainHealth - WATER_DAMAGE)
            last_water_damage_ms = now_ms
            print(f"Water hurts! HP: {MainHealth}")


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
PLAYER_WIDTH = PLAYER_HEIGHT

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

# Water Code, need this broken down to make it easier to understand
def load_strip(sheet, frame_w, frame_h, num_frames, spacing_x=0, margin_x=0):
    frames = []
    x = margin_x
    for _ in range(num_frames):
        rect = pygame.Rect(x, 0, frame_w, frame_h)
        frames.append(sheet.subsurface(rect).copy())
        x += frame_w + spacing_x
    return frames
# Foam animation config (set to your sheet)
FOAM_W = 64
FOAM_H = 64
FOAM_FRAMES = 16
FOAM_FPS = 8
FOAM_STEP = 96           # spacing to consider emitter slots along edges
FOAM_CHANCE = 0.35       # chance to place an emitter at a slot
FOAM_COOLDOWN_RANGE = (1200, 3500)  # ms between bursts
# Foam animation setup

foam_frames = load_strip(water_foam_sheet, FOAM_W, FOAM_H, FOAM_FRAMES)
foam_rot_left  = [pygame.transform.rotate(f, 90)  for f in foam_frames]
foam_rot_right = [pygame.transform.rotate(f, -90) for f in foam_frames]
foam_flip_bot  = [pygame.transform.flip(f, False, True) for f in foam_frames]



def tile_fill(surface, img, rect):
    iw, ih = img.get_width(), img.get_height()
    x0, y0, w, h = rect
    for y in range(y0, y0 + h, ih):
        for x in range(x0, x0 + w, iw):
            surface.blit(img, (x, y))

def draw_water_border():
    WATER_OUTER_MARGIN = TILE_SIZE * 2  # adjust later
    
    # Four border rectangles (outer to inner ring)
    top_rect    = (0, 0, SCREEN_WIDTH, BORDER_THICKNESS)
    bottom_rect = (0, SCREEN_HEIGHT - BORDER_THICKNESS, SCREEN_WIDTH, BORDER_THICKNESS)
    left_rect   = (0, 0, BORDER_THICKNESS, SCREEN_HEIGHT)
    right_rect  = (SCREEN_WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, SCREEN_HEIGHT)

    tile_fill(screen, water_tile, top_rect)
    tile_fill(screen, water_tile, bottom_rect)
    tile_fill(screen, water_tile, left_rect)
    tile_fill(screen, water_tile, right_rect)

#Character Abilities, to start, Dash, Magic Missle, Thunder Storm (finds enemies in radius around player, casts a lighting bolt on them, 60 second cooldown)

#   
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
        # precompute land bounds
        LAND_LEFT = LAND_MARGIN
        LAND_TOP = LAND_MARGIN
        LAND_RIGHT = SCREEN_WIDTH - LAND_MARGIN
        LAND_BOTTOM = SCREEN_HEIGHT - LAND_MARGIN
        move_bounds = LAND_RECT.inflate(GROUND_FEATHER, GROUND_FEATHER)

        Keys = pygame.key.get_pressed()
        moving = False
        # precompute movement bounds each update

        if Keys[pygame.K_w] or Keys[pygame.K_UP]:
            Player.rect.y = max(Player.rect.y - MainSpeed, move_bounds.top)
            moving = True
        if Keys[pygame.K_s] or Keys[pygame.K_DOWN]:
            Player.rect.y = min(Player.rect.y + MainSpeed, move_bounds.bottom - PLAYER_HEIGHT)
            moving = True
        if Keys[pygame.K_a] or Keys[pygame.K_LEFT]:
            Player.rect.x = max(Player.rect.x - MainSpeed, move_bounds.left)
            self.facing_left = True
            moving = True
        if Keys[pygame.K_d] or Keys[pygame.K_RIGHT]:
            Player.rect.x = min(Player.rect.x + MainSpeed, move_bounds.right - PLAYER_WIDTH)
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
            #Dash()

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
    def draw(self, surface): # this is what is layered over the background
        surface.blit(self.image, self.rect) # character is drawn

class Enemy:
      def __init__(self):
            
            pass


#    ~ Understanding better why Classes are needed in games, couldn't imagine defining these variables over and over again. ~
class WaterEmitter:
    def __init__(self, x, y, frames, fps):
        self.x = x
        self.y = y
        self.frames = frames
        self.fps = fps
        self.delay = int(1000 / fps)
        self.frame = 0
        self.last = 0
        self.active = False
        self.next_start = 0

    def schedule_next(self, now):
        wmin, wmax = FOAM_COOLDOWN_RANGE
        self.next_start = now + random.randint(wmin, wmax)

    def start(self, now):
        self.active = True
        self.frame = 0
        self.last = now

    def update(self, now):
        if not self.active:
            if now >= self.next_start:
                self.start(now)
            return
        if now - self.last >= self.delay:
            self.last = now
            self.frame += 1
            if self.frame >= len(self.frames):
                self.active = False
                self.schedule_next(now)
                self.frame = 0

    def draw(self, surface):
        if self.active:
            surface.blit(self.frames[self.frame], (self.x, self.y))

 #

# More Water Code, really interesting but im not there yet 
emitters = []

def init_water_emitters():
    emitters.clear()
    now = pygame.time.get_ticks()

    inner_x0 = LAND_MARGIN
    inner_y0 = LAND_MARGIN
    inner_x1 = SCREEN_WIDTH  - LAND_MARGIN
    inner_y1 = SCREEN_HEIGHT - LAND_MARGIN

    # top edge (emit just inside the inner edge)
    y_top = inner_y0 - FOAM_H // 2
    for x in range(inner_x0, inner_x1, FOAM_STEP):
        if random.random() < FOAM_CHANCE:
            e = WaterEmitter(x, y_top, foam_frames, FOAM_FPS)
            e.schedule_next(now)
            emitters.append(e)

    # bottom edge
    y_bot = inner_y1 - FOAM_H // 2
    for x in range(inner_x0, inner_x1, FOAM_STEP):
        if random.random() < FOAM_CHANCE:
            e = WaterEmitter(x, y_bot, foam_flip_bot, FOAM_FPS)
            e.schedule_next(now)
            emitters.append(e)

    # left edge
    x_left = inner_x0 - FOAM_W // 2
    for y in range(inner_y0, inner_y1, FOAM_STEP):
        if random.random() < FOAM_CHANCE:
            e = WaterEmitter(x_left, y, foam_rot_left, FOAM_FPS)
            e.schedule_next(now)
            emitters.append(e)

    # right edge
    x_right = inner_x1 - FOAM_W // 2
    for y in range(inner_y0, inner_y1, FOAM_STEP):
        if random.random() < FOAM_CHANCE:
            e = WaterEmitter(x_right, y, foam_rot_right, FOAM_FPS)
            e.schedule_next(now)
            emitters.append(e)

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

#Tile Code, for the time being this will be used to create the map, but we will need to add a way to create the map dynamically later on
tiles_ground = []

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image


def create_ground():
    tiles_ground.clear()
    start_x = -TILE_OVERLAP
    start_y = -TILE_OVERLAP
    end_x = SCREEN_WIDTH + TILE_SIZE
    end_y = SCREEN_HEIGHT + TILE_SIZE
    for y in range(start_y, end_y, TILE_STEP):
        for x in range(start_x, end_x, TILE_STEP):
            tiles_ground.append(Tile(x, y, ground_tile))

def tile_draw_ground():
    for tile in tiles_ground:
        screen.blit(tile.image, tile)

# choose a single tile from the tileset by grid coordinate
def get_tile(sheet, col, row, tile_size=TILE_SIZE):
    rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
    return sheet.subsurface(rect).copy()
# Smooth fade from ground into water
GROUND_FEATHER = 8
def create_ground_surface():
    # draw all ground tiles to an off-screen surface
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
    for t in tiles_ground:
        surf.blit(t.image, t)

    # build a soft alpha mask: full alpha in the center, fades to 0 near edges
    mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
    mask.fill((255, 255, 255, 0))

    inner = pygame.Rect(
        BORDER_THICKNESS, BORDER_THICKNESS,
        SCREEN_WIDTH - 2 * BORDER_THICKNESS,
        SCREEN_HEIGHT - 2 * BORDER_THICKNESS
    )

    # solid center
    pygame.draw.rect(mask, (255, 255, 255, 255), inner)

    # feather ring: draw expanding rects with increasing alpha
    for i in range(GROUND_FEATHER):
        a = int(255 * (i + 1) / (GROUND_FEATHER + 1))  # 0→255 ramp
        r = inner.inflate(2 * (i + 1), 2 * (i + 1))
        pygame.draw.rect(mask, (255, 255, 255, a), r, width=GROUND_FEATHER - i)

    # multiply ground by mask alpha for smooth edge
    surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return surf

# call after create_ground()
ground_surface = None

# pick which tile you want (set these to the desired tile position in the PNG)
CHOSEN_TILE_COL = 0  # change to your column
CHOSEN_TILE_ROW = 0  # change to your row
single_tile_image = get_tile(tile_image, CHOSEN_TILE_COL, CHOSEN_TILE_ROW)


#Establishing a variable for classes
Player = MainPlayer()
WaveEnemy = Enemy()
tiles_ground = []
create_ground()
ground_surface = create_ground_surface()
init_water_emitters()
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
        now = pygame.time.get_ticks()
        for e in emitters:
            e.update(now)
        #screen.blit(background_image,(0,0)) # background first, color incase anything bleeds through. 
        # draw ring of water 
        draw_water_border()
        # 3) land (precomposed with smooth fade)
        screen.blit(ground_surface, (0, 0))
        #random foam animation
        for e in emitters:
            e.draw(screen)
    
        Player.update() # player.update() handles the player animation and movement, calling it first begins the animation process. SUCH BELOW HERE HANDLES SOME COOL STUFF HEHE
        
        apply_water_damage(now)
        Player.draw(screen) # finally, draw the player
        if MainHealth == 0:
            print("I AM DEAD!")

    pygame.display.flip() # need this everytime to update the screen with what my code is doing
    clock.tick(60)  # FPS 60

pygame.quit()