"""
This module contains all the functions used by the application.

It defines: play_audio_file, create_audio_file,
translate_to_morse_code, translate_to_plain_text & copy_to_clipboard.
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
    """Play back the most-recently-generated Morse code audio file.

    Args:
        audio_status: str: Text from the widget entry_audio_status.

    Raises:
        PlaysoundException: If the audio file can't be played back.

    Returns:
        None
    """

    # Check whether the audio_status is non-empty
    if audio_status:
        try:
            playsound(sound=most_recent_audio_filepath)

        except PlaysoundException as e:
            # Display an error if the audio file can't be played
            msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=str(e))

    else:
        # Display a warning if no audio file has been created yet
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_PLAY_WARNING)


def change_entry_text(entry_to_change: tk.Entry, change_to: str = "") -> None:
    """Change a displayed entry widget text.

    Args:
        entry_to_change: tk.Entry: Entry widget to change.
        change_to: str: New value to display; defaults to an empty str.

    Returns:
        None
    """

    # Get the widget's current state ("readonly"/"normal")
    entry_widget_original_state = entry_to_change.cget("state")

    # Change the widget's state to allow modification if necessary
    if entry_widget_original_state == "readonly":
        entry_to_change.config(state="normal")

    # Delete all text from the widget
    entry_to_change.delete(first=0, last=tk.END)

    # Insert a new text (if provided) to the widget
    if change_to:
        entry_to_change.insert(index=0, string=change_to)

    # Restore the original state of the widget if necessary
    if entry_widget_original_state == "readonly":
        entry_to_change.config(state="readonly")


def create_audio_file(normalized_text: str, audio_status: tk.Entry) -> None:
    """Generate the Morse code audio file from a normalized text.

    Args:
        normalized_text (str): Text to be converted into audio.
        audio_status: tk.Entry: Audio status entry widget.

    Raises:
        PermissionError: If the audio file can't be created.

    Returns:
        None
    """

    # Check whether the normalized_text contains any chars unsupported
    # by the pycw module.
    if bool(re.search(pattern=PATT_SANITIZE_PLAIN_TEXT_INPUT, string=normalized_text)):

        # If so, ask the user whether to automatically remove them
        # from the text, or whether to abandon audio generation.
        if msgbox.askyesno(title=MSGBOX_TITLE_CONFIRM, message=MSGBOX_MSG_TRANSLATE_TO_MORSE_CONFIRM):
            normalized_text = re.sub(pattern=PATT_SANITIZE_PLAIN_TEXT_INPUT, repl="", string=normalized_text)

        else:
            global most_recent_audio_filepath
            most_recent_audio_filepath = ""
            change_entry_text(entry_to_change=audio_status)
            return None

    # Incrementally, find the first unused audio filename to avoid
    # overwriting previous ones.
    counter: int = 0
    audio_filepath: str = f"{DEFAULT_AUDIO_OUTPUT_DIR}/{DEFAULT_AUDIO_OUTPUT_FILE}"
    audio_file_name, audio_file_ext = splitext(p=audio_filepath)

    # Create the directory if it doesn't exist yet
    makedirs(name=DEFAULT_AUDIO_OUTPUT_DIR, exist_ok=True)

    while exists(audio_filepath):
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
        # due to lack of permission.
        msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=MSGBOX_MSG_TRANSLATE_TO_MORSE_ERROR)

    else:
        # Save the audio filepath as the most recent one
        most_recent_audio_filepath = audio_filepath
        change_entry_text(entry_to_change=audio_status, change_to=f"{AUDIO_READY_MESSAGE} {most_recent_audio_filepath}")


def translate_to_morse_code(user_plain_text: str, audio_request: bool, audio_status: tk.Entry,
                            output_entry: tk.Entry) -> None:
    """Translate the text entered by the user into Morse code
    and display it in the GUI. The function also calls
    'create_audio_file' to generate the corresponding
    Morse code audio file if the user wants it.

    Args:
        user_plain_text: str: Text from the plain text i/o entry.
        audio_request: bool: Whether to generate the audio.
        audio_status: tk.Entry: Audio status entry widget.
        output_entry: tk.Entry: Output entry widget.

    Returns:
        None
    """

    if user_plain_text:
        # Eliminate diacritical letters by finding the closest ASCII
        # representations for all characters.
        normalized_text: str = unidecode.unidecode(string=user_plain_text).upper().strip()
        split_user_text: list = normalized_text.split()

        # Translate the normalized text to Morse code.
        # Each letter is looked up in the MORSE_CODE_DICT,
        # and words are separated by a slash with spaces.
        mcode: str = " / ".join(" ".join(map(lambda c: MORSE_CODE_DICT.get(c, ""), word)) for word in split_user_text)
        mcode = mcode.strip()

        if mcode:
            # Change the output_entry text to mcode value if mcode
            # is not an empty str.
            change_entry_text(entry_to_change=output_entry, change_to=mcode)

            if audio_request:
                create_audio_file(normalized_text=normalized_text, audio_status=audio_status)

        else:
            # If mcode is an empty string, erase
            # any text in the most_recent_audio_filepath
            # and in audio_status, then display a warning
            # about the meaningless sequence in the input.
            global most_recent_audio_filepath
            most_recent_audio_filepath = ""
            change_entry_text(entry_to_change=audio_status)
            msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_MEANINGLESS_TO_MORSE_WARNING)

    else:
        # Display a warning if the user has not provided any input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_TRANSLATE_WARNING)


def translate_to_plain_text(user_morse_code_text: str, audio_request: bool,
                            audio_status: tk.Entry, output_entry: tk.Entry) -> None:
    """Translate the Morse code entered by the user into plain text,
    and display it in the GUI.

    Args:
        user_morse_code_text: str: Text from the Morse code i/o entry.
        audio_request: bool: Whether to generate the audio.
        audio_status: tk.Entry: Audio status entry widget.
        output_entry: tk.Entry: Output entry widget.

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
                                   in split_user_morse_code_text).strip()

        if plain_text:
            # Change the output_entry text to plain_text value
            # if it's not an empty str.
            change_entry_text(entry_to_change=output_entry, change_to=plain_text)
            if audio_request:
                create_audio_file(normalized_text=plain_text, audio_status=audio_status)

        else:
            # If output_entry is an empty string, erase
            # any text in the most_recent_audio_filepath
            # and in audio_status, then display a warning
            # about the meaningless sequence in the input.
            global most_recent_audio_filepath
            most_recent_audio_filepath = ""
            change_entry_text(entry_to_change=audio_status)
            msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_MEANINGLESS_TO_PLAIN_WARNING)


def copy_to_clipboard(text_to_copy: str) -> None:
    """A utility function to copy the arg to the clipboard.

    Args:
        text_to_copy: str: String from an entry widget.

    Returns:
        None
    """

    if text_to_copy:
        # Copy the text to the system clipboard and display
        # a success message to the user.
        pyperclip.copy(text=text_to_copy)
        msgbox.showinfo(title=MSGBOX_TITLE_SUCCESS, message=MSGBOX_MSG_COPY_SUCCESS)

    else:
        # Display a warning if there is no input
        msgbox.showwarning(title=MSGBOX_TITLE_WARNING, message=MSGBOX_MSG_COPY_WARNING)
