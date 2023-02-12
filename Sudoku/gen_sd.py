from random import randint, shuffle

def checkGrid(grid):
	for row in range(9):
		if 0 in grid[row]:
			return False
	return True

def current_info(grid, row, col):
	res = []
	
	for i in range(9):
		res.append(grid[i][col])
	
	r, c = row // 3 * 3, col // 3 * 3
	for i in range(r, r+3):
		res.extend(grid[i][c : c+3])
	
	return grid[row] + res

def fillGrid():
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

def makePuzzle(full_grid, attempts=3):
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


'''grid = fillGrid()
for i in grid: print(i)
print()

puzzle = makePuzzle(grid)
for i in puzzle: print(i)'''
