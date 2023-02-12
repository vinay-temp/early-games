import pygame
import sys
import random
from manage_shapes import shapes
from all_colors import *

pygame.init()
clock = pygame.time.Clock()

W = 700
H = 700

play_width = 300
play_height = 600
size = 30
top_left_x = (W - play_width)//3
top_left_y = (H - play_height)//2

shape_colors = [green, red, cyan, yellow, orange, blue, purple]

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Tetris')

class Piece(object):
    def __init__(self, shape):
        self.x = 2
        self.y = -3
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = random.randint(0, 4)

def create_grid(locked_pos):
    grid = [[grey for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    
    formatt = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(formatt):
        for j, col in enumerate(line):
            if col == '0':
                positions.append((shape.x + j, shape.y + i))

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i ) for j in range(10) if grid[i][j] == grey] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > 1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if grey not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except: continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', True, white)
    label_rect = label.get_rect(center = (4*W//5, 2*H//5))
    
    formatt = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(formatt):
        for j, col in enumerate(line):
            if col == '0':
                pygame.draw.rect(surface, shape.color, (7*W//10 + j*size, H//5 + i*size , size, size), 0)
    surface.blit(label, label_rect)

def draw_text_middle(surface, text, size, color):
    surface.fill(dark_grey)
    font = pygame.font.SysFont('comicsans', 30, bold = True)
    label = font.render(text, 1, color)
    label_rect = label.get_rect(center = (W//2, H//2))
    surface.blit(label, label_rect)

def draw_window(screen, grid, score):
    screen.fill(dark_grey)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (top_left_x + j*size, top_left_y + i*size , size, size), 0)

    pygame.draw.rect(screen, current_piece.color, (top_left_x, top_left_y, play_width, play_height), 3)
    
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), True, (255,255,255))
    label_rect = label.get_rect(center = (4*W//5, 2*H//4))
    screen.blit(label, label_rect)

def draw_screen():
    while True:
        draw_text_middle(screen, 'Press Any Key...', 100, black)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
# draw_screen()


locked_pos = {}
change_piece = False

current_piece = Piece(random.choice(shapes))
next_piece = Piece(random.choice(shapes))

score = 0

FALL_EVENT = pygame.USEREVENT
pygame.time.set_timer(FALL_EVENT, 100)

while True:
    grid = create_grid(locked_pos)
    shape_pos = convert_shape_format(current_piece)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == FALL_EVENT:
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if not(valid_space(current_piece, grid)):
                    current_piece.x += 1
            if event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if not(valid_space(current_piece, grid)):
                    current_piece.x -= 1
            if event.key == pygame.K_DOWN:
                current_piece.y += 1
                if not(valid_space(current_piece, grid)):
                    current_piece.y -= 1
            if event.key == pygame.K_UP:
                current_piece.rotation += 1
                if not(valid_space(current_piece, grid)):
                    current_piece.rotation -= 1
            
            if event.key == pygame.K_SPACE:
                pass

    for i in range(len(shape_pos)):
        x, y = shape_pos[i]
        if y > -1: grid[y][x] = current_piece.color

    if change_piece:
        for pos in shape_pos:
            locked_pos[(pos[0], pos[1])] = current_piece.color

        current_piece = next_piece
        next_piece = Piece(random.choice(shapes))
        
        change_piece = False
        score += clear_rows(grid, locked_pos) * 10
        score += 10

    if check_lost(locked_pos):
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    draw_window(screen, grid, score)
    draw_next_shape(next_piece, screen)
    
    clock.tick(70)
    pygame.display.update()
