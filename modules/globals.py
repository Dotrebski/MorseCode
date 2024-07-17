"""
This module contains all the global constants used by the
Morse Code Translator application.

It declares the app title, Morse code lookup dictionary, Tkinter style,
output audio settings and regex patterns.
"""

import re

APP_TITLE: str = "Morse Code Translator and Audio Generator 0.4.0"
MORSE_CODE_DICT: dict = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
                         "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
                         "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
                         "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----",
                         "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
                         "8": "---..", "9": "----.", ".": ".-.-.-", ",": "--..--", "'": ".----.", "\"": ".-..-.",
                         "_": "..--.-", ":": "---...", ";": "-.-.-.", "?": "..--..", "!": "-.-.--", "-": "-....-",
                         "+": ".-.-.", "/": "-..-.", "(": "-.--.", ")": "-.--.-", "=": "-...-", "@": ".--.-.",
                         "$": "...-..-", "&": ".-..."}

# Colors
BG_COLOR: str = "#454679"  # Soft Indigo
STATIC_TEXT_COLOR: str = "#FFC900"  # Tangerine Yellow

# Images' filepaths, dimensions and padding
LOGO_FILEPATH: str = "images/app_logo.png"
DEFAULT_AUDIO_OUTPUT_DIR: str = "output"
DEFAULT_AUDIO_OUTPUT_FILE: str = "morse_code_audio.wav"

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
LABEL_FONT: tuple[str, int, str] = ("Arial", 12, "bold")
CHECKBOX_FONT: tuple[str, int, str] = ("Arial", 11, "bold")
BUTTON_FONT: tuple[str, int, str] = ("Arial", 10, "bold")

# MessageBox
MSGBOX_TITLE_SUCCESS: str = "Success"
MSGBOX_TITLE_WARNING: str = "Warning"
MSGBOX_TITLE_ERROR: str = "Error"

MSGBOX_MSG_LOGO_ERROR: str = "The logo couldn't be loaded."
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
    \s{2,}   # Match two or more spaces
""", re.VERBOSE)
