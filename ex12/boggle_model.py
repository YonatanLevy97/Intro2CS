from boggle_board_randomizer import randomize_board
from ex12_utils import is_valid_path

""" this function opens the legal words list from the given file """
with open("boggle_dict.txt", "r") as words_dict:
    WORDS = words_dict.read().splitlines()


class BoogleModel:
    """ this class contains all of the logic of the game"""
    def __init__(self):
        self.board = randomize_board()
        self.current_path = list()
        self.chosen_words = set()
        self.score = 0

    def choose_word(self) -> str:
        """
        this function checks if a path that was chosen is a legal path and updates the score accordingly
        :return: a string containing the word if a word was chosen and None otherwise
        """
        chosen_word = is_valid_path(self.board, self.current_path, WORDS)
        if chosen_word and (chosen_word not in self.chosen_words):
            self.score += (len(self.current_path) ** 2)
            self.chosen_words.add(chosen_word)
        self.current_path = list()
        return chosen_word

    def clear_path(self) -> None:
        """
        this function resets the current letter path
        :return: None
        """
        self.current_path = list()

    def update_current_path(self, coordinates) -> None:
        """
        this function adds the coordinates of a letter that was chosen to the current path
        :param coordinates: the coordinates of the letter that was chosen on the board
        :return: None
        """
        self.current_path.append(coordinates)
