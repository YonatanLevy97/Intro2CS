from boggle_gui import BoggleGUI
from boggle_model import BoogleModel
from start_gui import StartGUI
from typing import Callable


class BoggleGame:
    """ this class is the manager of the game that merges the logic of the game and the gui elements"""
    def __init__(self, play_again=False):
        if not play_again:
            self._welcome_page = StartGUI()
            if not self._welcome_page.game_started:
                return
        self._boggle_model = BoogleModel()
        self._board = self._boggle_model.board
        self._boggle_gui = BoggleGUI(self._board)

        buttons = self._boggle_gui.get_button_chars()
        for button_text in buttons:
            action = self.create_button_action(buttons[button_text])
            self._boggle_gui.set_button_command(button_text, action)
        self._boggle_gui.update_display("")
        self.run()

    def create_button_action(self, button) -> Callable[[], None]:
        """
        this function assigns a function to every button from the gui class
        :param button: a button from the gui class
        :return: the appropriate function for the given button
        """
        def fun() -> None:
            does_return = False
            if button[0]["text"] == 'choose':
                word = self._boggle_model.choose_word()
                if word:
                    self._boggle_gui.update_words_display(word, self._boggle_model.score)
            elif button[0]["text"] == 'clear':
                self._boggle_model.current_path = list()
            else:
                cord = (button[1][0], button[1][1])
                if self.is_in_path(cord):
                    if self.compare_cords(cord, self._boggle_model.current_path[-1]):
                        self._boggle_gui.remove_letter_from_display(len(button[0]["text"]))
                        self._boggle_model.current_path.pop()
                    does_return = True
                elif self.is_valid_press(cord):
                    self._boggle_model.update_current_path(cord)
                else:
                    does_return = True
            self._boggle_gui.button_path = self._boggle_model.current_path
            if does_return:
                return
            self._boggle_gui.update_display(button[0]["text"])
        return fun

    def is_in_path(self, cord) -> bool:
        """
        this function checks if the given coordinates are in the current path excluding the last cell
        :param cord: a tuple containing the coordinates of the button that was pressed
        :return: True if the coordinates are in the current path excluding the last cell and false otherwise
        """
        in_path = False
        for path_cord in self._boggle_model.current_path:
            if self.compare_cords(cord, path_cord):
                in_path = True
                break
        return in_path

    def compare_cords(self, cord_1, cord_2) -> bool:
        """
        this function compares two tuples of coordinates
        :param cord_1: a tuple containing the first pair of coordinates that are to be compared
        :param cord_2: a tuple containing the first pair of coordinates that are to be compared
        :return: True if the coordinates are identical and False otherwise
        """
        return cord_1[0] == cord_2[0] and cord_1[1] == cord_2[1]

    def is_valid_press(self, cord) -> bool:
        """
        this function checks if the given coordinates are valid for the current path
        :param cord: the coordinates of the pressed button
        :return: True if the coordinates are valid for the current path and false otherwise
        """
        is_valid = True
        if len(self._boggle_model.current_path) != 0:
            y_distance = abs(self._boggle_model.current_path[-1][0] - cord[0])
            x_distance = abs(self._boggle_model.current_path[-1][1] - cord[1])
            is_valid = (y_distance in [0, 1]) and (x_distance in [0, 1]) and (cord not in self._boggle_model.current_path)
        return is_valid

    def run(self) -> None:
        """
        this function runs the main frame of the game
        :return: None
        """
        self._boggle_gui.run()


if __name__ == '__main__':
    B = BoggleGame()

