### Sudoku Generates Here ###

def checkGrid(grid):
	'''Checks if the grid is full or not'''
	for row in range(9):
		if 0 in grid[row]:
			return False
	return True

def current_info(grid, row, col):
	'''Gives all the numbers pesent in the current row, column and group'''
	res = []
	
	for i in range(9):
		res.append(grid[i][col])
	
	r, c = row // 3 * 3, col // 3 * 3
	for i in range(r, r+3):
		res.extend(grid[i][c : c+3])
	
	return grid[row] + res

def fillGrid():
	'''Fills the whole Grid'''
	numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	grid = [[0] * 9 for _ in range(9)]

	def recurse(grid):
		for i in range(81):
			row, col = i//9, i%9
			if grid[row][col] == 0:
				shuffle(numberList)
				for value in numberList:
					if value not in current_info(grid, row, col):
						grid[row][col] = value
						if checkGrid(grid):
							return True
						elif recurse(grid):
							return True
				break
		grid[row][col] = 0

	recurse(grid)
	return grid

def solveGrid(grid):
	'''Tries to solve the grid, uses counter to see how many solutions are possibles'''
	global counter
	
	for i in range(81):
		row, col = i // 9, i % 9
		if grid[row][col] == 0:
			for value in range(1, 10):
				if value not in current_info(grid, row, col):
					grid[row][col] = value
					if checkGrid(grid):
						counter += 1
						break
					elif solveGrid(grid):
						return True
			break
	grid[row][col] = 0

def makePuzzle(full_grid, attempts=1):
	'''Removes the numbers such that only one solution is present'''
	global counter
	
	grid = []
	for i in range(9):
		grid.append(full_grid[i][:])
	
	attempts = attempts  # High value -> hard puzzle (more time)
	while attempts > 0:
		
		row, col = randint(0, 8), randint(0, 8)
		while grid[row][col] == 0:
			row, col = randint(0, 8), randint(0, 8)

		backup = grid[row][col]
		grid[row][col] = 0

		copyGrid = []
		for i in range(9):
			copyGrid.append(grid[i][:])

		counter = 0
		solveGrid(copyGrid)
		if counter != 1:
			grid[row][col] = backup
			attempts -= 1
	
	return grid

### Game Code Starts Here ###

class Text:
	def __init__(self, text, font_face, font_color, font_size, pos):
		self.text = text

		self.font_face = font_face
		self.font_color = font_color
		self.font_size = font_size

		self.x, self.y = pos

	def draw(self, screen):
		font = pygame.font.SysFont(self.font_face, self.font_size)
		text = font.render(self.text, 1, self.font_color)
		text_rect = text.get_rect(center = (self.x, self.y))
		screen.blit(text, text_rect)


class Button:
	def __init__(self, text, font_face, font_color, font_size, pos, dim, rect_color, border=3):
		self.text = text

		self.font_face = font_face
		self.font_color = font_color
		self.font_size = font_size

		self.x, self.y = pos
		self.width, self.height = dim
		self.rect_color = rect_color
		
		self.border = border
		self.main_border = border

		self.clicked = False

	def draw(self, screen):
		self.rect = pygame.Rect((0,0), (self.width, self.height))
		self.rect.center = self.x, self.y
		pygame.draw.rect(screen, self.rect_color, self.rect, self.border)

		font = pygame.font.SysFont(self.font_face, self.font_size)
		text = font.render(self.text, 1, self.font_color)
		text_rect = text.get_rect(center = self.rect.center)
		screen.blit(text, text_rect)

		if self.clicked and self.border == 0:
			self.border = self.main_border
			self.clicked = False

	def is_clicked(self, pos):
		if self.rect.collidepoint(pos):
			self.clicked = True
			self.border = 0
			return True
		return False

	def is_selected(self, pos):
		if self.rect.collidepoint(pos):
			return True
		return False

### Menu ###

def Menu():
	start_btn = Button("Start", None, White, 40, (WIDTH//2, HEIGHT//4*3) , (WIDTH * .3, HEIGHT * .1), White, 3)
	plus_btn = Button(">", None, White, 30, (3*WIDTH//4, HEIGHT//2) , (WIDTH * .05, HEIGHT * .05), White, 3)
	minus_btn = Button("<", None, White, 30, (WIDTH//4, HEIGHT//2) , (WIDTH * .05, HEIGHT * .05), White, 3)

	levels = ["Beginner", "Easy", "Medium", "Hard", "Extreme"]
	level_text = Text(levels[0], None, White, 30, (WIDTH//2, HEIGHT//2))

	def drawMenu():
		SCREEN.fill(Grey)

		start_btn.draw(SCREEN)
		plus_btn.draw(SCREEN)
		minus_btn.draw(SCREEN)
		level_text.draw(SCREEN)

		pygame.display.update()
		clock.tick(12)

	def menuLoop():
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if plus_btn.is_clicked(event.pos):
						idx = levels.index(level_text.text) + 1
						if idx >= len(levels): idx = 0
						level_text.text = levels[idx]
					elif minus_btn.is_clicked(event.pos):
						idx = levels.index(level_text.text) - 1
						if idx < 0: idx = len(levels) - 1
						level_text.text = levels[idx]
					
					elif start_btn.is_selected(event.pos):
						start_btn.text = "Loading..."
						start_btn.border = 0
						start_btn.font_color = Grey
						drawMenu()
						return levels.index(level_text.text) + 1
			drawMenu()
	return menuLoop()

### Main Game ###

def MainGame(level):
	global selected_num
	selected_num = None

	GRID = fillGrid()
	puzzle = makePuzzle(GRID, attempts=level)

	font = pygame.font.SysFont("Kristen ITC", 30)

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
	for row in puzzle:
		per = []
		for num in row:
			per.append(bool(num))
		permanent.append(per)

	# Buttons
	width = WIDTH//6
	height = HEIGHT//13
	gap = WIDTH//30

	num_btn_rects = []
	for row in range(2):
		for col in range(5):
			rect = pygame.Rect( (col * (width + gap) + 10, row * (height + gap) + 10), (width, height))
			num_btn_rects.append(rect)

	# Button Selection
	def Select_Num_mouse(pos):
		for rect in num_btn_rects:
			if rect.collidepoint(pos):
				btn = num_btn_rects.index(rect) + 1
				if btn == selected_num:
					return None
				return btn
		return selected_num

	# Writing of Number on Board
	def Write_Num(pos):
		for row in range(len(boxes)):
			for col in range(len(boxes[row])):
				if boxes[row][col].collidepoint(pos) and permanent[row][col] is False:
					if selected_num != 10 and puzzle[row][col] != selected_num:
						puzzle[row][col] = selected_num
					else:
						puzzle[row][col] = 0
	
	def drawMain(screen):
		screen.fill(Grey)

		# Button Drawing
		for i, rect in enumerate(num_btn_rects):
			border = 0 if  i+1 == selected_num else 3
			color = White if border else Grey
			text = str(i + 1) if  i + 1 != 10 else "<<"

			pygame.draw.rect(screen, White, rect, border)
			
			text = font.render(text , 1, color)
			text_rect = text.get_rect(center = rect.center)
			screen.blit(text, text_rect)

		for row in range(len(boxes)):
			for col in range(len(boxes[row])):
				pygame.draw.rect(screen, Lightwhite, boxes[row][col], 1)

				num = puzzle[row][col]
				num = str(num) if num != 0 else ""

				text = font.render(num, 1, White)
				text_rect = text.get_rect(center = boxes[row][col].center)
				screen.blit(text, text_rect)

		for group in groups:
			pygame.draw.rect(screen, White, group, 3)

		pygame.display.update()
		clock.tick(40)

	def MainLoop():
		global selected_num
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					selected_num = Select_Num_mouse(event.pos)
					if selected_num:
						Write_Num(event.pos)

			drawMain(SCREEN)
	MainLoop()

from random import randint, shuffle
import sys
import pygame

pygame.init()
clock = pygame.time.Clock()

# Screen
WIDTH, HEIGHT = 600, 650
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
Grey = (30, 30, 30)
White = (250, 250, 250)
Lightwhite = (200, 200, 200)

start = Menu()
while start:
	MainGame(start * 2)
	start = Menu()

pygame.quit()