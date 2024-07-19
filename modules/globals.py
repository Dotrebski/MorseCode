"""
This module contains all the global constants used by the application.

It declares the app title, Morse code lookup dictionary, GUI style,
output audio settings and regex patterns.
"""

import re

APP_TITLE: str = "Morse Code Translator & Audio Generator v0.8.0"
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
BG_COLOR: str = "#FFF"  # White
READONLY_ENTRY_BG_COLOR: str = "#C7C7C7"  # Very Light Gray
BUTTON_BG_COLOR: str = "#003366"  # Prussian Blue
BUTTON_PRESSED_BG_COLOR: str = "#0A2B55"  # Prussian Blue Shade

STATIC_TEXT_COLOR: str = "#003366"  # Prussian Blue
BUTTON_TEXT_COLOR: str = "#FFF"  # White

# Images, Filepaths, Dimensions and Padding
LOGO_FILEPATH: str = "images/app_logo.png"
DEFAULT_AUDIO_OUTPUT_DIR: str = "output"
DEFAULT_AUDIO_OUTPUT_FILE: str = "morse_code_audio.wav"

IMG_WIDTH: int = 400
IMG_HEIGHT: int = 300

PADD_X: int = 60
PADD_Y: int = 60

# Buttons
BUTTON_X_PADD: tuple[int, int] = (5, 0)

BUTTON_WIDTH: int = 15
BUTTON_BORDER_WIDTH: float = 1.0

BUTTON_TRANSLATE_TO_MORSE_TEXT: str = "To Morse"
BUTTON_TRANSLATE_TO_PLAIN_TEXT: str = "To Plain Text"
BUTTON_COPY_TEXT: str = "Copy"
BUTTON_PLAY_TEXT: str = "Play Audio"
BUTTON_CLEAR_TEXT: str = "Clear All"

# Labels
LABEL_PLAIN_TEXT_IO_TEXT: str = "Plain Text:"
LABEL_MORSE_CODE_IO_TEXT: str = "Morse Code:"
LABEL_AUDIO_STATUS_TEXT: str = "Audio Status:"

# Checkbox
CHECKBOX_TEXT: str = "Create Audio"
CHECKBOX_VAL_ON: bool = True
CHECKBOX_VAL_OFF: bool = False

# Entries
ENTRY_WIDTH: int = 30
ENTRY_AUDIO_STATUS_WIDTH: int = 52

# Fonts
FONT_LABEL: tuple[str, int, str] = ("Arial", 11, "normal")
FONT_CHECKBOX: tuple[str, int, str] = ("Arial", 11, "normal")
FONT_BUTTON: tuple[str, int, str] = ("Arial", 10, "normal")

# MessageBox
MSGBOX_TITLE_SUCCESS: str = "Success"
MSGBOX_TITLE_CONFIRM: str = "Confirmation"
MSGBOX_TITLE_WARNING: str = "Warning"
MSGBOX_TITLE_ERROR: str = "Error"

MSGBOX_MSG_LOGO_ERROR: str = "The logo couldn't be loaded."

MSGBOX_MSG_COPY_SUCCESS: str = "The text has been successfully copied to your clipboard."
MSGBOX_MSG_COPY_WARNING: str = "There is nothing to copy (yet)."

MSGBOX_MSG_PLAY_WARNING: str = "There is nothing to play (yet)."
MSGBOX_MSG_PLAY_FILE_NF_ERROR: str = "The file that has just been created doesn't seem to exist anymore."

MSGBOX_MSG_TRANSLATE_WARNING: str = "There is nothing to translate (yet)."
MSGBOX_MSG_TRANSLATE_TO_MORSE_ERROR: str = "The application doesn't have permission to save files to the current " \
                                           "location."
MSGBOX_MSG_TRANSLATE_TO_PLAIN_WARNING: str = "You may only use the characters: .-/ and spaces in your Morse code input."

MSGBOX_MSG_MEANINGLESS_TO_MORSE_WARNING: str = "The input contains characters that cannot be translated into Morse" \
                                               " code. Please, use only letters, numbers, and punctuation marks."
MSGBOX_MSG_MEANINGLESS_TO_PLAIN_WARNING: str = "The input contains a sequence of valid symbols that do not correspond" \
                                               " to any Morse code symbol. Please, use only dots, dashes," \
                                               "forward slashes, and spaces."

MSGBOX_MSG_TRANSLATE_TO_MORSE_CONFIRM: str = "Your input contains characters that are unsupported for audio" \
                                             " generation (~`<>\\|*^%@#). Would you like to proceed and have them" \
                                             " removed automatically?"

# Audio Settings
AUDIO_TONE: int = 800
AUDIO_VOLUME: float = 1.0
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_WPM: int = 20  # Words per Minute
AUDIO_READY_MESSAGE: str = "READY:"

# Regex Patterns
PATT_SANITIZE_MORSE_CODE_INPUT = re.compile(r"""
    [.\-/ ]+   # Match one or more of these characters (only they can be translated from Morse code to plain text)
""", re.VERBOSE)

PATT_SANITIZE_PLAIN_TEXT_INPUT = re.compile(r"""
    [~`<>\\|*^%@#]+    # Match any of these characters (they are unsupported by the pycw module)
""", re.VERBOSE)

PATT_REDUCE_SPACES_MORSE_CODE_INPUT = re.compile(r"""
    \s{2,}   # Match two or more spaces
""", re.VERBOSE)
