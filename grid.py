import random
import numpy as np
import json

options = json.load(open("options.json", "r"))[0]

# GLOBAL CONSTANTS
WIDTH = options["width"]
HEIGHT = options["height"]
NWORDS = options["numberOfWords"]
WORDS = open(options["wordFile"], "r").read().splitlines()

if options["fillGrid"]:
    CHARS = "abcdefghijklmnopqrstuvwxyz"
else:
    CHARS = " "


class Grid:
    def __init__(self):
        self.chsn_wrds = []				# self.get_wrds()
        self.tkn_pos = []
        self.grid = np.array([])		# self.get_grid()
        self.x = 0
        self.y = 0
        self.pos = []

    def get_grid(self):
        letters = []
        for _ in range(WIDTH):
            for _ in range(HEIGHT):
                letters.append(random.choice(CHARS))
        self.grid = np.array(letters).reshape(HEIGHT, WIDTH)		# return

    @staticmethod
    def format_grid(grid):
        return str(grid).replace("[", " ").replace("]", " ").replace("'", "")

    def get_wrds(self):
        tkn_wrds = []
        wrds = []
        while len(wrds) < NWORDS:
            wrd = random.choice(WORDS).lower()
            if (len(wrd) < WIDTH) and (wrd not in tkn_wrds):
                wrds.append(wrd)
                tkn_wrds.append(wrd)
        self.chsn_wrds = wrds 										# return

    @staticmethod
    def format_wrds(words):
        return str(words[:]).replace("'", "").replace("[", "").replace("]", "")

    def get_pos(self, wrd):
        direction = random.choice([-1, 1])      # Reverse or normal
        orientation = random.choice([-1, 1])    # Vertical or Horizontal
        self.pos = []

        u = random.randint(0, WIDTH-1)

        if direction == 1:      # Normal = 1
            v = random.randint(0, WIDTH-len(wrd))
        else:                   # Reverse = -1
            v = random.randint(len(wrd), WIDTH-1)
            
        x = [v, u][::orientation][0]
        y = [v, u][::orientation][1]
        
        # Adding coordinates to position
        for _ in wrd:
            self.pos.append([y, x])

            if orientation == 1:    # Horizontal
                x += direction
            elif orientation == -1: # Vertical
                y += direction
        
        # Adding orientation to position
        self.pos.append(str(orientation))
 
        # Checking for collision with other words
        if self.is_collide(wrd) and len(self.tkn_pos) > 1:
            self.get_pos(wrd)
        else:
            self.tkn_pos.append(self.pos)
            # return pos

    def is_collide(self, wrd):
        collide = False
        collisions = 0
        for i in self.tkn_pos:
            for j in i:
                for k in self.pos:
                    if type(k) != str:

                        if k[0] == j[0] and k[1] == j[1]:                               # Checking if the words collide
                                collisions += 1

                                if self.share_let(self.pos[len(self.pos)-1], i[len(i) - 1], wrd, k) and collisions == 1:
                                    collide = False
                                    # print("SHARE", wrd)
                                else:
                                    collide = True 

        return collide

    def share_let(self, dirc1, dirc2, word, pos):                      # Needs Attention
        for l, p in zip(word, self.pos):                             # Getting letter of corresponding pos
            if p == pos:
                let = l

        if dirc1 != dirc2 and self.grid[pos[0], pos[1]] == let:
            return True
        return False

    def put_wrd(self, wrd, pos):
        for index, let in zip(pos, wrd):
            self.grid[index[0], index[1]] = let

    @staticmethod
    def save_grid(grid, words, filename, mode):
        f = open(filename, mode)
        f.write(f"{grid} \n\n {words}")
        f.close()

    @staticmethod
    def save_grid_data(filename, mode):
        f = open(filename, mode)
        f.write(data)
        f.close()

    def main(self):
        self.get_grid()
        self.get_wrds()

        global data
        data = ""

        for word in self.chsn_wrds:
            # chc = random.randint(0, 2)          # Horizontal, vertical or diagonal word
            # orientation = random.randint(0, 1)  # Normal or reverse word
            # wrd_len = len(word)

            # if word == self.chsn_wrds[0]:
            #     self.collide = False

            # if chc == 0:  # Horizontal word
            #     # Normal word
            #     if orientation == 0:
            #         op = '+'
            #         self.get_pos(wrd_len, 1, word, chc, orientation)
            #     # Reverse word
            #     else:
            #         op = '-'
            #         self.get_pos(wrd_len, 0, word, chc, orientation)

            #     data += f"Word: {word} | Len={wrd_len} | X={self.x + 1}{op} | Y={self.y + 1} | [Horizontal]\n"

            # elif chc == 1:  # Vertical word
            #     # Normal word
            #     if orientation == 0:
            #         op = '+'
            #         self.get_pos(1, wrd_len, word, chc, orientation)
            #     # Reverse word
            #     else:
            #         op = '-'
            #         self.get_pos(0, wrd_len, word, chc, orientation)

            #     data += f"Word: {word} | Len={wrd_len} | X={self.x + 1} | Y={self.y + 1}{op} | [Vertical]\n"

            # else:   # diagonal word
            #     if orientation == 0:
            #         op = "+"
            #         self.get_pos(wrd_len, wrd_len, word, chc, orientation)
            #     else:
            #         op = '-'
            #         self.get_pos(wrd_len, wrd_len, word, chc, orientation)

            #     data += f"Word: {word} | Len={wrd_len} | X={self.x + 1}{op} | Y={self.y + 1}{op} | [Diagonal]\n"

            
            # Writing word to the grid
            self.get_pos(word)
            self.put_wrd(word, self.pos)

            # Saving grid data
            data += f"Position: {self.pos}\n\n"

        # Returns arrays of grid and words
        return self.grid, self.chsn_wrds
