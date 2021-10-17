#!/usr/bin/python3


class Format:
    @staticmethod
    def format_grid(grid):
        return str(grid).replace("[", " ").replace("]", " ").replace("'", "")

    @staticmethod
    def format_wrds(words):
        return str(words[:]).replace("'", "").replace("[", "").replace("]", "")
