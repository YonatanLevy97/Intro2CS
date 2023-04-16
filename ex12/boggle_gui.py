import tkinter as tki
from typing import Callable, Dict, List, Any
from endgame_gui import EndGameGUI

BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'slateblue'

BUTTON_STYLE = {
    "font": ("Courier", 30),
    "borderwidth": 2,
    "relief": tki.RAISED,
    "bg": REGULAR_COLOR,
    "activebackground": BUTTON_ACTIVE_COLOR
}


class BoggleGUI:
    """ this class is the main gui of the game and all its main elements"""
    _buttons: Dict[str, tuple[tki.Button, [int, int]]] = {}

    def __init__(self, board):
        self._score = 0
        self._board = board
        self._all_words = list()
        self.button_path = list()

        root = tki.Tk()
        root.title("Boggle")
        root.resizable(False, False)

        self._main_window = root
        self.create_all_displays()
        self._create_buttons_in_lower_frame()
        self.countdown(180)

    def create_all_displays(self) -> None:
        """
        this function creates all the frames and displays of the game
        :return: None
        """
        self.left_side_frame = tki.Frame(self._main_window, bg=REGULAR_COLOR)
        self.left_side_frame.pack(side=tki.LEFT, fill=tki.BOTH)

        self.setting_frame = tki.Frame(self.left_side_frame, bg=REGULAR_COLOR)
        self.setting_frame.pack(side=tki.TOP, fill=tki.BOTH)

        self.timer_label = tki.Label(self.setting_frame, font=("Courier", 15), bg=REGULAR_COLOR, relief="ridge",
                                     text="time:")
        self.timer_label.pack(side=tki.TOP, fill=tki.BOTH)

        self.score_label = tki.Label(self.setting_frame, font=("Courier", 15), bg=REGULAR_COLOR,
                                     relief="ridge", text=f'score: {self._score}')
        self.score_label.pack(side=tki.TOP, fill=tki.BOTH)

        self._words_lable = tki.Frame(self.setting_frame, bg=REGULAR_COLOR)
        self._words_lable.pack(side=tki.TOP, fill=tki.BOTH)

        self.scrollbar = tki.Scrollbar(self._words_lable)
        self.scrollbar.pack(side=tki.RIGHT, fill=tki.BOTH)

        self.listbox_word = tki.Listbox(self._words_lable, yscrollcommand=self.scrollbar.set, font=("Courier", 15),
                                        bg=REGULAR_COLOR, width=17, height=15, selectbackground=BUTTON_ACTIVE_COLOR)

        self.listbox_word.pack(side=tki.LEFT, fill=tki.BOTH)
        self.scrollbar.config(command=self.listbox_word.yview)

        self._outer_frame = tki.Frame(self._main_window, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._display_label = tki.Label(self._outer_frame, font=("Courier", 30),
                                        bg=REGULAR_COLOR, width=23, relief="ridge")
        self._display_label.pack(side=tki.TOP, fill=tki.BOTH)

        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

    def end_game_pop_up(self) -> None:
        """
        this function destroys the root window and calls the EndGameGUI class to finish the game
        :return: None
        """
        self._main_window.destroy()
        EndGameGUI(self._all_words, self._score)

    def countdown(self, count) -> None:
        """
        this function creates and sets the games timer
        :param count: the amount of time until the end of the round
        :return: None
        """
        sec = str(count % 60)
        minute = str(count // 60 if count >= 60 else 0)

        sec = ('0' + sec) if len(sec) == 1 else sec
        minute = ('0' + minute) if len(minute) == 1 else minute

        self.timer_label['text'] = f'time left: {minute}:{sec}'

        if count > 0:
            # call countdown again after 1000ms (1s)
            self._main_window.after(1000, self.countdown, count - 1)

        else:
            self.end_game_pop_up()

    def run(self) -> None:
        """
        this function runs the games main frame
        :return: None
        """
        self._main_window.mainloop()

    def update_display(self, display_text: str) -> None:
        """
        this function updates the display according the button that was pressed
        :param display_text: the string that is to be added to the text display
        :return: None
        """
        if display_text in ['clear', 'choose']:
            self._display_label["text"] = ""
            self.__clear_buttons()
        else:
            self._display_label["text"] += display_text

    def remove_letter_from_display(self, text_len: int) -> None:
        """
        this function removes the last letters on the button that was last clicked from the display label
        :param text_len: the length of string inside the button that was last pressed
        :return: None
        """
        self._display_label["text"] = self._display_label["text"][:-text_len]

    def update_words_display(self, word: str, score: int) -> None:
        """
        this function updates guessed words bank according to the word that was guessed
        :param word: a string containing the word in the path that was guessed
        :param score: an int containing the players current score
        :return: None
        """
        if word not in self._all_words:
            self._all_words.append(word)
            self.listbox_word.insert(tki.END, word)
        else:
            def regular_color():
                self.listbox_word.configure(bg=REGULAR_COLOR)

            self.listbox_word.configure(bg=BUTTON_ACTIVE_COLOR)
            self.listbox_word.after(200, regular_color)

        self._score = score
        self.score_label["text"] = f'score: {self._score}'

    def set_button_command(self, button_name: str, cmd: Callable[[], None]) -> None:
        """
        this function is used to assaign a given command to a button
        :param button_name: the key of the button to be set in the buttons dict
        :param cmd: the command that is to be set to the specified button
        :return: None
        """
        self._buttons[button_name][0].configure(command=cmd)

    def _create_buttons_in_lower_frame(self) -> None:
        """
        this function places the button grid in the lower frame of the game gui
        :return: None
        """
        for i in range(4):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(5):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(4):
            for j in range(4):
                self._make_button(self._board[i][j], i, j)

        self._make_button("clear", 4, 0, columnspan=2)
        self._make_button("choose", 4, 2, columnspan=2)

    def _make_button(self, button_char: str, row: int, col: int,
                     rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        """
        this button defines a button according to the given parameters and inserts it in the buttons dict
        :param button_char: a string contains the button's key in the buttons dict
        :param row: an int containing the row of the button in the lower frame grid
        :param col: an int containing the column of the button in the lower frame grid
        :param rowspan: an int containing the row span of the button in the grid
        :param columnspan: an int containing the column span of the button in the grid
        :return: the button that is created according to the given parameters
        """
        button = tki.Button(self._lower_frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[f'{row},{col}'] = (button, (row, col))
        self.last_button_pressed = None

        def _on_press(event: Any) -> None:
            def regular_color():
                button['background'] = REGULAR_COLOR

            if button['background'] == REGULAR_COLOR:
                if self.is_valid_press((row, col)):
                    button['background'] = BUTTON_ACTIVE_COLOR
                else:
                    regular_color()
            else:
                if not self.is_in_button_path((row, col)):
                    regular_color()

            if button_char in {"clear", "choose"}:
                button.after(100, regular_color)
                self.__clear_buttons()

        button.bind("<Button-1>", _on_press)
        return button

    def is_valid_press(self, cord) -> bool:
        """
        this function checks if the given coordinates of
        the button that was pressed  are valid according to the current path
        :param cord: a tuple containing the coordinates of the button that was pressed
        :return: True if the keypress if valid and False otherwise
        """
        is_valid = True
        if len(self.button_path) != 0:
            y_distance = abs(self.button_path[-1][0] - cord[0])
            x_distance = abs(self.button_path[-1][1] - cord[1])
            is_valid = (y_distance in [0, 1]) and (x_distance in [0, 1]) and (
                    cord not in self.button_path)
        return is_valid

    def is_in_button_path(self, cord) -> bool:
        """
        this function checks if the given coordinates of a button are in the current path
        :param cord: a tuple containing the coordinates of the pressed button
        :return: True if the coordinates are in the path and false otherwise
        """
        in_path = False
        for path_cord in self.button_path[:-1]:
            if self.compare_cords(cord, path_cord):
                in_path = True
                break
        return in_path

    def compare_cords(self, cord_1, cord_2) -> bool:
        """
        this function compares with two cords
        :param cord_1: a tuple containing the first pair of coordinates that are to be compared
        :param cord_2: a tuple containing the first pair of coordinates that are to be compared
        :return: True if the coordinates are identical and False otherwise
        """
        return cord_1[0] == cord_2[0] and cord_1[1] == cord_2[1]

    def get_button_chars(self):
        """
        this function returns the buttons dict
        :return: a dictionary containing the gui buttons
        """
        return self._buttons

    def __clear_buttons(self) -> None:
        """
        this function changes the colors of all buttons back to normal
        :return: None
        """
        self.update_display("")
        for button in self._buttons.values():
            button[0]["background"] = REGULAR_COLOR
