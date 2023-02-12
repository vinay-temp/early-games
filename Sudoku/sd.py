import pygame
from gen_sd import fillGrid, makePuzzle

pygame.init()
clock = pygame.time.Clock()

# Puzzle

print("Generating")
puzzle = fillGrid()
numbers = makePuzzle(puzzle, attempts=1)
print("Done")

# Screen
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
Grey = (30, 30, 30)
White = (250, 250, 250)
Lightwhite = (200, 200, 200)

# Font
font = pygame.font.SysFont("Kristen ITC", 30)

# Buttons
width = 100
height = 50
gap = 20

num_btn_rects = []
for row in range(2):
	for col in range(5):
		rect = pygame.Rect( (col * (width + gap) + 10, row * (height + gap)), (width, height))
		num_btn_rects.append(rect)
selected_num = None

# Button Selection
def Select_Num_mouse(pos):
	for rect in num_btn_rects:
		if rect.collidepoint(pos):
			btn = num_btn_rects.index(rect) + 1
			if btn == selected_num:
				return None
			return btn
	return selected_num

# Board
# Main Box
box_len = 450

BOX = pygame.Rect( (0,0), (box_len, box_len))
BOX.center = (WIDTH//2, 3*HEIGHT//5)

# Groups
groups = []
group_len = box_len // 3
for row in range(3):
	for col in range(3):
		rect = pygame.Rect( (BOX.x + row * group_len, BOX.y + col * group_len), (group_len, group_len))
		groups.append(rect)

# Small Boxes
num_gap = box_len // 9
boxes = []
for j in range(9):
	box = []
	for i in range(9):
		rect = pygame.Rect( (BOX.x + i * num_gap, BOX.y + j * num_gap), (num_gap, num_gap))
		box.append(rect)
	boxes.append(box)

# Permanent positions
permanent = []
for row in numbers:
	per = []
	for num in row:
		per.append(bool(num))
	permanent.append(per)

# Writing of Number on Board
def Write_Num(pos):
	for row in range(len(boxes)):
		for col in range(len(boxes[row])):
			if boxes[row][col].collidepoint(pos) and permanent[row][col] is False:
				if selected_num != 10 and numbers[row][col] != selected_num:
					numbers[row][col] = selected_num
				else:
					numbers[row][col] = 0

# Drawing on Screen
def draw():
	screen.fill(Grey)

	# Button Drawing
	for i, rect in enumerate(num_btn_rects):
		border = 0 if  i+1 == selected_num else 3
		color = White if border else Grey
		text = str(i + 1) if  i + 1 != 10 else "<-"

		pygame.draw.rect(screen, White, rect, border)

		text = font.render(text , 1, color)
		text_rect = text.get_rect(center = rect.center)
		screen.blit(text, text_rect)

	# Board and numbers drawing
	for row in range(len(boxes)):
		for col in range(len(boxes[row])):
			pygame.draw.rect(screen, Lightwhite, boxes[row][col], 1)

			num = numbers[row][col]

			num = str(num) if num != 0 else ""
			text = font.render(num, 1, White)
			text_rect = text.get_rect(center = boxes[row][col].center)
			screen.blit(text, text_rect)

	for group in groups:
		pygame.draw.rect(screen, White, group, 3)

	pygame.display.update()
	clock.tick(70)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# Mouse Functions
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			selected_num = Select_Num_mouse(event.pos)
			if selected_num:
				Write_Num(event.pos)

		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			solve = True

	draw()
	'''if puzzle == numbers:
		screen.fill(Grey)
		text = font.render("Complete", 1, White)
		text_rect = text.get_rect(center = (WIDTH//2, HEIGHT//2))
		screen.blit(text, text_rect)
		pygame.display.update()
	else:
		draw()'''

pygame.quit()
