import random
import numpy as np
file = open("words.txt", "r")


# GLOBAL CONSTANTS
WIDTH = 18
HEIGHT = 18
CHARS = "abcdefghijklmnopqrstuvwxyz"
WORDS = file.read().splitlines()
NWORDS = 10


class CrossWord:
    def __init__(self):
        self.chsn_wrds = []
        self.tkn_pos = []
        self.grid = None
        self.pos = None
        self.x = None
        self.y = None

    def get_grid(self):
        letters = []
        for _ in range(WIDTH):
            for _ in range(HEIGHT):
                letters.append(random.choice(CHARS))
        self.grid = np.array(letters).reshape(HEIGHT, WIDTH)

    def format_grid(self):
        self.grid = str(self.grid).replace("[", " ").replace("]", " ").replace("'", "")

    def get_wrd(self):
        while len(self.chsn_wrds) < NWORDS:
            wrd = random.choice(WORDS)
            if len(wrd) < WIDTH and HEIGHT:
                self.chsn_wrds.append(wrd)

    def format_wrds(self):
        self.chsn_wrds = str(self.chsn_wrds[:]).replace("'", "").replace("[", "").replace("]", "")

    def get_pos(self, u, v, wrd, chc):
        x = random.randint(0, WIDTH - u)
        y = random.randint(0, HEIGHT - v)
        self.pos = []

        self.x = x
        self.y = y

        for _ in wrd:
            self.pos.append([x, y])
            if chc == 0:
                x += 1
            elif chc == 1:
                y += 1

    def put_wrd(self, x, y, wrd, chc):
        for let in wrd:
            self.grid[y, x] = let
            if chc == 0:
                x += 1
            elif chc == 1:
                y += 1

    def output(self, filename, mode):
        f = open(filename, mode)
        f.write(f"{self.grid} \n\n {self.chsn_wrds}")
        f.close()

    def main(self):
        self.get_grid()
        self.get_wrd()

        for word in self.chsn_wrds:
            chc = random.randint(0, 1)
            wrd_len = len(word)

            if chc == 0:
                self.get_pos(wrd_len, 1, word, chc)

                print(f"Word: {word} | Len={wrd_len} | X={self.x}+ | Y={self.y} | [Horizontal]")
            elif chc == 1:
                self.get_pos(1, wrd_len, word, chc)

                print(f"Word: {word} | Len={wrd_len} | X={self.x} | Y={self.y}+ [Vertical] ")

            print(f"Position: {self.pos}\n")
            self.put_wrd(self.x, self.y, word, chc)

        self.format_grid()
        self.format_wrds()
        self.output("grid.txt", "w+")


game = CrossWord()
game.main()
