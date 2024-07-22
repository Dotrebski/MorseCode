"""
This module contains all the functions used by the application.
"""

import re
import os
import tkinter as tk
from tkinter import messagebox
import playsound3
import unidecode
import pyperclip
import pycw
import globals

# Filepath to the most-recently-generated audio file
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

    if not isinstance(audio_status, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR, message=globals.MESSAGEBOX_MSG_PLAY_WRONG_ARG_ERROR)
        return

    # Check whether the audio_status is non-empty
    if audio_status:
        try:
            playsound3.playsound(sound=most_recent_audio_filepath)

        except playsound3.playsound3.PlaysoundException as e:
            # Display an error if the audio file can't be played
            messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR, message=str(e))

    else:
        # Display a warning if no audio file has been created yet
        messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING, message=globals.MESSAGEBOX_MSG_PLAY_WARNING)


def change_entry_text(entry_to_change: tk.Entry, change_to: str = "") -> None:
    """Change a displayed entry widget text.

    Args:
        entry_to_change: tk.Entry: Entry widget to change.
        change_to: str: New value to display; defaults to an empty str.

    Returns:
        None
    """

    if not isinstance(entry_to_change, tk.Entry):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_FIRST_ARG_ERROR)
        return

    if not isinstance(change_to, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_SECOND_ARG_ERROR)
        return

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


def change_most_recent_filepath(change_to: str = "") -> None:
    """A utility function to modify the most_recent_filepath
    global variable.

    Args:
        change_to: str: The value to assign to the global variable;
        defaults to an empty string.

    Returns:
        None
    """

    if not isinstance(change_to, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CHANGE_FILEPATH_WRONG_ARG_ERROR)
    else:
        global most_recent_audio_filepath
        most_recent_audio_filepath = change_to


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

    if not isinstance(normalized_text, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CREATE_AUDIO_FIRST_ARG_WRONG_ERROR)
        return

    if not isinstance(audio_status, tk.Entry):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CREATE_AUDIO_SECOND_ARG_WRONG_ERROR)
        return

    # Check whether the normalized_text contains any chars unsupported
    # by the pycw module.
    if re.search(pattern=globals.PATT_SANITIZE_PLAIN_TEXT_INPUT, string=normalized_text):

        # If so, ask the user whether to automatically remove them
        # from the text, or whether to abandon audio generation.
        if messagebox.askyesno(title=globals.MESSAGEBOX_TITLE_CONFIRM,
                               message=globals.MESSAGEBOX_MSG_AUTO_CLEANUP_CONFIRM):
            normalized_text = re.sub(pattern=globals.PATT_SANITIZE_PLAIN_TEXT_INPUT, repl="", string=normalized_text)

        else:
            change_most_recent_filepath()
            change_entry_text(entry_to_change=audio_status)
            return

    # Incrementally, find the first unused audio filename to avoid
    # overwriting previous ones.
    counter: int = 0
    audio_filepath: str = f"{globals.DEFAULT_AUDIO_OUTPUT_DIR}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
    audio_file_name, audio_file_ext = os.path.splitext(p=audio_filepath)

    # Create the directory if it doesn't exist yet
    # Generate the audio file according to the specified settings
    try:
        os.makedirs(name=globals.DEFAULT_AUDIO_OUTPUT_DIR, exist_ok=True)

        while os.path.exists(audio_filepath):
            counter += 1
            audio_filepath = f"{audio_file_name}_{counter}{audio_file_ext}"

        pycw.output_wave(file=audio_filepath,
                         text=normalized_text,
                         tone=globals.AUDIO_TONE,
                         volume=globals.AUDIO_VOLUME,
                         sample_rate=globals.AUDIO_SAMPLE_RATE,
                         wpm=globals.AUDIO_WPM)
    except PermissionError:
        # Display an error if the audio file can't be created
        # due to lack of permission.
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_MORSE_PERM_ERROR)

    else:
        # Save the audio filepath as the most recent one
        change_most_recent_filepath(change_to=audio_filepath)
        change_entry_text(entry_to_change=audio_status,
                          change_to=f"{globals.AUDIO_READY_MESSAGE} {most_recent_audio_filepath}")


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

    if not isinstance(user_plain_text, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_MORSE_FIRST_ARG_WRONG_ERROR)
        return

    if not isinstance(audio_request, bool):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_MORSE_SECOND_ARG_WRONG_ERROR)
        return

    if not isinstance(audio_status, tk.Entry):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_MORSE_THIRD_ARG_WRONG_ERROR)
        return

    if not isinstance(output_entry, tk.Entry):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_MORSE_FOURTH_ARG_WRONG_ERROR)
        return

    if user_plain_text:
        # Eliminate diacritical letters by finding the closest ASCII
        # representations for all characters.
        normalized_text: str = unidecode.unidecode(string=user_plain_text).upper().strip()
        split_user_text: list = normalized_text.split()

        # Remove all illegal characters from normalized_text
        sanitized_text: str = re.sub(pattern=globals.PATT_SANITIZE_PLAIN_TEXT_INPUT, repl="", string=normalized_text)

        # If the result of the above is an empty string, the clear
        # most_recent_filepath variable, and the audio_status widget,
        # and display the appropriate warning message to the user.
        if not sanitized_text:
            change_most_recent_filepath()
            change_entry_text(entry_to_change=audio_status)
            messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING,
                                   message=globals.MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING)
            return

        # Translate the normalized text to Morse code.
        # Letters are looked up in the MORSE_CODE_DICT, and they're
        # separated by a space, while the words are separated
        # by a slash with a space on either side.
        mcode: str = " / ".join(" ".join(map(lambda c: globals.MORSE_CODE_DICT.get(c, ""), word)) for word
                                in split_user_text)
        mcode = mcode.strip()
        change_entry_text(entry_to_change=output_entry, change_to=mcode)

        if audio_request:
            create_audio_file(normalized_text=normalized_text, audio_status=audio_status)

    else:
        # Display a warning if the user has not provided any input
        messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING,
                               message=globals.MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING)


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

    if not isinstance(user_morse_code_text, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_PLAIN_FIRST_ARG_WRONG_ERROR)
        return

    if not isinstance(audio_request, bool):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_PLAIN_SECOND_ARG_WRONG_ERROR)
        return

    if not isinstance(audio_status, tk.Entry):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_PLAIN_THIRD_ARG_WRONG_ERROR)
        return

    if not isinstance(output_entry, tk.Entry):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_TO_PLAIN_FOURTH_ARG_WRONG_ERROR)
        return

    if not user_morse_code_text:
        # Display a warning if the user has not provided any input
        messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING,
                               message=globals.MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING)
        return

    # Check if only legal chars are contained in user_morse_code_text
    only_legal = re.fullmatch(pattern=globals.PATT_SANITIZE_MORSE_CODE_INPUT, string=user_morse_code_text)

    if not only_legal:
        # Display a warning if the user has provided illegal chars
        messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING,
                               message=globals.MESSAGEBOX_MSG_TRANSLATE_TO_PLAIN_WARNING)
        return

    # Replace each occurrence of two spaces or more with one space
    user_morse_code_text_reduced: str = re.sub(pattern=globals.PATT_REDUCE_SPACES_MORSE_CODE_INPUT,
                                               repl=" ",
                                               string=user_morse_code_text)
    # Split the user's input into a list of words
    split_user_morse_code_text: list = user_morse_code_text_reduced.split(sep=" / ")

    # Create the dictionary with switched keys and values
    switched_morse_code_dict: dict = {v: k for k, v in globals.MORSE_CODE_DICT.items()}

    # Translate the Morse code to plain text.
    # Symbols are looked up in switched_morse_code_dict,
    # and the words are separated by a space.
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
        # about the meaningless input.
        change_most_recent_filepath()
        change_entry_text(entry_to_change=audio_status)
        messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING,
                               message=globals.MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING)


def copy_to_clipboard(text_to_copy: str) -> None:
    """Copies the arg to the system clipboard.

    Args:
        text_to_copy: str: String from an entry widget.

    Returns:
        None
    """

    if not isinstance(text_to_copy, str):
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CLIPBOARD_WRONG_ARG_ERROR)
        return

    if text_to_copy:
        # Copy text to the system clipboard and display
        # a success message to the user.
        pyperclip.copy(text=text_to_copy)
        messagebox.showinfo(title=globals.MESSAGEBOX_TITLE_SUCCESS, message=globals.MESSAGEBOX_MSG_COPY_SUCCESS)

    else:
        # Display a warning if there is no input
        messagebox.showwarning(title=globals.MESSAGEBOX_TITLE_WARNING, message=globals.MESSAGEBOX_MSG_COPY_WARNING)


def clear_all(*args: tk.Entry) -> None:
    """Clears all text input and output fields.

    Args:
        args: tk.Entry: A variable number of entry widgets to clear
                        all text from.

    Returns:
          None
    """

    if not args:
        messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                             message=globals.MESSAGEBOX_MSG_CLEAR_ALL_LACK_ARG_ERROR)
        return

    for widget in args:
        if not isinstance(widget, tk.Entry):
            messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR,
                                 message=globals.MESSAGEBOX_MSG_CLEAR_ALL_WRONG_ARG_ERROR)
            return

    for widget in args:
        change_entry_text(entry_to_change=widget)

    change_most_recent_filepath()
