#!/usr/bin/python3

import random
import numpy as np
import json

# LOAD OPTIONS FILE
options = json.load(open("options.json", "r"))[0]

# GLOBAL CONSTANTS
SIZE = options["size"]
NWORDS = options["numberOfWords"]
DIFFICULTY = options["difficulty"]
WORDS = open(options["wordFile"], "r").read().splitlines()

# Prevent overstuffing words
if SIZE-NWORDS < 5:
    NWORDS = SIZE + 5

# Empty or full grid
if options["fillGrid"]:
    CHARS = "abcdefghijklmnopqrstuvwxyz"
else:
    CHARS = " "


class Grid:
    def __init__(self):
        self.grid = self.get_grid()
        self.chsn_wrds = self.get_wrds()
        self.tkn_pos = []
        self.pos = []

    @staticmethod
    def get_grid():
        letters = []
        for _ in range(SIZE):
            for _ in range(SIZE):
                letters.append(random.choice(CHARS))
        return np.array(letters).reshape(SIZE, SIZE)

    @staticmethod
    def format_grid(grid):
        return str(grid).replace("[", " ").replace("]", " ").replace("'", "")

    @staticmethod
    def get_wrds():
        word_list = []
        tkn_wrds = []
        chsn_wrds = []

        if DIFFICULTY == "easy":
            length_range = range(3, 6)
        elif DIFFICULTY == "medium":
            length_range = range(6, 8) 
        elif DIFFICULTY == "hard":
            length_range = range(8, SIZE-1)
        else:               # mixed
            length_range = range(0, SIZE-1)

        for wrd in WORDS:                           # Get words for the difficulty, add to list
            if len(wrd) in length_range:
                word_list.append(wrd)

        while len(chsn_wrds) < NWORDS:              # Choose random words from word_list
            wrd = random.choice(word_list).lower()

            if (wrd not in tkn_wrds):
                chsn_wrds.append(wrd)
                tkn_wrds.append(wrd)

        return chsn_wrds

    @staticmethod
    def format_wrds(words):
        return str(words[:]).replace("'", "").replace("[", "").replace("]", "")

    def get_pos(self, wrd):
        # Generate coordinates for word
        direction = random.choice([-1, 1])                              # Reverse(-1) or normal(1)
        orientation = random.choice([-1, 0, 1])                         # Horizontal(-1) or Vertical(1) or Diagonal(0)
        x_diag_dirc, y_diag_dirc = random.sample([1, 1, -1, -1], 2)     # Left(=) or Right(><) diagonal
        
        normal_range = range(0, SIZE-len(wrd))
        reverse_range = range(len(wrd), SIZE)

        self.pos = []

        if orientation != 0:                                            # Horizontal or Vertical
            cord_1 = random.randint(0, SIZE-1)
            cord_2 = [random.choice(normal_range), random.choice(reverse_range)]

            x, y = [cord_1, cord_2[::direction][0]][::orientation]
        
        else:                                                           # Diagonal
            cord_1 = random.sample(normal_range, 2)                    
            cord_2 = random.sample(reverse_range, 2) 

            if x_diag_dirc == y_diag_dirc:                              # Left diagonal
                x, y = [cord_1, cord_2][::x_diag_dirc][0]
            else:                                                       # Right diagonal
                x, y = [cord_1[0], cord_2[0]][::x_diag_dirc]
            
        # Adding coordinates to position
        for _ in wrd:
            self.pos.append([y, x])

            if orientation == -1:
                x += direction
            elif orientation == 1:
                y += direction
            else:
                x += x_diag_dirc
                y += y_diag_dirc

        # Adding orientation to position
        self.pos.append(str(orientation))

        if self.is_collide(wrd):                                        # Checking for collsion between words
            self.get_pos(wrd)
        else:
            self.tkn_pos.append(self.pos)                               # Add pos to taken position

    def is_collide(self, wrd):
        collide = False

        for k in self.pos:
            if type(k) != str:
                if self.grid[k[0], k[1]] != " ":
                    collide = True 

                    letter = wrd[self.pos.index(k)]
                    if letter == self.grid[k[0], k[1]]:
                        collide = False

        return collide

    def put_wrd(self, wrd, pos):
        for cord, let in zip(pos, wrd):
            self.grid[cord[0], cord[1]] = let

    @staticmethod
    def save_grid_data(filename, mode, data):
        f = open(filename, mode)
        f.write(data)
        f.close()

    def main(self):
        self.get_grid()
        self.get_wrds()

        for word in self.chsn_wrds:
            # Get postion for word
            self.get_pos(word)

            # Writing word to the grid
            self.put_wrd(word, self.pos)

        # Returns arrays of grid and words
        return self.grid, self.chsn_wrds
