import random
import numpy as np
file = open("words.txt", "r")


# GLOBAL CONSTANTS
WIDTH = 18
HEIGHT = 18
NWORDS = 10
CHARS = " "
WORDS = file.read().splitlines()


class CrossWord:
    def __init__(self):
        self.chsn_wrds = []
        self.tkn_pos = []
        self.grid = np.array([])
        self.x = 0
        self.y = 0
        self.pos = []

    def get_grid(self):
        letters = []
        for _ in range(WIDTH):
            for _ in range(HEIGHT):
                letters.append(random.choice(CHARS))
        self.grid = np.array(letters).reshape(HEIGHT, WIDTH)

    def format_grid(self):
        self.grid = str(self.grid).replace("[", " ").replace("]", " ").replace("'", "")

    def get_wrds(self):
        tkn_wrds = []
        while len(self.chsn_wrds) < NWORDS:
            wrd = random.choice(WORDS).lower()
            if (len(wrd) < WIDTH) and (wrd not in tkn_wrds):
                self.chsn_wrds.append(wrd)
                tkn_wrds.append(wrd)

    def format_wrds(self):
        self.chsn_wrds = str(self.chsn_wrds[:]).replace("'", "").replace("[", "").replace("]", "")

    def get_pos(self, u, v, wrd, chc, orientation):
        if orientation == 0:  # Normal word
            self.x = random.randint(0, WIDTH - u)
            self.y = random.randint(0, HEIGHT - v)
            self.pos = []

            x, y = self.x, self.y

            # array of positions that the word will take
            for _ in wrd:
                self.pos.append([y, x])

                if chc == 0:
                    x += 1
                elif chc == 1:
                    y += 1
                else:
                    x += 1
                    y += 1

        else:  # Reverse word
            self.x = random.randint(u, WIDTH - 1)
            self.y = random.randint(v, HEIGHT - 1)
            self.pos = []

            x, y = self.x, self.y

            # array of positions that the word will take
            for _ in wrd:
                self.pos.append([y, x])

                if chc == 0:
                    x += -1
                elif chc == 1:
                    y += -1
                else:
                    x -= 1
                    y -= 1

        if chc == 0:
            orien = '0'
        elif chc == 1:
            orien = '1'
        else:
            orien = '2'

        self.pos.append(orien)

        # Adding the position of the first word to the taken positions
        if len(self.tkn_pos) == 0:
            self.tkn_pos.append(self.pos)

        # generate a new position if it collides
        if self.is_collide(chc, wrd) and len(self.tkn_pos) > 1:  # Making sure it doesn't loop through the first position
            self.get_pos(u, v, wrd, chc, orientation)
        else:
            self.tkn_pos.append(self.pos)

    def is_collide(self, chc, wrd):
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

    def share_let(self, dirc1, dirc2, word, pos):
        for l, p in zip(word, self.pos):                             # Getting letter of corresponding pos
            if p == pos:
                let = l

        if dirc1 != dirc2 and self.grid[pos[0], pos[1]] == let:
            return True
        return False

    def put_wrd(self, wrd, pos):
        for index, let in zip(pos, wrd):
            self.grid[index[0], index[1]] = let

    def save_grid(self, filename, mode):
        f = open(filename, mode)
        f.write(f"{self.grid} \n\n {self.chsn_wrds}")
        f.close()

    @staticmethod
    def save_grid_data(filename, mode, data):
        f = open(filename, mode)
        f.write(data)
        f.close()

    def main(self):
        self.get_grid()
        self.get_wrds()

        data = ""

        for word in self.chsn_wrds:
            chc = random.randint(0, 2)          # Horizontal, vertical or diagonal word
            orientation = random.randint(0, 1)  # Normal or reverse word
            wrd_len = len(word)

            if word == self.chsn_wrds[0]:
                self.collide = False

            if chc == 0:  # Horizontal word
                # Normal word
                if orientation == 0:
                    op = '+'
                    self.get_pos(wrd_len, 1, word, chc, orientation)
                # Reverse word
                else:
                    op = '-'
                    self.get_pos(wrd_len, 0, word, chc, orientation)

                data += f"Word: {word} | Len={wrd_len} | X={self.x + 1}{op} | Y={self.y + 1} | [Horizontal]\n"

            elif chc == 1:  # Vertical word
                # Normal word
                if orientation == 0:
                    op = '+'
                    self.get_pos(1, wrd_len, word, chc, orientation)
                # Reverse word
                else:
                    op = '-'
                    self.get_pos(0, wrd_len, word, chc, orientation)

                data += f"Word: {word} | Len={wrd_len} | X={self.x + 1} | Y={self.y + 1}{op} | [Vertical]\n"

            else:   # diagonal word
                if orientation == 0:
                    op = "+"
                    self.get_pos(wrd_len, wrd_len, word, chc, orientation)
                else:
                    op = '-'
                    self.get_pos(wrd_len, wrd_len, word, chc, orientation)

                data += f"Word: {word} | Len={wrd_len} | X={self.x + 1}{op} | Y={self.y + 1}{op} | [Diagonal]\n"

            # Writing word to the grid
            self.put_wrd(word, self.pos)

            # Saving grid data
            data += f"Position: {self.pos}\n\n"

        # Returns arrays of grid and words
        return self.grid, self.chsn_wrds

        # Formatting words and grid to write to text file
        self.format_grid()
        self.format_wrds()
        self.save_grid("grid.txt", "w+")
        self.save_grid_data("grid_data.txt", "w+", data)
