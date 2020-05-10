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
        self.old_pos = None
        self.dup = None

    def get_grid(self):
        letters = []
        for _ in range(WIDTH):
            for _ in range(HEIGHT):
                letters.append(random.choice(CHARS))
        self.grid = np.array(letters).reshape(HEIGHT, WIDTH)

    def format_grid(self):
        self.grid = str(self.grid).replace("[", " ").replace("]", " ").replace("'", "")

    def get_wrd(self):
        tkn_wrds = []
        while len(self.chsn_wrds) < NWORDS:
            wrd = random.choice(WORDS)
            if (len(wrd) < WIDTH and HEIGHT) and (wrd not in tkn_wrds):
                self.chsn_wrds.append(wrd)
                tkn_wrds.append(wrd)

    def format_wrds(self):
        self.chsn_wrds = str(self.chsn_wrds[:]).replace("'", "").replace("[", "").replace("]", "")

    def get_pos(self, u, v, wrd, chc):
        self.x = random.randint(0, WIDTH - u)
        self.y = random.randint(0, HEIGHT - v)

        x, y = self.x, self.y
        for _ in wrd:
            self.pos.append([x, y])
            if chc == 0:
                x += 1
            elif chc == 1:
                y += 1

    def collision(self):
        pass

    def put_wrd(self, x, y, wrd, chc):
        for let in wrd:
            self.grid[x, y] = let
            if chc == 0:
                x += 1
            elif chc == 1:
                y += 1

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
        self.get_wrd()
        data = ""

        for word in self.chsn_wrds:
            chc = random.randint(0, 1)
            wrd_len = len(word)

            if chc == 0:
                self.get_pos(wrd_len, 1, word, chc)

                data += f"Word: {word} | Len={wrd_len} | X={self.x}+ | Y={self.y} | [Horizontal]\n"
            elif chc == 1:
                self.get_pos(1, wrd_len, word, chc)

                data += f"Word: {word} | Len={wrd_len} | X={self.x} | Y={self.y}+ | [Vertical]\n"

            data += f"Position: {self.pos}\nold_pos: {self.old_pos}\nDuplicate: {self.dup}\n\n"

            self.put_wrd(self.x, self.y, word, chc)

        self.format_grid()
        self.format_wrds()
        self.save_grid("grid.txt", "w+")
        self.save_grid_data("grid_data.txt", "w+", data)
        print(self.tkn_pos)


game = CrossWord()
game.main()
