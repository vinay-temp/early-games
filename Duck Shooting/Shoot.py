import pygame, sys, random

# Setup
pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Screen
width, height = 1024,512
screen = pygame.display.set_mode((width,height))

# Surfaces
wood_bg = pygame.transform.scale(pygame.image.load('./Data/Stall/bg_blue.png'), (width,height))
land_bg =  pygame.transform.scale(pygame.image.load('Data/Stall/grass1.png'), (width,height//4))
water_bg = pygame.transform.scale(pygame.image.load('Data/Stall/water1.png'), (width,height//4))
cloud1 = pygame.transform.scale(pygame.image.load('Data/Stall/cloud1.png'), (100,50))
cloud2 = pygame.transform.scale(pygame.image.load('Data/Stall/cloud2.png'), (100,50))
crosshair = pygame.image.load('Data/HUD/crosshair_white_small.png')
duck_brown = pygame.image.load('Data/Objects/duck_brown.png')
duck_yellow = pygame.image.load('Data/Objects/duck_yellow.png')
duck_white = pygame.image.load('Data/Objects/duck_white.png')
duck_surfaces = [duck_brown, duck_yellow, duck_white]

# Font
game_font = pygame.font.Font(None, 60)
text_surface  = game_font.render('You Won !!!', True, (255,255,255))
text_rect = text_surface.get_rect(center = (width//2, height//2))

# Positions and Speed
land_pos = 400    ;    land_speed = 1
water_pos = 450    ;    water_speed = 1
cloud_pos = 0    ;    cloud_speed = 2

# Duck rectangles
duck_list = []
for i in range(20):
    duck_pos_x = random.randint(50, 980)
    duck_pos_y = random.randint(50, 350)
    duck_rect = duck_white.get_rect(center =(duck_pos_x, duck_pos_y))
    duck_list.append(duck_rect)

# Game Loop
while True:
    for event in pygame.event.get():
        
        # Exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Crosshair Rectangle
        if event.type == pygame.MOUSEMOTION:
            crosshair_rect = crosshair.get_rect(center = event.pos)
            
        # Destroy Duck
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index,duck_rect in enumerate(duck_list):
                if duck_rect != '':
                    if duck_rect.collidepoint(event.pos):   #crosshair_rect.colliderect(duck_rect):
                        del duck_list[index]
                        duck_list.insert(index,'')
            
    # Back Ground
    screen.blit(wood_bg, (0,0))

    # Land
    land_pos -= land_speed
    if land_pos <=  390 or land_pos >= 410: land_speed *= -1
    screen.blit(land_bg,(0, land_pos))

    # Water
    water_pos += water_speed
    if water_pos <=  430 or water_pos >= 470: water_speed *= -1
    screen.blit(water_bg,(0,water_pos))

    # Ducks
    for index,duck_rect in enumerate(duck_list):
        if duck_rect != '':
            screen.blit(duck_surfaces[index%3],duck_rect)

    # Cross Hair
    screen.blit(crosshair,crosshair_rect)
    
    # Clouds
    cloud_pos += cloud_speed
    if cloud_pos <= -20 or cloud_pos >= 20: cloud_speed *= -1
    screen.blit(cloud1,(100 + cloud_pos, 30))
    screen.blit(cloud1,(500 + cloud_pos,10))
    screen.blit(cloud1,(300 + cloud_pos, 30))
    screen.blit(cloud2,(700 + cloud_pos, 70))
    screen.blit(cloud2,(150 + cloud_pos, 80))
    screen.blit(cloud1,(900 + cloud_pos, 20))

    #Text
    for i in duck_list:
        if i != '':
            win = 0
            break
        else: win = 1
    if win : screen.blit(text_surface,text_rect)
    
    # Update
    pygame.display.update()
    clock.tick(120)
