word = "hello"

import pygame, sys, math, random

def DRAW():
    # BG
    win.fill(WHITE)

    # Title
    text = TITLE_FONT.render("Guess The Word !", True, BLACK)
    rect = text.get_rect(center = (WIDTH//2, 25))
    win.blit(text, rect)

    # Butttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            text = LETTER_FONT.render(ltr, True, BLACK)
            rect = text.get_rect(center = (x,y))
            win.blit(text, rect)
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3)

    # Word
    display_word = ""
    for letter in word:
        if letter in guessed: display_word += letter + "  "
        else: display_word += "_  "

    text = WORD_FONT.render(display_word, True, BLACK)
    rect = text.get_rect(center = (3*WIDTH//4, HEIGHT//3))
    win.blit(text, rect)
        
    # Hangman
    win.blit(images[hangman_status],(100,50))
    
    # Update
    pygame.display.update()
    clock.tick(60)

def disp(msg):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(f"You {msg} !!!", True, BLACK)
    rect = text.get_rect(center = (WIDTH//2, HEIGHT//2))
    win.blit(text, rect)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Setup
pygame.init()
clock = pygame.time.Clock()

# Screen
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# Font
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Images
images = []
for i in range(7):
    img = pygame.image.load(f"Data/hangman" + str(i) + ".png")
    images.append(img)

# Buttons
RADIUS = 20
GAP = 15
letters = []
start_x = (WIDTH - (RADIUS * 2 + GAP) * 13 ) // 2
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 +((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS*2))
    letters.append([x, y, chr(A + i), True])

# Game Variables
hangman_status = 0
word = word.upper()
guessed = []

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    distance = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                    if distance < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word: hangman_status += 1

    DRAW()

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won: disp("WON")
    if hangman_status == 6: disp("LOST")
