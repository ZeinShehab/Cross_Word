#!/usr/bin/python3

import random
from setup import Setup


class Grid(Setup):
    def __init__(self):
        super(Grid, self).__init__()

        self.pos = []
        self.main()

    def get_pos(self, wrd):
        direction = random.choice([-1, 1])                              # Reverse(-1) or normal(1)
        orientation = random.choice([-1, 0, 1])                         # Horizontal(-1) or Vertical(1) or Diagonal(0)
        x_diag_dirc, y_diag_dirc = random.sample([1, 1, -1, -1], 2)     # Left(=) or Right(><) diagonal
        
        normal_range = range(0, self.SIZE-len(wrd))
        reverse_range = range(len(wrd), self.SIZE)

        self.pos = []

        if orientation != 0:                                            # Horizontal or Vertical
            cord_1 = random.randint(0, self.SIZE-1)
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

        if self.is_collide(wrd):           # Checking for collsion between words
            self.get_pos(wrd)

    def is_collide(self, wrd):
        collide = False

        for k in self.pos:
            letter = wrd[self.pos.index(k)]
            grid_letter = self.grid[k[0], k[1]]

            if grid_letter != " " and grid_letter != letter:
                collide = True

        return collide

    def put_wrd(self, wrd, pos):
        for cord, let in zip(pos, wrd):
            self.grid[cord[0], cord[1]] = let

    def main(self):
        for wrd in self.words:
            self.get_pos(wrd)
            self.put_wrd(wrd, self.pos)