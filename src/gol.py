import pygame
from time import sleep

# Initialize game properties
pygame.init()
window_w = 255
window_h = 285
window = pygame.display.set_mode((window_w, window_h))
running = True

# Initialize grid square properties
box_height = 20
box_width = 20
margin = 5
started = False

# Initialize widely used colours
WHITE = (255, 255, 255)
BLUE = (0, 80, 230)
GRAY = (98, 98, 98)

def checkRange(element):
    if element == 0: # First row or first column, range is 0 to 1
        temp = range(0, 2)
    elif element == 9: # Last row or last column, range is -1 to 0
        temp = range(-1, 1)
    else: # Otherwise, range -1 to 1
        temp = range(-1, 2)
    return temp

def nbCount(row, col):
    count = 0
    for i in checkRange(row):
        for j in checkRange(col):
            if (row + i) > 9 or (col + j) > 9:
                return
            if i == 0 and j == 0:
                continue
            if grid[row + i][col + j] == 1:
                count += 1
    return count

def calculateLive(row, col):
    nb = nbCount(row, col)
    if (nb == 2 or nb == 3) and grid[row][col] == 1:
        temp_grid[row][col] = 1
        return True
    elif nb == 3 and grid[row][col] == 0:
        temp_grid[row][col] = 1
        return True
    else:
        temp_grid[row][col] = 0
        return False

def startGame():
    if not started:
        return
    for i in range(10):
        for j in range(10):
            calculateLive(i, j)
    for k in range(10):
        for l in range(10):
            grid[k][l] = temp_grid[k][l]

def drawGridSquare(left, top, colour):
    pygame.draw.rect(window, colour, (left, top, box_width, box_height))

def drawStartButton(colour, started):
    btn_h = 25
    btn_w = 100
    pygame.draw.rect(window, colour, (window_w // 2 - btn_w // 2, window_h - margin - btn_h, btn_w, btn_h))

def drawGrid():
    for i in range(10):
        for j in range(10):
            colour = WHITE
            if grid[i][j] == 1:
                 colour = BLUE
            drawGridSquare(margin + (box_width + margin) * j, margin + (box_height + margin) * i, colour)

def generateGrid():
    grid = []
    for i in range(10):
        grid.append([])
        for j in range(10):
            grid[i].append(0)
    return grid

grid = generateGrid()
temp_grid = generateGrid()

colour = WHITE
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # print('x-pos: ' + pos[0])
            # print('y-pos: ' + pos[1])
            if pos[1] < 250 and not started:
                row = pos[1] // (box_height + margin)
                col = pos[0] // (box_width + margin)
                if grid[row][col] == 0:
                    grid[row][col] = 1
                else:
                    grid[row][col] = 0
                # print(nbCount(row, col)) # Gives nbCount for each block clicked
            elif pos[0] > 76 and pos[0] < 178:
                colour = GRAY
                started = True
        startGame()
        drawGrid()
        drawStartButton(colour, started)

        pygame.time.Clock().tick(60)
        pygame.display.update()

pygame.quit()