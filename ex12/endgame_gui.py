import tkinter as tki

BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'slateblue'

BUTTON_STYLE = {
    "font": ("Courier", 30),
    "borderwidth": 1,
    "relief": tki.RAISED,
    "bg": REGULAR_COLOR,
    "activebackground": BUTTON_ACTIVE_COLOR
}


class EndGameGUI:
    """
    this class is contains the endgame screen gui:
    it contains a play again button,the final score
    and a listbox with all of the words that were guessed during the round
    """
    def __init__(self, all_words, score):
        self.root = tki.Tk()
        self.root.title("GAME OVER")
        self.root.resizable(False, False)
        end_frame = tki.Frame(self.root, bg=REGULAR_COLOR)
        end_frame.pack(fill=tki.BOTH, expand=True)

        score_display = tki.Label(end_frame, font=("Courier bolt", 20), bg=REGULAR_COLOR, width=10, relief="ridge",
                                  text=f"Final score: {score}")

        words_display = tki.Frame(end_frame, bg=REGULAR_COLOR, relief="ridge")
        word_display_title = tki.Label(words_display, font=("Courier Bolt", 14), width=10, height=2,
                                       text="Words found: \n", bg=REGULAR_COLOR)
        word_display_title.pack(side=tki.TOP, fill=tki.BOTH)
        scrollbar = tki.Scrollbar(words_display)
        scrollbar.pack(side=tki.RIGHT, fill=tki.BOTH)

        listbox_word = tki.Listbox(words_display, yscrollcommand=scrollbar.set, font=("Courier", 14),
                                   bg=REGULAR_COLOR, width=10, height=7, selectbackground=BUTTON_ACTIVE_COLOR)

        for word in all_words:
            listbox_word.insert(tki.END, word)

        listbox_word.pack(side=tki.RIGHT, fill=tki.BOTH)
        scrollbar.config(command=listbox_word.yview)

        words_display.pack(side=tki.LEFT, fill=tki.BOTH, pady=5, padx=5)
        score_display.pack(side=tki.TOP, fill=tki.BOTH, pady=5, padx=5)

        play_again_label = tki.Label(end_frame)
        play_again_label.pack(side=tki.BOTTOM, fill=tki.BOTH)

        def play_again() -> None:
            """
            this function starts a new boggle round
            :return: None
            """
            from boggle import BoggleGame
            self.root.destroy()
            BoggleGame(True)

        self.play_again_image = tki.PhotoImage(file="images/play_again.png")
        self.play_again_button = tki.Button(play_again_label, image=self.play_again_image)
        self.play_again_button.configure(command=play_again)
        self.play_again_button.pack(side=tki.BOTTOM, fill=tki.BOTH)
