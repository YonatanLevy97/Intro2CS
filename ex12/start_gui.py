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


class StartGUI:
    """ this class cantians the start screen gui: it contains the start button and a welcome statement """
    def __init__(self):
        def start():
            self.game_started = True
            self.root.destroy()

        self.root = tki.Tk()
        self.root.resizable(False, False)
        self.root.title("Boggle")
        self.game_started = False

        start_frame = tki.Frame(self.root, bg=REGULAR_COLOR)
        start_frame.pack(fill=tki.BOTH)

        start_label = tki.Label(start_frame, font=("Courier bolt", 20), bg=REGULAR_COLOR, text="Welcome to Boggle!", relief="ridge",border=2, padx=20, pady=20)
        start_label.pack(fill=tki.BOTH,side=tki.TOP)

        play_photo = tki.PhotoImage(file="images/play.png")
        play_button = tki.Button(start_frame, image=play_photo, border=5)
        play_button.configure(command=start)
        play_button.pack(fill=tki.BOTH, side=tki.BOTTOM)
        self.root.mainloop()
