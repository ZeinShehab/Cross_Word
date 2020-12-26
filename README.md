## Description

This project generates word find / crossword puzzles.

You can solve the puzzles in an interactive graphical game or 
you can choose to save the puzzles as PDF or txt to print or use later.

## Instructions

- Run `pip` or `pip3` `install -r requirements.txt` in your terminal.
- Run the `gui.py` file for a graphical playable version.
- You can also run the `save.py` file to save a crossword puzzle grid in PDF & txt (OPTIONAL).


## For own use
The `grid.py` file returns the grid and wordlist. For use in a personal program add to code:

- `from grid import Grid`
- `grid, words = Grid.main()` which returns the grid and wordlist.

Now you can use the `grid` and `words` variables in your program.    
