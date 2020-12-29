import pygame
import os
import sys
import numpy as np
import json
from grid import Grid

options = json.load(open("options.json", "r"))[0]

pygame.init()
pygame.font.init()
pygame.display .set_caption("Cross Word")

# GLOBAL CONSTANTS
BLOCK_SIZE = 20
MARGIN = 15
N_BLOCKS = options["size"]

# GLOBAL VARIABLES
GRID = []
WORDS = []

# GAME WINDOW
WIDTH = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN + 300
HEIGHT = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# COLORS
LET_COLOR = (0, 0, 0)
WORD_COLOR = (155, 0, 0)
ACCENT = (130, 30, 30)

# LOADING IMAGES
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets/Images", "bg.jpg")), (WIDTH, HEIGHT))
RESTART = pygame.transform.scale(pygame.image.load(
    os.path.join("assets/Images", "restart.png")), (75, 75))
# CIRCLE = pygame.transform.scale(pygame.image.load(
    # os.path.join("assets/Images", "circle-32.png")), (32, 32))
CIRCLE = pygame.image.load(
    os.path.join("assets/Images", "circle-32.png"))


# LOADING FONTS
LET_FONT = pygame.font.Font(os.path.join(
    "assets/Montserrat", "Montserrat-Light.ttf"), 27)
LET_FONT_2 = pygame.font.Font(os.path.join(
    "assets/Montserrat", "Montserrat-Medium.ttf"), 30)
WORD_FONT = pygame.font.Font(os.path.join(
    "assets/Montserrat", "Montserrat-Light.ttf"), 35)

def get_grid():
    global GRID, WORDS

    GRID, WORDS = Grid().main()

def hover(rect):
    if rect.collidepoint(pygame.mouse.get_pos()):
        return True
    return False

def show_grid(selection_grid):

	for column in range(N_BLOCKS):
		for row in range(N_BLOCKS):
			x = (MARGIN + BLOCK_SIZE) * column + MARGIN
			y = (MARGIN + BLOCK_SIZE) * row + MARGIN

			text = LET_FONT.render(str(GRID[row, column]), 1, (0, 0, 0))
			text_rect = text.get_rect()
			text_rect.x = int(x + (BLOCK_SIZE / 2) - text_rect.width / 2)
			text_rect.y = int(y + (BLOCK_SIZE / 2) - text_rect.height / 2)

			if selection_grid[row, column] == 1:
				WIN.blit(CIRCLE, (x-6, y-3)) 
			
			if hover(text_rect):
				text = LET_FONT_2.render(str(GRID[row, column]), 1, ACCENT)

			WIN.blit(text, (text_rect.x, text_rect.y))


def show_words():
    pygame.draw.line(WIN, (0, 0, 0), (WIDTH-250, 0),  (WIDTH-250, HEIGHT), 3)

    for word in WORDS:
        word_lbl = WORD_FONT.render(word, 1, WORD_COLOR)
        word_rect = word_lbl.get_rect()
        word_rect.x = int(WIDTH/2-(word_rect.width/2)+300)
        word_rect.y = int(WORDS.index(word)*word_rect.height)

        WIN.blit(word_lbl, (word_rect.x, word_rect.y))


def rest_btn():
    rest_rect = RESTART.get_rect()
    rest_rect.x = int(WIDTH/2 - (rest_rect.width/2) + 300)
    rest_rect.y = int(HEIGHT - (rest_rect.height + MARGIN))

    WIN.blit(RESTART, (rest_rect.x, rest_rect.y))

    return rest_rect


def main():
	run = True
	clock = pygame.time.Clock()
	selection_grid = np.zeros((N_BLOCKS, N_BLOCKS))

	get_grid()

	while run:
		clock.tick(60)

		WIN.blit(BG, (0, 0))

		show_grid(selection_grid)
		show_words()
		restart_btn = rest_btn()

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				column = (pos[0]-6) // (BLOCK_SIZE + MARGIN)
				row = (pos[1]-6) // (BLOCK_SIZE + MARGIN)
				
				if row < N_BLOCKS and column < N_BLOCKS:
					if selection_grid[row, column] == 1:
						selection_grid[row, column] = 0
					else:
						selection_grid[row, column] = 1

				if hover(restart_btn):
					run = False
					main()


if __name__ == '__main__':
	main()
