#!/usr/bin/python3

import random
import json
import numpy as np


class Setup:
    options = json.load(open("options.json", "r"))[0]

    SIZE = options["size"]
    WORD_LEN = options["wordLength"]
    NWORDS = options["numberOfWords"]
    WORDS = open(options["wordFile"], "r").read().splitlines()
    CHARS = " "

    if SIZE - NWORDS < 5:
        NWORDS = SIZE + 5

    if options["fillGrid"]:
        CHARS = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self) -> None:
        self.grid = self.get_grid()
        self.words = self.get_words()

    def get_grid(self):
        grid = []
        for _ in range(self.SIZE):
            for _ in range(self.SIZE):
                grid.append(random.choice(self.CHARS))
        return np.array(grid).reshape(self.SIZE, self.SIZE)

    def get_words(self):
        chsn_words = []

        if self.WORD_LEN == "short":
            length_range = range(3, 6)
        if self.WORD_LEN == "medium":
            length_range = range(6, 8)
        if self.WORD_LEN == "long":
            length_range = range(8, self.SIZE-1)
        if self.WORD_LEN == "mixed":
            length_range = range(3, self.SIZE-1)

        for wrd in self.WORDS:
            if len(wrd) in length_range:
                chsn_words.append(wrd)

        return random.sample(chsn_words, self.NWORDS)