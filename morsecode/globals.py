"""
This module contains all the global constants used by the application.

It declares the app title, Morse code lookup dictionary, GUI style,
output audio settings, tkinter.messagebox messages and regex patterns.
"""

import re

APP_TITLE: str = "Morse Code Translator & Audio Generator v1.0.0"
MORSE_CODE_DICT: dict = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
                         "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
                         "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
                         "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----",
                         "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
                         "8": "---..", "9": "----.", ".": ".-.-.-", ",": "--..--", "'": ".----.", "\"": ".-..-.",
                         "_": "..--.-", ":": "---...", ";": "-.-.-.", "?": "..--..", "!": "-.-.--", "-": "-....-",
                         "+": ".-.-.", "/": "-..-.", "(": "-.--.", ")": "-.--.-", "=": "-...-", "@": ".--.-.",
                         "$": "...-..-", "&": ".-..."}

# ~ Colors ~
ROOT_BG_COLOR: str = "#FFF"  # White
READONLY_ENTRY_BG_COLOR: str = "#C7C7C7"  # Very Light Gray

BUTTON_PRIMARY_BG_COLOR: str = "#003366"  # Prussian Blue
BUTTON_PRIMARY_PRESSED_BG_COLOR: str = "#0A2B55"  # Prussian Blue shade

BUTTON_SECOND_BG_COLOR: str = "#3a507e"  # Prussian Blue tint
BUTTON_SECOND_PRESSED_BG_COLOR: str = "#003366"  # Prussian Blue

STATIC_TEXT_COLOR: str = "#003366"  # Prussian Blue
BUTTON_TEXT_COLOR: str = "#FFF"  # White

# ~ Images, Filepaths, Dimensions & Padding ~
LOGO_FILEPATH: str = "images/app_logo.png"
DEFAULT_AUDIO_OUTPUT_DIR: str = "output"
DEFAULT_AUDIO_OUTPUT_FILE: str = "morse_code_audio.wav"

IMG_WIDTH: int = 400
IMG_HEIGHT: int = 300

ROOT_PAD_X: int = 60
ROOT_PAD_Y: int = 10

# ~ Buttons ~
BUTTON_PAD_X: tuple[int, int] = (5, 0)

BUTTON_WIDTH: int = 15
BUTTON_BORDER_WIDTH: float = 1.0

BUTTON_TRANSLATE_TO_MORSE_TEXT: str = "To Morse"
BUTTON_TRANSLATE_TO_PLAIN_TEXT: str = "To Plain Text"
BUTTON_COPY_TEXT: str = "Copy"
BUTTON_PLAY_TEXT: str = "Play Audio"
BUTTON_CLEAR_TEXT: str = "Clear All"

# ~ Labels ~
LABEL_PLAIN_TEXT_IO_TEXT: str = "Plain Text:"
LABEL_MORSE_CODE_IO_TEXT: str = "Morse Code:"
LABEL_AUDIO_STATUS_TEXT: str = "Audio Status:"

LABEL_INFO_PAD_X: tuple[int, int] = (50, 10)
LABEL_INFO_TEXT: str = "Developed by Dominik Otrębski\n" \
                       "For updates and feedback, visit github.com/Dotrebski/MorseCode\n" \
                       "Licensed under the BSD-3-Clause License. See LICENSE for details.\n" \
                       "© 2024 Dominik Otrębski. All rights reserved."

# ~ Checkbox ~
CHECKBOX_TEXT: str = "Create Audio"
CHECKBOX_VAL_ON: bool = True
CHECKBOX_VAL_OFF: bool = False

# ~ Entries ~
ENTRY_WIDTH: int = 30
ENTRY_AUDIO_STATUS_WIDTH: int = 52

# ~ Fonts ~
FONT_LABEL: tuple[str, int, str] = ("Arial", 11, "normal")
FONT_CHECKBOX: tuple[str, int, str] = ("Arial", 11, "normal")
FONT_BUTTON: tuple[str, int, str] = ("Arial", 10, "normal")
FONT_INFO: tuple[str, int, str] = ("Arial", 10, "normal")

# ~ MessageBox ~
# ~~ Titles ~~
MESSAGEBOX_TITLE_SUCCESS: str = "Success"
MESSAGEBOX_TITLE_CONFIRM: str = "Confirmation"
MESSAGEBOX_TITLE_WARNING: str = "Warning"
MESSAGEBOX_TITLE_ERROR: str = "Error"

# ~~ Messages ~~
# ~~~ Successes ~~~
MESSAGEBOX_MSG_COPY_SUCCESS: str = "The text has been successfully copied to your clipboard."

# ~~~ Confirmations ~~~
MESSAGEBOX_MSG_AUTO_CLEANUP_CONFIRM: str = "Your input contains characters that are unsupported for audio" \
                                             " generation (~`<>\\|*^%@#). Would you like to proceed and have them" \
                                             " removed automatically?"

# ~~~ Warnings ~~~
MESSAGEBOX_MSG_COPY_WARNING: str = "There is nothing to copy (yet)."
MESSAGEBOX_MSG_PLAY_WARNING: str = "There is nothing to play (yet)."
MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING: str = "There is nothing to translate (yet)."
MESSAGEBOX_MSG_TRANSLATE_TO_PLAIN_WARNING: str = "You may only use the characters: .-/ and spaces" \
                                                 " in your Morse code input."
MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING: str = "The input contains a sequence of valid symbols, but they do not" \
                                               " correspond to any Morse code symbol."

# ~~~ Errors ~~~
# UI
MESSAGEBOX_MSG_LOGO_ERROR: str = f"The logo ({LOGO_FILEPATH}) couldn't be loaded."

# The change_entry_text function
MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_FIRST_ARG_ERROR: str = "The first argument (entry_to_change) to change_entry_text()" \
                                                         " must be an instance of tkinter.Entry."
MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_SECOND_ARG_ERROR: str = "The second argument (change_to) to change_entry_text()" \
                                                         " must be of type str."
# The change_most_recent_filepath function
MESSAGEBOX_MSG_CHANGE_FILEPATH_WRONG_ARG_ERROR: str = "The argument (audio_status) to change_most_recent_filepath()" \
                                                      " must be of type str. It is an empty string by default."

# The copy_to_clipboard function
MESSAGEBOX_MSG_CLIPBOARD_WRONG_ARG_ERROR: str = "The argument (text_to_copy) to copy_to_clipboard() must" \
                                                " be of type str."

# The clear_all function
MESSAGEBOX_MSG_CLEAR_ALL_LACK_ARG_ERROR: str = "At least one argument must be passed to clear_all()."
MESSAGEBOX_MSG_CLEAR_ALL_WRONG_ARG_ERROR: str = "Arguments to clear_all() must all be instances of tkinter.Entry."

# The play_audio_file function
MESSAGEBOX_MSG_PLAY_WRONG_ARG_ERROR: str = "The argument (audio_status) to play_audio_file() must be of type str."

# The create_audio_file function
MESSAGEBOX_MSG_CREATE_AUDIO_FIRST_ARG_WRONG_ERROR: str = "The first argument (normalized_text) to create_audio_file()" \
                                          " must be of type str."
MESSAGEBOX_MSG_CREATE_AUDIO_SECOND_ARG_WRONG_ERROR: str = "The second argument (audio_status) to create_audio_files()" \
                                          " must an instance of tkinter.Entry."

# The translate_to_morse_code function
MESSAGEBOX_MSG_TO_MORSE_FIRST_ARG_WRONG_ERROR: str = "The first argument (user_plain_text)" \
                                          " to translate_to_morse_code() must be of type str."
MESSAGEBOX_MSG_TO_MORSE_SECOND_ARG_WRONG_ERROR: str = "The second argument (audio_request)" \
                                          " to translate_to_morse_code() must be of type bool."
MESSAGEBOX_MSG_TO_MORSE_THIRD_ARG_WRONG_ERROR: str = "The third argument (audio_status)" \
                                          " to translate_to_morse_code() must be an instance of tkinter.Entry."
MESSAGEBOX_MSG_TO_MORSE_FOURTH_ARG_WRONG_ERROR: str = "The fourth argument (output_entry)" \
                                          " to translate_to_morse_code() must be an instance of tkinter.Entry."
MESSAGEBOX_MSG_TO_MORSE_PERM_ERROR: str = f"The application doesn't have permission to save files to the current" \
                                           f" location ({DEFAULT_AUDIO_OUTPUT_DIR})."

# The translate_to_plain_text function
MESSAGEBOX_MSG_TO_PLAIN_FIRST_ARG_WRONG_ERROR: str = "The first argument (user_morse_code_text)" \
                                          " to translate_to_plain_text() must be of type str."

MESSAGEBOX_MSG_TO_PLAIN_SECOND_ARG_WRONG_ERROR: str = "The second argument (audio_request)" \
                                          " to translate_to_plain_text() must be of type bool."

MESSAGEBOX_MSG_TO_PLAIN_THIRD_ARG_WRONG_ERROR: str = "The third argument (audio_status)" \
                                          " to translate_to_plain_text() must be an instance of tkinter.Entry."

MESSAGEBOX_MSG_TO_PLAIN_FOURTH_ARG_WRONG_ERROR: str = "The fourth argument (output_entry)" \
                                          " to translate_to_plain_text() must be an instance of tkinter.Entry."

# ~ Audio Settings ~
AUDIO_TONE: int = 800
AUDIO_VOLUME: float = 1.0
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_WPM: int = 20  # Words per Minute
AUDIO_READY_MESSAGE: str = "READY:"

# ~ Regex Patterns ~
PATT_SANITIZE_MORSE_CODE_INPUT = re.compile(r"""
    [.\-/ ]+   # Match one or more of these characters (only they can be translated from Morse code to plain text)
""", re.VERBOSE)

PATT_SANITIZE_PLAIN_TEXT_INPUT = re.compile(r"""
    [~`<>\\|*^%@#]+    # Match any of these characters (they are unsupported by the pycw module)
""", re.VERBOSE)

PATT_REDUCE_SPACES_MORSE_CODE_INPUT = re.compile(r"""
    \s{2,}   # Match at least two white-space characters
""", re.VERBOSE)
