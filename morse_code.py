"""
Morse Code Translator and Audio Generator 0.3.0

This script provides a GUI application to translate text to Morse code, and vice versa,
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
import re
import unidecode
import pyperclip
import pycw
from playsound3 import playsound
from playsound3.playsound3 import PlaysoundException

# -- Globals --
APP_TITLE: str = "Morse Code Translator and Audio Generator 0.3.0"
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
STATIC_TEXT_COLOR: str = "#FFC900"  # Tangerine Yellow

# Images' filepaths, dimensions and padding
LOGO_FILEPATH: str = "app_logo.png"
DEFAULT_AUDIO_OUTPUT_FILEPATH: str = "morse_code_audio.wav"

IMG_WIDTH: int = 400
IMG_HEIGHT: int = 300

PADD_X: int = 60
PADD_Y: int = 60
BUTTON_X_PADD: tuple[int, int] = (5, 0)

# Buttons
BUTTON_SMALL_WIDTH: int = 15
BUTTON_LARGE_WIDTH: int = 31
BUTTON_TRANSLATE_TO_MORSE_TEXT: str = "To Morse"
BUTTON_TRANSLATE_TO_PLAIN_TEXT: str = "To Plain Text"
BUTTON_COPY_TEXT: str = "Copy"
BUTTON_PLAY_TEXT: str = "Play Audio"

# Labels
LABEL_PLAIN_TEXT_IO_TEXT: str = "Plain Text:"
LABEL_MORSE_CODE_IO_TEXT: str = "Morse Code:"
LABEL_AUDIO_STATUS_TEXT: str = "Audio Status:"

# Checkbox
CHECKBOX_TEXT: str = "Create Audio"
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

MSGBOX_MSG_COPY_SUCCESS: str = "The text has been successfully copied to your clipboard."
MSGBOX_MSG_COPY_WARNING: str = "There is nothing to copy (yet)."
MSGBOX_MSG_PLAY_WARNING: str = "There is nothing to play (yet)."
MSGBOX_MSG_PLAY_FILE_NF_ERROR: str = "The file that has just been created doesn't seem to exist anymore."
MSGBOX_MSG_TRANSLATE_WARNING: str = "There is nothing to translate (yet)."
MSGBOX_MSG_TRANSLATE_TO_MORSE_ERROR: str = "The program doesn't have permission to save files to the current location."
MSGBOX_MSG_TRANSLATE_TO_PLAIN_WARNING: str = "You may only use the characters: .-/ and spaces in your Morse code input."

# Audio Settings
AUDIO_TONE: int = 800
AUDIO_VOLUME: float = 1.0
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_WPM: int = 20  # Words per Minute
AUDIO_READY_MESSAGE: str = "READY:"

# Regex Patterns
PATT_SANITIZE_MORSE_CODE_INPUT = re.compile(r"""
    [.\-/ ]+   # Match one or more of the characters: dot, dash, slash, space
""", re.VERBOSE)

PATT_REDUCE_SPACES_MORSE_CODE_INPUT = re.compile(r"""
    \d{2,}   # Match two or more spaces
""", re.VERBOSE)


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
        msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=MSGBOX_MSG_TRANSLATE_TO_MORSE_ERROR)

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
        entry_audio_status.insert(0, f"{AUDIO_READY_MESSAGE} {most_recent_audio_filepath}")
        entry_audio_status.config(state="readonly")


def translate_to_morse_code() -> None:
    """Translate the text entered by the user into Morse code
    and display it in the GUI. The function also calls
    'create_audio_file' to generate the corresponding
    Morse code audio file.

    Returns:
        None
    """

    user_text: str = entry_plain_text_io.get()

    if user_text:
        # Eliminate diacritical letters by finding the closest ASCII
        # representations for all characters.
        normalized_user_text: str = unidecode.unidecode(user_text).upper()
        split_user_text: list = normalized_user_text.split()

        # Translate the normalized text to Morse code.
        # Each letter is looked up in the MORSE_CODE_DICT,
        # and words are separated by a slash with spaces.
        mcode: str = " / ".join(" ".join(map(lambda c: MORSE_CODE_DICT.get(c, ""), word)) for word in split_user_text)

        # Delete the previous text and insert the translation.
        entry_morse_code_io.delete(0, tk.END)
        entry_morse_code_io.insert(0, mcode)

        if audio_requested.get():
            create_audio_file(normalized_user_text)
        else:
            # Change the state of the relevant entry widget to allow
            # the modification of its text. Delete the previous text,
            # and change the state again to disallow further edits.
            entry_audio_status.config(state="normal")
            entry_audio_status.delete(0, tk.END)
            entry_audio_status.config(state="readonly")

            global most_recent_audio_filepath
            most_recent_audio_filepath = ""

    else:
        # Display a warning if the user has not provided any input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)


def translate_to_plaintext() -> None:
    """Translate the Morse code entered by the user into plain text,
    and display it in the GUI.

    Returns:
        None
    """

    user_morse_code_text: str = entry_morse_code_io.get().strip()
    if not user_morse_code_text:
        # Display a warning if the user has not provided any input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)

    elif not bool(re.fullmatch(pattern=PATT_SANITIZE_MORSE_CODE_INPUT, string=user_morse_code_text)):
        # Display a warning if the user has provided illegal chars.
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_TO_PLAIN_WARNING)

    else:

        # Replace each occurrence of two spaces or more with one space.
        user_morse_code_text_reduced: str = re.sub(pattern=PATT_REDUCE_SPACES_MORSE_CODE_INPUT, repl=" ",
                                                   string=user_morse_code_text)
        # Split the user's input into a list of words.
        split_user_morse_code_text: list = user_morse_code_text_reduced.split(" / ")

        # Create the dictionary with switched keys and values.
        reversed_morse_code_dict: dict = {v: k for k, v in MORSE_CODE_DICT.items()}

        # Look up each Morse code letter in that dict, and join each
        # word with the separator being a space.
        plain_text: str = " ".join("".join(map(lambda c: reversed_morse_code_dict.get(c, ""), word.split())) for word
                                   in split_user_morse_code_text)

        # Insert plain_text into the output widget.
        entry_plain_text_io.delete(0, tk.END)
        entry_plain_text_io.insert(0, plain_text)


def copy_to_clipboard(text_to_copy: str) -> None:
    """A utility function to copy the arg to the clipboard.

    Args:
        text_to_copy: str: String from an entry widget.

    Returns:
        None
    """

    if text_to_copy:
        # Copy the translation to the systen clipboard and display
        # a success message to the user.
        pyperclip.copy(text_to_copy)
        msgbox.showinfo(title=MSGBOX_TITLE_SUCCESS, message=MSGBOX_MSG_COPY_SUCCESS)

    else:
        # Display a warning if there is no input yet.
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_COPY_WARNING)


def copy_morse_translation() -> None:
    """Call the main copying function with the Morse translation as argument.

    Returns:
        None
    """

    copy_to_clipboard(entry_morse_code_io.get())


def copy_plain_text() -> None:
    """Call the main copying function with the plain text as argument.

    Returns:
        None
    """

    copy_to_clipboard(entry_plain_text_io.get())


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

# Labels for user i/o fields with custom font and color
label_plain_text_io = tk.Label(text=LABEL_PLAIN_TEXT_IO_TEXT, fg=STATIC_TEXT_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_plain_text_io.grid(column=0, row=2)

label_morse_code_io = tk.Label(text=LABEL_MORSE_CODE_IO_TEXT, fg=STATIC_TEXT_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_morse_code_io.grid(column=0, row=3)

label_audio_status = tk.Label(text=LABEL_AUDIO_STATUS_TEXT, fg=STATIC_TEXT_COLOR, bg=BG_COLOR, font=LABEL_FONT)
label_audio_status.grid(column=0, row=4)

# Entry widgets for plain text i/o, Morse code i/o, and audio status
entry_plain_text_io = tk.Entry(width=ENTRY_WIDTH)
entry_plain_text_io.focus()  # Automatically focus on the text entry field
entry_plain_text_io.grid(column=1, row=2)

entry_morse_code_io = tk.Entry(width=ENTRY_WIDTH)
entry_morse_code_io.grid(column=1, row=3)

entry_audio_status = tk.Entry(width=ENTRY_WIDTH)
entry_audio_status.config(state="readonly")  # Display audio file status, not editable by the user
entry_audio_status.grid(column=1, row=4)

# Buttons for translating text, copying text, and playing audio
button_translate_to_morse = tk.Button(text=BUTTON_TRANSLATE_TO_MORSE_TEXT, font=BUTTON_FONT, width=BUTTON_SMALL_WIDTH,
                                      command=translate_to_morse_code, bg=BG_COLOR, fg=STATIC_TEXT_COLOR,
                                      activebackground=BG_COLOR, activeforeground=STATIC_TEXT_COLOR)
button_translate_to_morse.grid(column=2, row=2, padx=BUTTON_X_PADD)

button_copy_plain = tk.Button(text=BUTTON_COPY_TEXT, font=BUTTON_FONT, width=BUTTON_SMALL_WIDTH,
                              command=copy_plain_text, bg=BG_COLOR, fg=STATIC_TEXT_COLOR, activebackground=BG_COLOR,
                              activeforeground=STATIC_TEXT_COLOR)
button_copy_plain.grid(column=3, row=2)

button_translate_to_plain = tk.Button(text=BUTTON_TRANSLATE_TO_PLAIN_TEXT, font=BUTTON_FONT, width=BUTTON_SMALL_WIDTH,
                                      command=translate_to_plaintext, bg=BG_COLOR, fg=STATIC_TEXT_COLOR,
                                      activebackground=BG_COLOR, activeforeground=STATIC_TEXT_COLOR)
button_translate_to_plain.grid(column=2, row=3, padx=BUTTON_X_PADD)

button_copy_morse = tk.Button(text=BUTTON_COPY_TEXT, font=BUTTON_FONT, width=BUTTON_SMALL_WIDTH,
                              command=copy_morse_translation, bg=BG_COLOR, fg=STATIC_TEXT_COLOR,
                              activebackground=BG_COLOR, activeforeground=STATIC_TEXT_COLOR)
button_copy_morse.grid(column=3, row=3)

button_play_audio = tk.Button(text=BUTTON_PLAY_TEXT, font=BUTTON_FONT, width=BUTTON_LARGE_WIDTH,
                              command=play_audio_file, bg=BG_COLOR, fg=STATIC_TEXT_COLOR, activebackground=BG_COLOR,
                              activeforeground=STATIC_TEXT_COLOR)
button_play_audio.grid(column=2, row=4, padx=BUTTON_X_PADD, columnspan=2)

# Checkbox for deciding whether to produce an audio file
checkbox_audio_request = tk.Checkbutton(text=CHECKBOX_TEXT, variable=audio_requested, onvalue=VAL_ON_CHECKBOX,
                                        offvalue=VAL_OFF_CHECKBOX, bg=BG_COLOR, highlightthickness=0,
                                        font=CHECKBOX_FONT, fg=STATIC_TEXT_COLOR, activebackground=BG_COLOR,
                                        activeforeground=STATIC_TEXT_COLOR, selectcolor=BG_COLOR)
checkbox_audio_request.grid(column=1, row=1)

# Start the main event loop of the application
root.mainloop()
