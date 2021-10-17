## Description

This project generates word find / crossword puzzles.

You can solve the puzzles in an interactive graphical game or 
you can choose to save the puzzles as PDF or txt to print or use later.

## Instructions

- Run `pip` or `pip3` `install -r requirements.txt` in your terminal.
- Run the `gui.py` file for a graphical playable version.
- You can also run the `save.py` file to save a crossword puzzle grid in PDF & txt (OPTIONAL).

You can modify the options of the game in the `options.json` file:
- `size` is the width and height of the grid
- `numberOfWords` is the numbers of words you want in the puzzle. Try not to make the number bigger than the size.
- `wordLength` determines the length of the words chosen for you. The options are short, medium, long, mixed
- `wordFile` is the text file which you get the words from
- `fillGrid` is used for debugging in development but feel free to experiment with it. It takes true or false.

## For own use
The `grid.py` file returns the grid and wordlist. For use in a personal program add to code:

- `from grid import Grid`
- `obj = Grid()`
- `grid, words = obj.grid, obj.chsn_wrds`

Now you can use the `grid` and `words` variables in your program.    
