import copy
import random
from operator import index
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """
    """
    STATIC DEFINITIONS
    """
    # 8 possible directions in relation to the 1st letter coordinates
    # left, lower left diag, bottom, lower right diag, right, upper right diag, top, upper left diag
    _directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c]) 
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None


    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """
        # Video Notes:
        # This function doesn't care that the words are <4 characters
        # Can't have duplicating letters from same coordinate

        word = word.lower()

        # Search through board for the 1st letter to start the recursive search
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == word[0]: # If coordinate matches the first letter of the word
                    path =[]
                    if self.recursive_search(i, j, 0, word, path): # Start a recursive search on the surrounded spaces around the 1st letter for the 2nd+ letters
                        return path # returns path coordinates if found
        # Returns None if the first letter cannot be found
        return None

    def recursive_search(self, i, j, index, word, path):
        """
        Searches for the letters surrounding the index letter of the word
        """
        # if the direction is out of bounds, already visited, or the letter doesn't match, return False
        if (i < 0 or i >= self.size or j < 0 or j >= self.size) or ((i,j) in path) or (self.board[i][j] != word[index]):
            return False

        # Adding the current coordinates to the path to not repeat coordinates
        path.append((i,j))

        # End Recursive loop if whole word found
        if len(path) == len(word):
            return True

        # Recursively search for the next letter in the surrounding cells
        for dx,dy in MyGameManager._directions: # calls static name directions for the 8 possible spaces around the letter
            if  self.recursive_search(i+dx, j+dy, index + 1, word, path): # If path is found
                return True

        #Remove the current coordinate from path if there's no successful match after finding initial path
        path.pop()
        return False

    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.lower()
        if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """
        # Find all the unique letters on the board
        letters_on_board = set()
        for row in self.board:
            letters_on_board.update(row)

        words_dict = set()
        for word in self.dictionary: # loop through dictionary text file
            if len(word) > SHORT and word[0] in letters_on_board: # if word is > SHORT & first letter exists on the board
                path = self.find_word_in_board(word) # initialize find_word_on_board
                if path: # add to words found by computer & not human
                    words_dict.add(word)
        return words_dict

    def get_dice_adjacent_directory(self):
        """
        Gets up to 8 plausible cell coordinates surrounding each cell
        """
        dice_directory = dict()
        for i in range(self.size):
            for j in range(self.size):
                dice_directory[(i,j)] = set()
                for dx, dy in MyGameManager._directions:  # calls static name directions for the 8 possible spaces around the letter
                    if i + dx >= 0 and i + dx <= self.size - 1 and j + dy >= 0 and j + dy <= self.size - 1: # check if valid coordinate
                        dice_directory[(i,j)].add((i + dx, j + dy))
        return dice_directory

    def board_word_search_helper(self, i, j, board_dict: dict, word: str, words: set, path):
        """
        Pulls all words existing on board, starting with given cell.
        """
        current_coord = (i, j)
        path.append(current_coord)  # also denotes visited items
        word += self.board[i][j] # need to figure out how to keep these in loop but reset when n
        if self.dictionary.contains(word) and len(word) > SHORT: #if word is in dictionary and is >=4, then add to board word list
            words.add(word)
        if not self.dictionary.is_prefix(word):
            return # stops this search 'strand' if the string is not a prefix
        for neighbor in board_dict[(i,j)]:
            if neighbor not in path:
                path_new = path
                i_new, j_new = neighbor
                self.board_word_search_helper(i_new, j_new, board_dict, word, words, path = path[:])

    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """
        all_words_board = set() #init blank set for all strings on the board
        board_dict = self.get_dice_adjacent_directory()
        for i in range(0, self.size):
            for j in range(0, self.size):
                words = set()
                self.board_word_search_helper(i, j, board_dict, word = "", words= words, path = [])
                all_words_board.update(words)
        return all_words_board