import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending

class TrieDictionary(BoggleDictionary):
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        """
        iterates over every word in the dictionary text file and adds it to a Trie Tree Node
        """
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            words = set() # Edge case: repeated words in dictionary text file
            for line in wordsfile:
                # Ed discussions say not to edit below line
                word = line.strip().lower() #strip white, all lower
                word = word.replace(" ", "") # Edge case: added this line to not mess with line above, and to get rid of white spaces # delete?
                current = self.root # set root
                # Edge case: blank lines
                # Edge case: make sure root is not set as word by blank lines
                if len(word) > 0 and word not in words: # skip blank lines # checks for repeated words in dictionary text file
                    words.add(word) # Edge Case: adds word if not a repeated word in the dictionary text file
                    for letter in word:
                        if letter not in current.children: # for each letter in a word, check if child node
                            current.children[letter] = TrieNode() # if not, create one
                        current = current.children[letter] # move to child node and repeat down word
                    current.is_word = True # at end of word, set value to true to indicate word

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """
        # Ed discussion: states that empty input string for 'prefix' will not show up

        current = self.root
        prefix = prefix.strip().lower() # deletes whitespace and lowercases letters, # prefix will not have input = ''
        for letter in prefix:
            if letter in current.children:  # if can't find prefix return false
                current = current.children[letter]
            else:
                return None
        return current # if whole prefix found, return prefix string, already stored as current string in node

    def is_prefix(self, prefix: str) -> bool:
        """
        is_prefix will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns False.
        Otherwise, returns True that 'prefix' exists in the Trie.
        """
        traverse = self.traverse(prefix) # Call traverse method to detect if string is a prefix or not
        if traverse is not None:
            return True
        else:
            return False

    def contains(self, word: str) -> bool:
        """
        contains will traverse the Trie down a given path of letters `word`.
        If there is ever a missing child node and the input string isn't the end of a word, then returns False.
        Otherwise, returns True that 'word' exists in the Trie and is the end of a word.
        """
        # Ed discussion: states that the text file won't contain empty line

        traverse = self.traverse(word) # Call traverse method to detect if string is a word or not
        if traverse is not None and traverse.is_word:
            return True  # if whole word found and is marked as word
        else:
            return False # no if not marked as word

    def _collect_words_from_node(self, node: TrieNode, word: str, words: list[str]) -> None:
        """
        Helper function to recursively collect all words in the Trie.
        """
        if node.is_word:
            words.append(word)  # Add the current word to the list

        # Recursively explore child nodes
        # for loop is skipped when no more children left (i.e. end of the word, is_word = true). Then it backtracks to the previous recursive call (i.e. parent node)
        for char, child_node in node.children.items():
            self._collect_words_from_node(child_node, word + char, words)

    def __iter__(self) -> typing.Iterator[str]:
        """
        Used to access all words in the trie object.
        Need to return words in a lexicographic order.
        __iter__ called when accessing a for loop or other iterables (i.e. list(), next(), etc)
        """
        words = []
        self._collect_words_from_node(self.root, "", words)  # Collect all words in a list
        words = sorted(words) # sort words to export in alphabetical order
        return iter(words)  # Return an iterator over the list of words