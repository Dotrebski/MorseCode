"""These integration tests evaluate whether the primary functions used
by the app work as expected, and whether they can handle some
edge cases.

The tested functions are:
1. play_audio_file,
2. create_audio_file,
3. translate_to_morse_code,
4. and translate_to_plain_text.
"""

import os
import tkinter as tk
from tkinter import messagebox
import pytest
from morsecode import functions
from morsecode import globals

# Globals
TK_MESSAGE_ERROR: str = "tkinter.messagebox.showerror"
TK_MESSAGE_WARN: str = "tkinter.messagebox.showwarning"
TEST_PATH: str = "output/morse_code_audio.wav"
TEST_TEXT: str = "Test text"


@pytest.fixture(scope="function")
def tk_root():
    """A fixture returning a top-level tkinter widget."""

    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()


class Test_PlayAudioFile:
    """Group of tests for the 'play_audio_file' function.

    These tests ensure the function can correctly play .wav audio
    files, as well as handle edge case and invalid arguments.
    """

    def test_wrong_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not of type str.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_PLAY_WRONG_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.play_audio_file(audio_status=1.2)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_no_file_yet(self) -> None:
        """Test whether the function displays a warning message with
        the expected title and content in the event the argument
        'audio_status' is an empty string.

        Returns:
              None
        """

        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_PLAY_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        try:
            self.messagebox_called = False
            functions.play_audio_file(audio_status="")  # noqa
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning


class Test_CreateAudioFile:
    """Group of tests for the 'create_audio_file' function.

    These tests ensure the function can create a valid .wav file,
    handle invalid inputs, PermissionError, and allow the user
    to decide whether they want invalid characters removed from their
    input automatically.
    """

    def test_wrong_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'normalized_text' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CREATE_AUDIO_FIRST_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.create_audio_file(normalized_text=3, audio_status=tk.Entry(tk_root))  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_second_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not an instance of tkinter.Entry.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CREATE_AUDIO_SECOND_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.create_audio_file(normalized_text=TEST_TEXT, audio_status=3.9)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_user_confirms_false(self, tk_root) -> None:
        """Test whether the function displays a confirmation prompt
        when the provided input is invalid. The prompt should
        ask the user whether they want the app to automatically delete
        illegal characters. This test covers the path where the user
        resigns from creating the audio file altogether.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_askyesno(title, message):
            assert title == globals.MESSAGEBOX_TITLE_CONFIRM
            assert message == globals.MESSAGEBOX_MSG_AUTO_CLEANUP_CONFIRM
            self.messagebox_called = True
            return False

        original_askyesno = messagebox.askyesno
        messagebox.askyesno = mock_askyesno

        invalid_text: str = "#test@"
        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        try:
            self.messagebox_called = False
            functions.create_audio_file(normalized_text=invalid_text, audio_status=audio_status)  # noqa
            assert self.messagebox_called, "The confirmation prompt wasn't displayed."
        finally:
            messagebox.askyesno = original_askyesno

        assert audio_status.get() == "", "The variable 'audio_status' wasn't set to an empty string."
        assert audio_status.cget("state") == "readonly", ("The variable 'audio_status' wasn't restored"
                                                          "to its original state ('readonly').")
        assert functions.most_recent_audio_filepath == "", ("The variable 'most_recent_audio_filepath'"
                                                            " wasn't set to an empty string.")

    def test_user_confirms_true(self, tk_root) -> None:
        """Test whether the function displays a confirmation prompt
        when the provided input is invalid. The prompt should
        ask the user whether they want the app to automatically delete
        illegal characters. This test covers the path where the user
        agrees, and the audio file is created.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_askyesno(title, message):
            assert title == globals.MESSAGEBOX_TITLE_CONFIRM
            assert message == globals.MESSAGEBOX_MSG_AUTO_CLEANUP_CONFIRM
            self.messagebox_called = True
            return True

        original_askyesno = messagebox.askyesno
        messagebox.askyesno = mock_askyesno

        audio_filepath: str = f"{globals.DEFAULT_AUDIO_OUTPUT_DIR}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
        invalid_text: str = "@test#"
        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        try:
            self.messagebox_called = False
            functions.create_audio_file(normalized_text=invalid_text, audio_status=audio_status)  # noqa
            assert self.messagebox_called, "The confirmation prompt wasn't displayed."
            assert os.path.exists(audio_filepath), f"The file {audio_filepath} wasn't created."
        finally:
            messagebox.askyesno = original_askyesno
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)

        assert functions.most_recent_audio_filepath == audio_filepath, ("The variable most_recent_audio_filepath wasn't"
                                                                        " set to audio_filepath'.")

        ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
        assert audio_status.get() == ready_message, "The entry audio_status wasn't set to ready_message."

    def test_happy_path(self, tk_root) -> None:
        """Test whether the function can create an audio file given
        the right arguments.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        audio_filepath: str = f"{globals.DEFAULT_AUDIO_OUTPUT_DIR}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
        valid_text: str = TEST_TEXT
        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        try:
            functions.create_audio_file(normalized_text=valid_text, audio_status=audio_status)
            assert os.path.exists(audio_filepath), f"The file {audio_filepath} wasn't created."

        finally:
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)

        assert functions.most_recent_audio_filepath == audio_filepath, \
            "The variable most_recent_audio_filepath wasn't set to audio_filepath'."

        ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
        assert audio_status.get() == ready_message, "The entry audio_status wasn't set to ready_message."


class Test_TranslateToMorseCode:
    """Group of tests for the 'translate_to_morse_code' function.

    These tests ensure the function can handle normal usage
    and edge cases, translating valid inputs into Morse code,
    and calling the create_audio_file function if the user wishes so.
    """

    def test_wrong_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_plain_text' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_MORSE_FIRST_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_morse_code(user_plain_text=1,  # noqa
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_second_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_request' is not of type bool.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_MORSE_SECOND_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_morse_code(user_plain_text=TEST_TEXT,
                                              audio_request=2,  # noqa
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_third_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_MORSE_THIRD_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_morse_code(user_plain_text=TEST_TEXT,
                                              audio_request=True,
                                              audio_status=1,  # noqa
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_fourth_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
         the expected title and content in the event the argument
         'output_entry' is not an instance of tkinter.Entry.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_MORSE_FOURTH_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_morse_code(user_plain_text=TEST_TEXT,
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=1)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_empty_first_arg(self, tk_root) -> None:
        """Test whether the function displays a warning message with
         the expected title and content in the event the argument
         'user_plain_text' is an empty string.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        try:
            self.messagebox_called = False
            functions.translate_to_morse_code(user_plain_text="",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning

    def test_meaningless_first_arg(self, tk_root) -> None:
        """Test whether the function displays a warning message with
         the expected title and content in the event the argument
         'user_plain_text' consists of characters that, although legal,
         can't be translated into Morse code. Currently, the list
         of such characters includes symbols unsupported by the pycw
         module and non-ASCII characters that can't be easily
         represented by ASCII characters.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        audio_status = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        try:
            self.messagebox_called = False
            functions.change_most_recent_filepath(change_to=TEST_TEXT)
            functions.translate_to_morse_code(user_plain_text="##",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning

        assert functions.most_recent_audio_filepath == "", ("The variable most_recent_audio_filepath"
                                                            " wasn't set to an empty string.")
        assert audio_status.get() == "", "The audio_status text wasn't set to an empty string."
        assert audio_status.cget("state") == "readonly", "The audio_status state wasn't set to 'readonly'."

    def test_happy_with_audio(self, tk_root) -> None:
        """Test whether the function can correctly translate a valid
        plain-text input into Morse code, and whether it can call
        the create_audio_file function to generate the audio file.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        expected_morse_code: str = "..--- / ... . .- ..."  # "2 SEAS"

        audio_filepath: str = f"{globals.DEFAULT_AUDIO_OUTPUT_DIR}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        try:
            functions.translate_to_morse_code(user_plain_text=" 2 SeAs",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=output_entry)
            assert os.path.exists(audio_filepath), f"The file {audio_filepath} wasn't created."

        finally:
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)

        assert output_entry.get() == expected_morse_code, "output_entry text didn't match the expected Morse code."
        assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

        assert functions.most_recent_audio_filepath == audio_filepath, \
               "The variable most_recent_audio_filepath wasn't set to the generated audio file filepath."

        ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
        assert audio_status.get() == ready_message, "audio_status text didn't match ready_message."


class Test_TranslateToPlainText:
    """Group of tests for the 'translate_to_plain_text' function.

    These tests ensure the function can handle normal usage
    and edge cases, translating valid inputs into plain text,
    and calling the create_audio_file function if the user wishes so.
    """

    def test_wrong_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_PLAIN_FIRST_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text=2,  # noqa
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_second_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_request' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_PLAIN_SECOND_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text=".",
                                              audio_request=2,  # noqa
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The error message wasn't displayed."

        finally:
            messagebox.showerror = original_showerror

    def test_wrong_third_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_PLAIN_THIRD_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text="-",
                                              audio_request=True,
                                              audio_status=-3,  # noqa
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The error message wasn't displayed."

        finally:
            messagebox.showerror = original_showerror

    def test_wrong_fourth_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'output_entry' is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_TO_PLAIN_FOURTH_ARG_WRONG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text="-",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=1)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."

        finally:
            messagebox.showerror = original_showerror

    def test_empty_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' is an empty string.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text="",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning

    def test_bad_chars_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' contains illegal characters.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_TRANSLATE_TO_PLAIN_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text="#$gaw",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning

    def test_meaningless_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' contains characters that are meaningless
        to Morse code.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """
        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        audio_status = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        functions.change_most_recent_filepath(change_to=TEST_TEXT)

        try:
            self.messagebox_called = False
            functions.translate_to_plain_text(user_morse_code_text="-----------",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=tk.Entry(tk_root))
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning

        assert functions.most_recent_audio_filepath == "", ("The variable most_recent_audio_filepath"
                                                            " wasn't set to an empty string.")
        assert audio_status.get() == "", "audio_status text wasn't set to an empty string."
        assert audio_status.cget("state") == "readonly", "audio_status state wasn't reverted to its original state."

    def test_happy_with_audio(self, tk_root) -> None:
        """Test whether the function can correctly translate a valid
        Morse code input into plain text, and whether it can call
        the create_audio_file function to generate the audio file.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        audio_filepath: str = f"{globals.DEFAULT_AUDIO_OUTPUT_DIR}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"

        expected_plain_text = "2 SEAS"  # "..--- / ... . .- ..."
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        try:
            functions.translate_to_plain_text(user_morse_code_text="..--- / ... . .- ...",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=output_entry)
            assert os.path.exists(audio_filepath), f"The file {audio_filepath} wasn't created."

        finally:
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)

        assert output_entry.get() == expected_plain_text, "output_entry didn't match expected_plain_text."
        assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

        assert functions.most_recent_audio_filepath == audio_filepath, \
               "The variable most_recent_audio_filepath wasn't set to audio_filepath."

        ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
        assert audio_status.get() == ready_message, "audio_status text wasn't set to ready_message."
