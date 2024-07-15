"""
Morse Code Translator and Audio Generator

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

# -- Globals --
APP_TITLE: str = "MORSE CODE -.-"
MORSE_CODE_DICT: dict = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
                         "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
                         "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
                         "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----",
                         "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
                         "8": "---..", "9": "----."}

most_recent_audio_filepath: str = ""

# Colors
BG_COLOR: str = "#454679"  # Soft Indigo
LABEL_COLOR: str = "#FFC900"  # Tangerine Yellow

# Img filepaths, Dimensions and Padding
LOGO_FILEPATH: str = "app_logo.png"
DEFAULT_AUDIO_OUTPUT_FILEPATH: str = "morse_code_audio.wav"

IMG_WIDTH: int = 400
IMG_HEIGHT: int = 300

PADD_X: int = 50
PADD_Y: int = 60
BUTTON_X_PADD: tuple[int, int] = (5, 0)

# Buttons
SMALL_BUTTON_WIDTH: int = 15
BUTTON_TRANSLATE_TEXT: str = "Translate"
BUTTON_COPY_TEXT: str = "Copy"
BUTTON_PLAY_TEXT: str = "Play Audio"

# Labels
LABEL_YOUR_TEXT_TEXT: str = "Your text:"
LABEL_MORSE_CODE_OUTPUT_TEXT: str = "Morse code:"
LABEL_AUDIO_OUTPUT_TEXT: str = "Audio:"

# Entries
ENTRY_WIDTH: int = 30

# Fonts
LABEL_FONT: tuple[str, int, str] = ("Courier New", 14, "bold")
BUTTON_FONT: tuple[str, int, str] = ("Courier New", 10, "bold")

# MessageBox
MSGBOX_TITLE_SUCCESS: str = "Success"
MSGBOX_TITLE_WARNING: str = "Warning"

MSGBOX_MSG_COPY_SUCCESS: str = "The translation has been successfully copied to your clipboard."
MSGBOX_MSG_COPY_WARNING: str = "There is nothing to copy (yet)."
MSGBOX_MSG_PLAY_WARNING: str = "There is nothing to play (yet)."
MSGBOX_MSG_TRANSLATE_WARNING: str = "There is nothing to translate (yet)."

# Audio Settings
AUDIO_TONE: int = 800
AUDIO_VOLUME: float = 1.0
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_WPM: int = 20  # Words per Minute
AUDIO_READY_MESSAGE: str = "READY & SAVED"


# -- Functions --
def play_audio_file() -> None:
    """Play the most-recently-generated Morse code audio file.

    Returns
        None
    """

    audio_output_text: str = entry_audio_status.get()
    if audio_output_text:
        playsound(most_recent_audio_filepath)
    else:
        # Display a warning if no audio file has been created yet.
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_PLAY_WARNING)


def create_audio_file(normalized_text: str) -> None:
    """Generate a Morse code audio file from a normalized text.

    Args
        normalized_text (str): The text to be converted into audio.
    Returns
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
    pycw.output_wave(audio_filepath, normalized_text, tone=AUDIO_TONE, volume=AUDIO_VOLUME,
                     sample_rate=AUDIO_SAMPLE_RATE, wpm=AUDIO_WPM)

    # Save the audio filepath as the most recent one.
    global most_recent_audio_filepath
    most_recent_audio_filepath = audio_filepath

    # Change the state of the relevant entry widget to allow
    # the modification of its text. Delete the previous text,
    # insert the information that the audio file is ready,
    # and change the state again to disallow further modifications.
    entry_audio_status.config(state="normal")
    entry_audio_status.delete(0, tk.END)
    entry_audio_status.insert(0, AUDIO_READY_MESSAGE)
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

        create_audio_file(normalized_user_text)

    else:
        # Display a warning if the user has not provided any input.
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)


def copy_translation() -> None:
    """Copy the Morse code translation to the system clipboard.

    Returns
        None
    """

    morse_code_output_text: str = entry_morse_code_output.get()
    if morse_code_output_text:
        # Copy the translation to the systen clipboard and display
        # a success message to the user.
        pyperclip.copy(morse_code_output_text)
        msgbox.showinfo(title=MSGBOX_TITLE_SUCCESS, message=MSGBOX_MSG_COPY_SUCCESS)
    else:
        # Display a warning if no translation has been created yet.
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_COPY_WARNING)


# -- UI Configuration --
# Root window setup with padding and background color
root = tk.Tk()
root.title(APP_TITLE)
root.config(padx=PADD_X, pady=PADD_Y, bg=BG_COLOR)

# Canvas for displaying the application logo
canvas = tk.Canvas(width=IMG_WIDTH, height=IMG_HEIGHT)
app_logo = tk.PhotoImage(file=LOGO_FILEPATH)

# Center the logo image on the canvas
canvas.create_image(IMG_WIDTH // 2, IMG_HEIGHT // 2, image=app_logo)
canvas.config(bg=BG_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=4)

# Labels for user input and output fields with custom font and color
label_your_text = tk.Label(text=LABEL_YOUR_TEXT_TEXT, fg=LABEL_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_your_text.grid(column=0, row=1)

label_morse_code_output = tk.Label(text=LABEL_MORSE_CODE_OUTPUT_TEXT, fg=LABEL_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_morse_code_output.grid(column=0, row=2)

label_audio_output = tk.Label(text=LABEL_AUDIO_OUTPUT_TEXT, fg=LABEL_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_audio_output.grid(column=0, row=3)

# Entry widgets for user input, Morse code output, and audio file status
entry_text = tk.Entry(width=ENTRY_WIDTH)
entry_text.focus()  # Automatically focus on the text entry field
entry_text.grid(column=1, row=1)

entry_morse_code_output = tk.Entry(width=ENTRY_WIDTH)
entry_morse_code_output.config(state="readonly")  # Prevent user from editing Morse code output
entry_morse_code_output.grid(column=1, row=2)

entry_audio_status = tk.Entry(width=ENTRY_WIDTH)
entry_audio_status.config(state="readonly")  # Display audio file status, not editable by the user
entry_audio_status.grid(column=1, row=3)

# Buttons for translating text, copying Morse code, and playing audio
button_translate = tk.Button(text=BUTTON_TRANSLATE_TEXT, font=BUTTON_FONT, width=SMALL_BUTTON_WIDTH,
                             command=translate_to_morse_code)
button_translate.grid(column=2, row=1, padx=BUTTON_X_PADD)

button_copy = tk.Button(text=BUTTON_COPY_TEXT, font=BUTTON_FONT, width=SMALL_BUTTON_WIDTH, command=copy_translation)
button_copy.grid(column=2, row=2, padx=BUTTON_X_PADD)

button_play_audio = tk.Button(text=BUTTON_PLAY_TEXT, font=BUTTON_FONT, width=SMALL_BUTTON_WIDTH,
                              command=play_audio_file)
button_play_audio.grid(column=2, row=3, padx=BUTTON_X_PADD)

# Start the main event loop of the application
root.mainloop()
