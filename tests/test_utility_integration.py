"""These integration tests evaluate whether the utility functions used
by the app work as expected, and whether they can handle
some edge cases.

The tested functions are:
1. change_entry_text,
2. change_most_recent_filepath,
3. copy_to_clipboard,
4. and clear_all.
"""

import tkinter as tk
from tkinter import messagebox
import pytest
import pyperclip
from morsecode import functions
from morsecode import globals

# Globals
TK_MESSAGE_ERROR: str = "tkinter.messagebox.showerror"
TEST_PATH: str = "output/morse_code_audio.wav"
TEST_TEXT: str = "Test text"


@pytest.fixture(scope="function")
def tk_root():
    """A fixture returning a top-level tkinter widget."""

    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()


class Test_ChangeEntryText:
    """Group of tests for the 'change_entry_text' utility function.

    These tests ensure that the text within a Tkinter entry widget
    is updated correctly, reflecting both normal usage and edge cases
    such as invalid inputs.
    """

    def test_wrong_first_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'entry_to_change' is not an instance of tkinter.Entry.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_FIRST_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.change_entry_text(entry_to_change=1.2)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_second_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'change_to' is not of type str.

        Args:
            tk_root: The top-level tkinter wigdet.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_SECOND_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.change_entry_text(entry_to_change=tk.Entry(tk_root), change_to=3)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror


class Test_ChangeMostRecentFilepath:
    """Group of tests for the 'change_most_recent_filepath'
    utility function.

    These tests ensure the 'most_recent_audio_filepath' variable is updated
    correctly, and that the function properly handles invalid inputs.
    """

    def test_wrong_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'change_to' is not of type str.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CHANGE_FILEPATH_WRONG_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.change_most_recent_filepath(change_to=1.2)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_change_and_erase_global_var(self) -> None:
        """Test whether the function correctly sets the variable
        'most_recent_audio_filepath' both to an empty string
        and non-empty string.

        Returns:
              None
        """

        functions.change_most_recent_filepath(change_to=TEST_PATH)
        assert functions.most_recent_audio_filepath == TEST_PATH, ("The variable 'most_recent_audio_filepath' wasn't"
                                                                   " set to the expected string.")

        functions.change_most_recent_filepath()
        assert functions.most_recent_audio_filepath == "", ("The variable 'most_recent_audio_filepath' wasn't"
                                                            " set to an empty string.")


class Test_CopyToClipboard:
    """Group of tests for the 'copy_to_clipboard' utility function.

    These tests ensure the function can copy valid inputs to the system
    clipboard correctly, and that it properly handles invalid inputs.
    """

    def test_wrong_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'text_to_copy' is not of type str.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CLIPBOARD_WRONG_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.copy_to_clipboard(text_to_copy=1.2)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_empty_str(self) -> None:
        """Test whether the function displays a warning message with
        the expected title and content in the event the argument
        'text_to_copy' is an empty string.

        Returns:
              None
        """

        def mock_showwarning(title, message):
            assert title == globals.MESSAGEBOX_TITLE_WARNING
            assert message == globals.MESSAGEBOX_MSG_COPY_WARNING
            self.messagebox_called = True

        original_showwarning = messagebox.showwarning
        messagebox.showwarning = mock_showwarning

        try:
            self.messagebox_called = False
            functions.copy_to_clipboard(text_to_copy="")  # noqa
            assert self.messagebox_called, "The warning message wasn't displayed."
        finally:
            messagebox.showwarning = original_showwarning

    def test_copy_to_clipboard_with_valid_input(self) -> None:
        """Test whether the function correctly copies the given string
        to the system clipboard, and displays an info message with
        the expected title and content.

        Returns:
              None
        """

        def mock_showinfo(title, message):
            assert title == globals.MESSAGEBOX_TITLE_SUCCESS
            assert message == globals.MESSAGEBOX_MSG_COPY_SUCCESS
            self.messagebox_called = True

        original_showinfo = messagebox.showinfo
        messagebox.showinfo = mock_showinfo

        try:
            self.messagebox_called = False
            functions.copy_to_clipboard(text_to_copy=TEST_TEXT)  # noqa
            clipboard_content: str = pyperclip.paste()
            assert clipboard_content == TEST_TEXT, "TEST_TEXT wasn't copied to the system clipboard."
            assert self.messagebox_called, "The info message wasn't displayed."
        finally:
            messagebox.showinfo = original_showinfo


class Test_ClearAll:
    """Group of tests for the 'clear_all' utility function.

    These tests ensure the function can successfully clear text from
    tkinter.Entry instances passed to it as arguments.
    """

    def test_no_args(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        is an empty tuple.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CLEAR_ALL_LACK_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.clear_all()  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_wrong_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event at least
        one of the arguments is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        def mock_showerror(title, message):
            assert title == globals.MESSAGEBOX_TITLE_ERROR
            assert message == globals.MESSAGEBOX_MSG_CLEAR_ALL_WRONG_ARG_ERROR
            self.messagebox_called = True

        original_showerror = messagebox.showerror
        messagebox.showerror = mock_showerror

        try:
            self.messagebox_called = False
            functions.clear_all(tk.Entry(tk_root), 0)  # noqa
            assert self.messagebox_called, "The error message wasn't displayed."
        finally:
            messagebox.showerror = original_showerror

    def test_clear_success(self, tk_root) -> None:
        """Test whether the function correctly clears all text from
        valid arguments, all of which are instances of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        functions.change_most_recent_filepath(change_to=TEST_PATH)
        assert functions.most_recent_audio_filepath == TEST_PATH, ("The variable 'most_recent_audio_filepath' wasn't"
                                                                   " set to the expected string.")

        arg1_clear_all = tk.Entry(tk_root)
        arg1_clear_all.insert(index=0, string=TEST_TEXT)
        arg1_clear_all.pack()

        arg2_clear_all = tk.Entry(tk_root)
        arg2_clear_all.insert(index=0, string=TEST_TEXT)
        arg2_clear_all.pack()

        functions.clear_all(arg1_clear_all, arg2_clear_all)
        assert arg1_clear_all.get() == "", "The first argument wasn't set to an empty string."
        assert arg2_clear_all.get() == "", "The second argument wasn't set to an empty string."
        assert functions.most_recent_audio_filepath == "", ("The variable 'most_recent_audio_filepath' wasn't"
                                                            " set to the expected string.")
