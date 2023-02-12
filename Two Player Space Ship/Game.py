import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsans", 40)
win_font = pygame.font.SysFont("comicsans", 100)
shoot = pygame.mixer.Sound("Assets/sfx_laser1.ogg")
hit = pygame.mixer.Sound("Assets/sfx_lose.ogg")

FPS = 60
Grey = (50, 50, 50)
White = (250, 250, 250)
Yellow_color = (250, 250, 0)
Red_color = (250, 0, 0)

Vel = 5
B_vel = 7

bullet_width, bullet_height = 20, 10
max_bullet = 5

Width, Height = 1000, 500
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game...")

bg = pygame.transform.scale(
	pygame.image.load("Assets/space.png"), (Width,Height))

border = pygame.Rect(0,0 ,5,Height)
border.center = (Width//2, Height//2)

yellow_ship = pygame.transform.rotozoom(
	pygame.image.load("Assets/yellow.png"), 90, 0.12)
red_ship = pygame.transform.rotozoom(
	pygame.image.load("Assets/red.png"), 270, 0.12)

yellow_life = 10
red_life = 10

def yellow_movement(keys, yellow):
	if keys[pygame.K_w] and yellow.top >= 0:
		yellow.centery -= Vel

	if keys[pygame.K_s] and yellow.bottom <= Height:
		yellow.centery += Vel

	if keys[pygame.K_a] and yellow.left >= 0:
		yellow.centerx -= Vel

	if keys[pygame.K_d] and yellow.right <= border.left:
		yellow.centerx += Vel

def red_movement(keys, red):
	if keys[pygame.K_UP] and red.top >= 0:
		red.centery -= Vel

	if keys[pygame.K_DOWN] and red.bottom <= Height:
		red.centery += Vel

	if keys[pygame.K_LEFT] and red.left >= border.right:
		red.centerx -= Vel

	if keys[pygame.K_RIGHT] and red.right <= Width:
		red.centerx += Vel

def handle_bullet(yellow,red, yellow_bullets,red_bullets):
	global red_life, yellow_life
	for bullet in yellow_bullets:
		bullet.x += B_vel
		if red.colliderect(bullet):
			yellow_bullets.remove(bullet)
			red_life -= 1
			hit.play()
		elif bullet.left >= Width:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= B_vel
		if yellow.colliderect(bullet):
			red_bullets.remove(bullet)
			yellow_life -= 1
			hit.play()
		elif bullet.right <= 0:
			red_bullets.remove(bullet)

def draw_winner():
	if yellow_life == 0:
		winner = win_font.render("Red Wins !!!", 1, White)
	elif red_life == 0:
		winner = win_font.render("Yellow Wins !!!", 1, White)

	winner_pos = winner.get_rect(center = (Width//2, Height//2))
	Win.blit(winner, winner_pos)
	pygame.display.update()

def draw(yellow,red, yellow_bullets,red_bullets):
	Win.blit(bg, (0,0))

	yellow_text = font.render(str(f"Life {yellow_life}"), 1, Yellow_color)
	red_text = font.render(str(f"Life {red_life}"), 1, Red_color)

	Win.blit(yellow_text, (10,10))
	Win.blit(red_text, (Width - red_text.get_width() -10, 10))

	pygame.draw.rect(Win, White, border)

	for bullet in yellow_bullets:
		pygame.draw.ellipse(Win, Yellow_color, bullet)

	for bullet in red_bullets:
		pygame.draw.ellipse(Win, Red_color, bullet)

	Win.blit(yellow_ship, yellow)
	Win.blit(red_ship, red)

	pygame.display.update()
	clock.tick(FPS)

def main():
	global yellow_life, red_life
	yellow = yellow_ship.get_rect(center = (100, Height//2))
	red = red_ship.get_rect(center = (Width - 100, Height//2))

	yellow_bullets = []
	red_bullets = []

	while yellow_life != 0 and red_life != 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullet:
					bullet = pygame.Rect((0,0),(bullet_width,bullet_height))
					bullet.center = yellow.center
					yellow_bullets.append(bullet)
					shoot.play()

				if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullet:
					bullet = pygame.Rect((0,0),(bullet_width,bullet_height))
					bullet.center = red.center
					red_bullets.append(bullet)
					shoot.play()

		draw(yellow,red, yellow_bullets,red_bullets)

		keys = pygame.key.get_pressed()
		yellow_movement(keys, yellow)
		red_movement(keys, red)

		handle_bullet(yellow,red, yellow_bullets,red_bullets)

	draw_winner()
	pygame.time.delay(3000)
	yellow_life, red_life = 10, 10
	main()

if __name__ == '__main__':
	main()
