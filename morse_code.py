"""
Morse Code Translator and Audio Generator 0.2.0

This script provides a GUI application to translate text to Morse code,
generate audio files for the Morse code, and play them back.

Dependencies:
- tkinter for the GUI
- unidecode for transliteration of Unicode into ASCII
- pyperclip for clipboard operations
- pycw for Morse code audio generation
- playsound3 for audio playback

Usage:
Run this script directly to launch the application.
No command-line arguments are required.
"""

import tkinter as tk
from tkinter import messagebox as msgbox
from os.path import splitext, exists
import unidecode
import pyperclip
import pycw
from playsound3 import playsound
from playsound3.playsound3 import PlaysoundException

# -- Globals --
APP_TITLE: str = "Morse Code Translator and Audio Generator 0.2.0"
MORSE_CODE_DICT: dict = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
                         "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
                         "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
                         "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----",
                         "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
                         "8": "---..", "9": "----.", ".": ".-.-.-", ",": "--..--", "'": ".----.", "\"": ".-..-.",
                         "_": "..--.-", ":": "---...", ";": "-.-.-.", "?": "..--..", "!": "-.-.--", "-": "-....-",
                         "+": ".-.-.", "/": "-..-.", "(": "-.--.", ")": "-.--.-", "=": "-...-", "@": ".--.-.",
                         "$": "...-..-", "&": ".-..."}

most_recent_audio_filepath = ""

# Colors
BG_COLOR: str = "#454679"  # Soft Indigo
LABEL_AND_CHECKBOX_TEXT_COLOR: str = "#FFC900"  # Tangerine Yellow

# Images' filepaths, dimensions and padding
LOGO_FILEPATH: str = "app_logo.png"
DEFAULT_AUDIO_OUTPUT_FILEPATH: str = "morse_code_audio.wav"

IMG_WIDTH: int = 400
IMG_HEIGHT: int = 300

PADD_X: int = 60
PADD_Y: int = 60
BUTTON_X_PADD: tuple[int, int] = (5, 0)

# Buttons
BUTTON_WIDTH: int = 15
BUTTON_TRANSLATE_TEXT: str = "Translate"
BUTTON_COPY_TEXT: str = "Copy"
BUTTON_PLAY_TEXT: str = "Play Audio"

# Labels
LABEL_YOUR_TEXT_TEXT: str = "Your text:"
LABEL_MORSE_CODE_OUTPUT_TEXT: str = "Morse code:"
LABEL_AUDIO_OUTPUT_TEXT: str = "Audio:"

# Checkbox
TEXT_CHECKBOX: str = "Create audio"
VAL_ON_CHECKBOX: bool = True
VAL_OFF_CHECKBOX: bool = False

# Entries
ENTRY_WIDTH: int = 30

# Fonts
LABEL_FONT: tuple[str, int, str] = ("Courier New", 14, "bold")
CHECKBOX_FONT: tuple[str, int, str] = ("Courier New", 11, "bold")
BUTTON_FONT: tuple[str, int, str] = ("Courier New", 10, "bold")

# MessageBox
MSGBOX_TITLE_SUCCESS: str = "Success"
MSGBOX_TITLE_WARNING: str = "Warning"
MSGBOX_TITLE_ERROR: str = "Error"

MSGBOX_MSG_COPY_SUCCESS: str = "The translation has been successfully copied to your clipboard."
MSGBOX_MSG_COPY_WARNING: str = "There is nothing to copy (yet)."
MSGBOX_MSG_PLAY_WARNING: str = "There is nothing to play (yet)."
MSGBOX_MSG_PLAY_FILE_NF_ERROR: str = "The file that has just been created doesn't seem to exist anymore."
MSGBOX_MSG_TRANSLATE_WARNING: str = "There is nothing to translate (yet)."
MSGBOX_MSG_TRANSLATE_PERMISS_ERROR: str = "The program doesn't have permission to save files to the current location."

# Audio Settings
AUDIO_TONE: int = 800
AUDIO_VOLUME: float = 1.0
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_WPM: int = 20  # Words per Minute
AUDIO_READY_MESSAGE: str = "READY:"


# -- Functions --
def play_audio_file() -> None:
    """Play the most-recently-generated Morse code audio file.

    Raises:
        PlaysoundException: If the audio file can't be played.

    Returns:
        None
    """

    audio_output_text: str = entry_audio_status.get()
    if audio_output_text:
        try:
            playsound(most_recent_audio_filepath)
        except PlaysoundException as e:
            # Display an error if the audio file can't be played.
            msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=str(e))
    else:
        # Display a warning if no audio file has been created yet.
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_PLAY_WARNING)


def create_audio_file(normalized_text: str) -> None:
    """Generate a Morse code audio file from a normalized text.

    Args:
        normalized_text (str): The text to be converted into audio.

    Raises:
        PermissionError: If the audio file can't be created.

    Returns:
        None
    """

    # Incrementally, find the first unused audio filename to avoid
    # overwriting previous ones.
    counter: int = 0
    audio_filepath = DEFAULT_AUDIO_OUTPUT_FILEPATH
    audio_file_name, audio_file_ext = splitext(audio_filepath)

    while exists(audio_filepath):
        counter += 1
        audio_filepath = f"{audio_file_name}_{counter}{audio_file_ext}"

    # Generate the audio file according to the specified settings.
    try:
        pycw.output_wave(audio_filepath, normalized_text, tone=AUDIO_TONE, volume=AUDIO_VOLUME,
                         sample_rate=AUDIO_SAMPLE_RATE, wpm=AUDIO_WPM)
    except PermissionError:
        # Display an error if the audio file can't be created
        # due to lack of permissions.
        msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=MSGBOX_MSG_TRANSLATE_PERMISS_ERROR)
    else:
        # Save the audio filepath as the most recent one.
        global most_recent_audio_filepath
        most_recent_audio_filepath = audio_filepath

        # Change the state of the relevant entry widget to allow
        # the modification of its text. Delete the previous text,
        # insert the information that the audio file is ready,
        # and change the state again to disallow further modifications.
        entry_audio_status.config(state="normal")
        entry_audio_status.delete(0, tk.END)
        entry_audio_status.insert(0, f"{AUDIO_READY_MESSAGE}: {most_recent_audio_filepath}")
        entry_audio_status.config(state="readonly")


def translate_to_morse_code() -> None:
    """Translate the text entered by the user into Morse code
    and display it in the GUI. The function also calls
    'create_audio_file' to generate the corresponding
    Morse code audio file.

    Returns:
        None
    """

    user_text: str = entry_text.get()

    if user_text:
        # Eliminate diacritical letters by finding the closest ASCII
        # representations for all characters.
        normalized_user_text: str = unidecode.unidecode(user_text).upper()
        split_user_text: list = normalized_user_text.split()

        # Translate the normalized text to Morse code.
        # Each letter is looked up in the MORSE_CODE_DICT,
        # and words are separated by a slash with spaces.
        mcode: str = " / ".join(' '.join(map(lambda c: MORSE_CODE_DICT.get(c, ""), word)) for word in split_user_text)

        # Change the state of the relevant entry widget to allow
        # the modification of its text. Delete the previous text,
        # insert the translation, and change the state again
        # to disallow further modifications.
        entry_morse_code_output.config(state="normal")
        entry_morse_code_output.delete(0, tk.END)
        entry_morse_code_output.insert(0, mcode)
        entry_morse_code_output.config(state="readonly")

        if audio_requested.get():
            create_audio_file(normalized_user_text)
        else:
            # Change the state of the relevant entry widget to allow
            # the modification of its text. Delete the previous text,
            # and change the state again to disallow further
            # modifications.
            entry_audio_status.config(state="normal")
            entry_audio_status.delete(0, tk.END)
            entry_audio_status.config(state="readonly")

            global most_recent_audio_filepath
            most_recent_audio_filepath = ""

    else:
        # Display a warning if the user has not provided any input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)


def copy_translation() -> None:
    """Copy the Morse code translation to the system clipboard.

    Returns:
        None
    """

    morse_code_output_text: str = entry_morse_code_output.get()
    if morse_code_output_text:
        # Copy the translation to the systen clipboard and display
        # a success message to the user
        pyperclip.copy(morse_code_output_text)
        msgbox.showinfo(title=MSGBOX_TITLE_SUCCESS, message=MSGBOX_MSG_COPY_SUCCESS)
    else:
        # Display a warning if no translation has been created yet
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_COPY_WARNING)


# -- UI Configuration --
# Root window setup with padding and bg color, and a checkbox variable
root = tk.Tk()
root.title(APP_TITLE)
root.config(padx=PADD_X, pady=PADD_Y, bg=BG_COLOR)

audio_requested = tk.BooleanVar(value=VAL_OFF_CHECKBOX)  # Whether to produce the audio file (defaults to off)

# Canvas for displaying the application logo
canvas = tk.Canvas(width=IMG_WIDTH, height=IMG_HEIGHT)
app_logo = tk.PhotoImage(file=LOGO_FILEPATH)

# Center the logo image on the canvas
canvas.create_image(IMG_WIDTH // 2, IMG_HEIGHT // 2, image=app_logo)
canvas.config(bg=BG_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=4)

# Labels for user input and output fields with custom font and color
label_your_text = tk.Label(text=LABEL_YOUR_TEXT_TEXT, fg=LABEL_AND_CHECKBOX_TEXT_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_your_text.grid(column=0, row=1)

label_morse_code_output = tk.Label(text=LABEL_MORSE_CODE_OUTPUT_TEXT, fg=LABEL_AND_CHECKBOX_TEXT_COLOR, bg=BG_COLOR,
                                   font=LABEL_FONT)
label_morse_code_output.grid(column=0, row=3)

label_audio_output = tk.Label(text=LABEL_AUDIO_OUTPUT_TEXT, fg=LABEL_AND_CHECKBOX_TEXT_COLOR, bg=BG_COLOR,
                              font=LABEL_FONT)
label_audio_output.grid(column=0, row=4)

# Entry widgets for user input, Morse code output, and audio status
entry_text = tk.Entry(width=ENTRY_WIDTH)
entry_text.focus()  # Automatically focus on the text entry field
entry_text.grid(column=1, row=1)

entry_morse_code_output = tk.Entry(width=ENTRY_WIDTH)
entry_morse_code_output.config(state="readonly")  # Prevent editing Morse code output
entry_morse_code_output.grid(column=1, row=3)

entry_audio_status = tk.Entry(width=ENTRY_WIDTH)
entry_audio_status.config(state="readonly")  # Display audio file status, not editable by the user
entry_audio_status.grid(column=1, row=4)

# Buttons for translating text, copying Morse code, and playing audio
button_translate = tk.Button(text=BUTTON_TRANSLATE_TEXT, font=BUTTON_FONT, width=BUTTON_WIDTH,
                             command=translate_to_morse_code)
button_translate.grid(column=2, row=1, padx=BUTTON_X_PADD)

button_copy = tk.Button(text=BUTTON_COPY_TEXT, font=BUTTON_FONT, width=BUTTON_WIDTH, command=copy_translation)
button_copy.grid(column=2, row=3, padx=BUTTON_X_PADD)

button_play_audio = tk.Button(text=BUTTON_PLAY_TEXT, font=BUTTON_FONT, width=BUTTON_WIDTH,
                              command=play_audio_file)
button_play_audio.grid(column=2, row=4, padx=BUTTON_X_PADD)

# Checkbox for deciding whether to produce an audio file
checkbox_audio_request = tk.Checkbutton(text=TEXT_CHECKBOX, variable=audio_requested, onvalue=VAL_ON_CHECKBOX,
                                        offvalue=VAL_OFF_CHECKBOX, bg=BG_COLOR, highlightthickness=0,
                                        font=CHECKBOX_FONT, fg=LABEL_AND_CHECKBOX_TEXT_COLOR, activebackground=BG_COLOR,
                                        activeforeground=LABEL_AND_CHECKBOX_TEXT_COLOR, selectcolor=BG_COLOR)
checkbox_audio_request.grid(column=1, row=2)

# Start the main event loop of the application
root.mainloop()
