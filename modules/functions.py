"""
This module contains all the functions used by the
Morse Code Translator application.

It defines: play_audio_file, create_audio_file,
translate_to_morse_code,translate_to_plain_text, and copy_to_clipboard.
"""

import tkinter as tk
from tkinter import messagebox as msgbox
from os.path import splitext, exists
from os import makedirs
from playsound3 import playsound
from playsound3.playsound3 import PlaysoundException
import unidecode
import pyperclip
import pycw
from modules.globals import *

most_recent_audio_filepath: str = ""


def play_audio_file(audio_status: str) -> None:
    """Play the most-recently-generated Morse code audio file.

    Args:
        audio_status: str: Text from the widget entry_audio_status

    Raises:
        PlaysoundException: If the audio file can't be played

    Returns:
        None
    """

    if audio_status:
        try:
            playsound(sound=most_recent_audio_filepath)

        except PlaysoundException as e:
            # Display an error if the audio file can't be played
            msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=str(e))

    else:
        # Display a warning if no audio file has been created yet
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_PLAY_WARNING)


def create_audio_file(normalized_text: str, audio_status: tk.Entry) -> None:
    """Generate a Morse code audio file from a normalized text.

    Args:
        normalized_text (str): Text to be converted into audio
        audio_status: tk.Entry: Audio status entry widget

    Raises:
        PermissionError: If the audio file can't be created

    Returns:
        None
    """

    # Incrementally, find the first unused audio filename to avoid
    # overwriting previous ones.
    counter: int = 0
    audio_filepath: str = f"{DEFAULT_AUDIO_OUTPUT_DIR}/{DEFAULT_AUDIO_OUTPUT_FILE}"
    audio_file_name, audio_file_ext = splitext(p=audio_filepath)

    # Create the directory if it doesn't exist yet
    makedirs(name=DEFAULT_AUDIO_OUTPUT_DIR, exist_ok=True)

    while exists(path=audio_filepath):
        counter += 1
        audio_filepath = f"{audio_file_name}_{counter}{audio_file_ext}"

    # Generate the audio file according to the specified settings
    try:
        pycw.output_wave(file=audio_filepath,
                         text=normalized_text,
                         tone=AUDIO_TONE,
                         volume=AUDIO_VOLUME,
                         sample_rate=AUDIO_SAMPLE_RATE,
                         wpm=AUDIO_WPM)

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
        audio_status.config(state="normal")
        audio_status.delete(first=0, last=tk.END)
        audio_status.insert(index=0, string=f"{AUDIO_READY_MESSAGE} {most_recent_audio_filepath}")
        audio_status.config(state="readonly")


def translate_to_morse_code(user_plain_text: str, output_entry: tk.Entry, audio_request: bool,
                            audio_status: tk.Entry) -> None:
    """Translate the text entered by the user into Morse code
    and display it in the GUI. The function also calls
    'create_audio_file' to generate the corresponding
    Morse code audio file if the user wants it.

    Args:
        user_plain_text: str: Text from the plain text i/o entry
        output_entry: tk.Entry: Output entry widget
        audio_request: bool: Whether to generate the audio
        audio_status: tk.Entry: Audio status entry widget

    Returns:
        None
    """

    if user_plain_text:
        # Eliminate diacritical letters by finding the closest ASCII
        # representations for all characters. Make a list of words.
        normalized_text: str = unidecode.unidecode(string=user_plain_text).upper()
        split_user_text: list = normalized_text.split()

        # Translate the normalized text to Morse code.
        # Each letter is looked up in the MORSE_CODE_DICT,
        # and words are separated by a slash with spaces.
        mcode: str = " / ".join(" ".join(map(lambda c: MORSE_CODE_DICT.get(c, ""), word)) for word in split_user_text)

        # Delete the previous text and insert the translation
        output_entry.delete(first=0, last=tk.END)
        output_entry.insert(index=0, string=mcode)

        if audio_request:
            create_audio_file(normalized_text=normalized_text, audio_status=audio_status)
        else:
            # Change the state of the relevant entry widget to allow
            # the modification of its text. Delete the previous text,
            # and change the state again to disallow further edits.
            audio_status.config(state="normal")
            audio_status.delete(0, tk.END)
            audio_status.config(state="readonly")

            global most_recent_audio_filepath
            most_recent_audio_filepath = ""

    else:
        # Display a warning if the user has not provided any input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)


def translate_to_plain_text(user_morse_code_text: str, output_entry: tk.Entry, audio_status: tk.Entry) -> None:
    """Translate the Morse code entered by the user into plain text,
    and display it in the GUI.

    Args:
        user_morse_code_text: str: Text from the Morse code i/o entry
        output_entry: tk.Entry: Output entry widget
        audio_status: tk.Entry: Audio status entry widget

    Returns:
        None
    """

    if not user_morse_code_text:
        # Display a warning if the user has not provided any input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)

    elif not bool(re.fullmatch(pattern=PATT_SANITIZE_MORSE_CODE_INPUT, string=user_morse_code_text)):
        # Display a warning if the user has provided illegal chars
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_TO_PLAIN_WARNING)

    else:

        # Replace each occurrence of two spaces or more with one space
        user_morse_code_text_reduced: str = re.sub(pattern=PATT_REDUCE_SPACES_MORSE_CODE_INPUT, repl=" ",
                                                   string=user_morse_code_text)
        # Split the user's input into a list of words
        split_user_morse_code_text: list = user_morse_code_text_reduced.split(sep=" / ")

        # Create the dictionary with switched keys and values
        switched_morse_code_dict: dict = {v: k for k, v in MORSE_CODE_DICT.items()}

        # Look up each Morse code letter in that dict, and join each
        # word with the separator being a space.
        plain_text: str = " ".join("".join(map(lambda c: switched_morse_code_dict.get(c, ""), word.split())) for word
                                   in split_user_morse_code_text)

        # Insert plain_text into the output widget
        output_entry.delete(first=0, last=tk.END)
        output_entry.insert(index=0, string=plain_text)

        # Clear the audio status
        audio_status.config(state="normal")
        audio_status.delete(first=0, last=tk.END)
        audio_status.config(state="readonly")


def copy_to_clipboard(text_to_copy: str) -> None:
    """A utility function to copy the arg to the clipboard.

    Args:
        text_to_copy: str: String from an entry widget

    Returns:
        None
    """

    if text_to_copy:
        # Copy the translation to the systen clipboard and display
        # a success message to the user.
        pyperclip.copy(text=text_to_copy)
        msgbox.showinfo(title=MSGBOX_TITLE_SUCCESS, message=MSGBOX_MSG_COPY_SUCCESS)

    else:
        # Display a warning if there is no input yet
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_COPY_WARNING)
