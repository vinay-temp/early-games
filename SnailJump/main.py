import pygame, sys
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.player_walk = [player_walk_1, player_walk_2, player_jump]
		self.player_index = 0

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (100, 0))
		self.ground = 300
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.1)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= self.ground:
			self.jump_sound.play()
			self.gravity = -20

	def apply_gravity(self):
		self.gravity += 1
		self.rect.bottom += self.gravity
		if self.rect.bottom >= self.ground: self.rect.bottom = self.ground

	def animation(self):
		if self.rect.bottom < self.ground: self.image = self.player_walk[2]
		else:
			self.player_index += 0.1
			if self.player_index > len(self.player_walk) - 1: self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation()


class Obstacle(pygame.sprite.Sprite):
	def __init__(self, obs_type):
		super().__init__()
		if obs_type == "snail":
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1, snail_2]
			y_pos = 300
		
		elif obs_type == "fly":
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1, fly_2]
			y_pos = 100

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

	def animation(self):
		self.animation_index += 0.1
		if self.animation_index > len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def move_left(self):
		self.rect.x -= 5
		if self.rect.x <= -50: self.kill()

	def update(self):
		self.animation()
		self.move_left()


def display_score():
	current_time = pygame.time.get_ticks() - start_time
	score_surf = test_font.render(str(current_time // 100), False, 'Grey10')
	score_rect = score_surf.get_rect(center=(400, 40))
	screen.blit(score_surf, score_rect)
	return current_time // 100

def draw_and_update(screen):
	screen.blit(SKY, (0,0))
	screen.blit(GROUND, (0, 300))
	player.draw(screen)
	player.update()
	obstacle_group.draw(screen)
	obstacle_group.update()

# Starting Variables
game_active = start_time = score = 0

# Initial Setup
pygame.init()
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 100)
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)
screen = pygame.display.set_mode((800, 400))

# Background
SKY = pygame.image.load('graphics/SKY.png').convert_alpha()
GROUND = pygame.image.load('graphics/ground.png').convert_alpha()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# Sprites
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# MainLoop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit()

		elif game_active and event.type == obstacle_timer:
			obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

		elif not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			player = pygame.sprite.GroupSingle()
			player.add(Player())
			obstacle_group = pygame.sprite.Group()		
			start_time = pygame.time.get_ticks()
			game_active = True

	if game_active:
		draw_and_update(screen)
		score = display_score()
		game_active = not pygame.sprite.spritecollide(player.sprite, obstacle_group, False)

	else:
		if score: pygame.time.delay(1000)
		screen.fill((94, 129, 162))
		score_surf = test_font.render(f'S c o r e : {score}', 1, (111,196,169))
		score_rect = score_surf.get_rect(center=(400, 200))
		screen.blit(score_surf, score_rect)

	clock.tick(60)
	pygame.display.update()