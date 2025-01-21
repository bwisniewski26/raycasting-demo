import pygame
import sys
import math


SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 32
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 30
MAX_DEPTH = 16 * TILE_SIZE
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS
FORWARD = False

player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

WORLD_MAP = (
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
    'W                              W'
    'W   W   W   W   W     W        W'
    'W   W   W   W   W     W   WWWWWW'
    'W       W       W         WW   W'
    'W       W   W   W         WW   W'
    'WWWWWWWW   W   WWWWWWWWWW  WW  W'
    'W           W              WW  W'
    'W   WWWWWWWWWWWWWWWWWWWWWWWW  WW'
    'W   W                         WW'
    'W   W   W                    WWW'
    'W   W   W                    WWW'
    'W       W              WWW     W'
    'W       W              WWW     W'
    'WW   WWWWWWWWWW   WWWWWWW      W'
    'W          WW                  W'
    'W   W   WWWWWWW    WWWWWWWWWWWWW'
    'W   W                        WWW'
    'W   W   WWW   W                W'
    'W       W   W                WWW'
    'W       W       W   WWW    W   W'
    'WWWWWWWWWMMWWWM   WW    WWW   WW'
    'W                        WWW   W'
    'W   WWWWWMMWWWMWWWWWWWWWWWWW   W'
    'W   W          WW              W'
    'W   W   W                    WWW'
    'W       W   W      W         WWW'
    'W       W          W         WWW'
    'WWWWWWWWWWWWWWWWWWWWW      WW WW'
    'W                     WW       W'
    'WWW  WWW         WWWWWWW     WWW'
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
)



pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Przykład raycastingu')
clock = pygame.time.Clock()
wall_texture = pygame.image.load("wall.png").convert()

def draw_textured_wall(x, y, texture, wall_height, column_offset):
    # Wycinanie odpowiedniego fragmentu tekstury
    texture_width, texture_height = texture.get_size()
    texture_x = int(column_offset * texture_width)
    texture_slice = texture.subsurface((texture_x, 0, 1, texture_height))

    # Skalowanie fragmentu do wysokości ściany
    texture_slice = pygame.transform.scale(texture_slice, (int(SCALE), int(wall_height * 2)))

    # Rysowanie tekstury
    win.blit(texture_slice, (x, y - wall_height))

def draw_map(player_x, player_y, key):    

    empty = (0, 0, 0)
    wall = (65, 255, 0)
    door = (255, 255, 0)

    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):            

            square = i * MAP_SIZE + j
        
            pygame.draw.rect(win, 
                wall if WORLD_MAP[square] == 'W' else (door if WORLD_MAP[square] == 'M' else empty),                
                (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
            pygame.draw.circle(win, (162, 0, 255), (int(player_x), int(player_y)), 5)
    
    start_angle = player_angle - HALF_FOV
    pygame.draw.rect(win, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))    
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    for ray in range(CASTED_RAYS):        
        for depth in range(MAX_DEPTH):            
           
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y +  math.cos(start_angle) * depth
            

            col = int(target_x / TILE_SIZE)           
            row = int(target_y / TILE_SIZE)  
          
            square = row * MAP_SIZE + col                        
              
            color = 255 / (1 + depth * depth * 0.001)

            wall_height = 21000 / (5 * depth + 0.0001)

            if WORLD_MAP[square] == 'W':
                column_offset = (target_x % TILE_SIZE) / TILE_SIZE
                draw_textured_wall(SCREEN_HEIGHT + ray * SCALE, SCREEN_HEIGHT / 2, wall_texture, wall_height, column_offset)
                pygame.draw.rect(win, (197, 137, 38), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
                pygame.draw.line(win, (233, 166, 49), (player_x, player_y), (target_x, target_y))                      
                break
    
            if WORLD_MAP[square] == 'M':
                pygame.draw.rect(win, door,
                (SCREEN_HEIGHT + ray * SCALE,
                (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))                             

                pygame.draw.rect(win, (197, 137, 38), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
                pygame.draw.line(win, (233, 166, 49), (player_x, player_y), (target_x, target_y))                                
                break
            
      
        start_angle += STEP_ANGLE
        
def is_wall(x, y):
    col = int(x / TILE_SIZE)
    row = int(y / TILE_SIZE)
    square = row * MAP_SIZE + col

    return 0 <= square < len(WORLD_MAP) and WORLD_MAP[square] == 'W'

def can_move(x, y):
    return not is_wall(x, y)


while True:    
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:            
            pygame.quit()
            sys.exit(0)
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))
   
    keys = pygame.key.get_pressed()
   
    if keys[pygame.K_LEFT]:             
        player_angle -= 0.1
    elif keys[pygame.K_RIGHT]:        
        player_angle += 0.1    
    elif keys[pygame.K_UP]:   
        new_x = player_x + (-1 * math.sin(player_angle) * 5) / 4
        new_y = player_y + (math.cos(player_angle) * 5) / 4
        if can_move(new_x, new_y):
            player_x = new_x
            player_y = new_y
    elif keys[pygame.K_DOWN]:        

        new_x = player_x - (-1 * math.sin(player_angle) * 5) / 4
        new_y = player_y - (math.cos(player_angle) * 5) / 4
        
        if can_move(new_x, new_y):
            player_x = new_x
            player_y = new_y
    draw_map(player_x, player_y, keys)
 
    clock.tick(60)
    fps = str(int(clock.get_fps()))    
    font = pygame.font.SysFont('Arial', 30)    
    fpssurface = font.render(fps, False, (255, 255, 255))    
    win.blit(fpssurface, (int(SCREEN_WIDTH / 2), 0))
    pygame.display.flip()