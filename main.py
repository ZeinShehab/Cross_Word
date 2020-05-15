import random
import numpy as np

file = open("words.txt", "r")

# GLOBAL CONSTANTS
WIDTH = 18
HEIGHT = 18
NWORDS = 5
CHARS = "abcdefghijklmnopqrstuvwxyz"
WORDS = file.read().splitlines()


class CrossWord:
    def __init__(self):
        self.chsn_wrds = []
        self.tkn_pos = []
        self.grid = np.array([])
        self.run = True
        self.x = 0
        self.y = 0
        self.pos = []
        self.orientation = None
        self.old_pos = None
        self.collide = False

    def get_grid(self):
        # Generating a grid of random letters
        letters = []
        for _ in range(WIDTH):
            for _ in range(HEIGHT):
                letters.append(random.choice(CHARS))
        self.grid = np.array(letters).reshape(HEIGHT, WIDTH)

    def format_grid(self):
        self.grid = str(self.grid).replace("[", " ").replace("]", " ").replace("'", "")

    def get_wrds(self, chc):
        # Generating a list of random words
        tkn_wrds = []
        while len(self.chsn_wrds) < NWORDS:
            wrd = random.choice(WORDS)
            if chc == 0:
                if (len(wrd) < WIDTH) and (wrd not in tkn_wrds):
                    self.chsn_wrds.append(wrd)
                    tkn_wrds.append(wrd)
            elif chc == 1:
                if (len(wrd) < HEIGHT) and (wrd not in tkn_wrds):
                    self.chsn_wrds.append(wrd)
                    tkn_wrds.append(wrd)

    def format_wrds(self):
        self.chsn_wrds = str(self.chsn_wrds[:]).replace("'", "").replace("[", "").replace("]", "")

    def get_pos(self, u, v, wrd, chc, orientation):

        if orientation == 0:  # Normal word
            self.orientation = "Normal"

            # Generating coordinates of the word
            self.x = random.randint(0, WIDTH - u)
            self.y = random.randint(0, HEIGHT - v)
            self.pos = []

            x, y = self.x, self.y

            # Generating array of positions that the word will take
            for _ in wrd:
                self.pos.append([x, y])

                # Incrementing x for horizontal word
                if chc == 0:
                    x += 1
                # Incrementing y for vertical word
                elif chc == 1:
                    y += 1

        else:  # Reverse word
            self.orientation = "Reverse"

            # Generating coordinates of the word
            self.x = random.randint(u, WIDTH - 1)
            self.y = random.randint(v, HEIGHT - 1)
            self.pos = []

            x, y = self.x, self.y

            # Generating array of positions that the word will take
            for _ in wrd:
                self.pos.append([x, y])

                # Decrementing x for horizontal word
                if chc == 0:
                    x += -1
                # Decrementing y for vertical word
                elif chc == 1:
                    y += -1

        # Adding the position of the first word to the taken positions
        if len(self.tkn_pos) == 0:
            self.tkn_pos.append(self.pos)

        # Checking if the word collides with any other word
        self.is_collide()

        # Recalling the get_pos func to generate a new position if it collides
        if self.collide and len(self.tkn_pos) > 1:  # Making sure it doesn't loop through the first position
            self.old_pos = self.pos
            self.get_pos(u, v, wrd, chc, orientation)
        else:
            self.tkn_pos.append(self.pos)

    def is_collide(self):
        collide = False
        for i in self.tkn_pos:
            for j in i:
                for k in self.pos:
                    if k[0] == j[0] and k[1] == j[1]:
                        collide = True
                        break
                    else:
                        self.collide = False
        self.collide = collide

    def put_wrd(self, x, y, wrd, chc, orientation):
        # Plotting each letter in the word on its respective x and y
        for let in wrd:
            self.grid[y, x] = let

            # Incrementing x and y to plot normal words
            if orientation == 0:
                if chc == 0:
                    x += 1
                elif chc == 1:
                    y += 1
            # Decrementing x and y to plot reverse words
            else:
                if chc == 0:
                    x += -1
                elif chc == 1:
                    y += -1

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
        # Horizontal or vertical word
        chc = random.randint(0, 1)

        # Generating grid and words
        self.get_grid()
        self.get_wrds(chc)

        data = ""

        for word in self.chsn_wrds:
            # Normal or reverse word
            orientation = random.randint(0, 1)

            wrd_len = len(word)

            if chc == 0:  # Horizontal word

                # Normal word
                if orientation == 0:
                    op = '+'
                    self.get_pos(wrd_len, 1, word, chc, orientation)
                # Reverse word
                else:
                    op = '-'
                    self.get_pos(wrd_len, 0, word, chc, orientation)

                data += f"Word: {word} | Len={wrd_len} | X={self.x+1}{op} | Y={self.y+1} | [Horizontal] |" \
                        f" {self.orientation}\n"

            elif chc == 1:  # Vertical word

                # Normal word
                if orientation == 0:
                    op = '+'
                    self.get_pos(1, wrd_len, word, chc, orientation)
                # Reverse word
                else:
                    op = '-'
                    self.get_pos(0, wrd_len, word, chc, orientation)

                data += f"Word: {word} | Len={wrd_len} | X={self.x+1} | Y={self.y+1}{op} | [Vertical] |" \
                        f" {self.orientation}\n"

            if word == self.chsn_wrds[0]:
                self.collide = False

            # Saving grid data
            data += f"Position: {self.pos}\nold_pos: {self.old_pos}\nCollide: {self.collide}\n\n"

            # Writing word to the grid
            self.put_wrd(self.x, self.y, word, chc, orientation)

        # Formatting words and grid to write to text file
        self.format_grid()
        self.format_wrds()
        self.save_grid("grid.txt", "w+")
        self.save_grid_data("grid_data.txt", "w+", data)


game = CrossWord()
game.main()
