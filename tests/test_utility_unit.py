"""These unit tests evaluate whether the utility functions used
by the app work as expected, and whether they can handle
some edge cases.

The tested functions are:
1. change_entry_text,
2. change_most_recent_filepath,
3. copy_to_clipboard,
4. and clear_all.
"""

import tkinter as tk
from unittest.mock import patch, PropertyMock
import pytest
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

    def test_no_args(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with no arguments.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.change_entry_text()  # noqa

    def test_more_than_two_args(self, tk_root) -> None:
        """Test whether the function raises TypeError in the event
        it's called with more than two arguments.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.change_entry_text(tk.Entry(tk_root), "arg2", True)  # noqa

    def test_wrong_first_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'entry_to_change' is not an instance of tkinter.Entry.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.change_entry_text(entry_to_change=1.2)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_FIRST_ARG_ERROR)

    def test_wrong_second_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'change_to' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.change_entry_text(entry_to_change=tk.Entry(tk_root), change_to=3)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CHANGE_ENTRY_WRONG_SECOND_ARG_ERROR)

    def test_delete_entry_text_normal_state(self, tk_root) -> None:
        """Test whether the function correctly deletes all text from
        a tkinter.Entry with state "normal" and verify the state
        doesn't change.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        entry_normal = tk.Entry(tk_root)
        entry_normal.insert(index=0, string=TEST_TEXT)
        entry_normal.pack()

        functions.change_entry_text(entry_to_change=entry_normal)

        assert entry_normal.get() == "", "The entry's text wasn't set to an empty string."
        assert entry_normal.cget("state") == "normal", "The entry's state was changed."

    def test_delete_entry_text_readonly_state(self, tk_root) -> None:
        """Test whether the function correctly deletes all text from
        a tkinter.Entry with the original state "readonly" and verify
        the entry's state is reverted to the original.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        entry_readonly = tk.Entry(tk_root)
        entry_readonly.insert(index=0, string=TEST_TEXT)
        entry_readonly.config(state="readonly")
        entry_readonly.pack()

        functions.change_entry_text(entry_to_change=entry_readonly)

        assert entry_readonly.get() == "", "The entry's text wasn't set to an empty string."
        assert entry_readonly.cget("state") == "readonly", "The entry's state wasn't reverted to 'readonly'."

    def test_change_entry_text_normal_state(self, tk_root) -> None:
        """Test whether the function correctly changes the text from
        a tkinter.Entry with state "normal" and verify the state
        doesn't change.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        entry_normal = tk.Entry(tk_root)
        entry_normal.insert(index=0, string=TEST_TEXT)
        entry_normal.pack()

        functions.change_entry_text(entry_to_change=entry_normal, change_to="New Text")

        assert entry_normal.get() == "New Text", "The entry's text wasn't set to the expected string."
        assert entry_normal.cget("state") == "normal", "The entry's state was changed."

    def test_change_entry_text_readonly_state(self, tk_root) -> None:
        """Test whether the function correctly changes the text from
        a tkinter.Entry with the original state "readonly" and verify
        the entry's state is reverted to the original.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        entry_readonly = tk.Entry(tk_root)
        entry_readonly.insert(index=0, string=TEST_TEXT)
        entry_readonly.config(state="readonly")
        entry_readonly.pack()

        functions.change_entry_text(entry_to_change=entry_readonly, change_to="New Text")

        assert entry_readonly.get() == "New Text", "The entry's text wasn't set to the expected string."
        assert entry_readonly.cget("state") == "readonly", "The entry's state wasn't reverted to 'readonly'."


class Test_ChangeMostRecentFilepath:
    """Group of tests for the 'change_most_recent_filepath'
    utility function.

    These tests ensure the 'most_recent_audio_filepath' variable is updated
    correctly, and that the function properly handles invalid inputs.
    """

    def test_more_than_one_arg(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with no arguments.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.change_most_recent_filepath("", "arg2")  # noqa

    def test_wrong_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'change_to' is not of type str.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.change_most_recent_filepath(change_to=1.2)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CHANGE_FILEPATH_WRONG_ARG_ERROR)

    def test_change_and_erase_global_var(self) -> None:
        """Test whether the function correctly sets the variable
        'most_recent_audio_filepath' both to an empty string
        and non-empty string.

        Returns:
              None
        """

        with patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var:
            mock_var.return_value = TEST_PATH
            functions.change_most_recent_filepath(change_to=TEST_PATH)
            assert mock_var.return_value == TEST_PATH, ("The variable 'most_recent_audio_filepath'"
                                                        " wasn't set to the expected string.")

            mock_var.return_value = ""
            functions.change_most_recent_filepath()
            assert mock_var.return_value == "", ("The variable 'most_recent_audio_filepath' wasn't set to an empty"
                                                 " string.")


class Test_CopyToClipboard:
    """Group of tests for the 'copy_to_clipboard' utility function.

    These tests ensure the function can copy valid inputs to the system
    clipboard correctly, and that it properly handles invalid inputs.
    """

    def test_no_args(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with no arguments.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.copy_to_clipboard()  # noqa

    def test_more_than_one_arg(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with more than one argument.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.copy_to_clipboard("arg1", "arg2")  # noqa

    def test_wrong_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'text_to_copy' is not of type str.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.copy_to_clipboard(text_to_copy=2.5)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CLIPBOARD_WRONG_ARG_ERROR)

    def test_empty_str(self) -> None:
        """Test whether the function displays a warning message with
        the expected title and content in the event the argument
        'text_to_copy' is an empty string.

        Returns:
              None
        """

        with patch(target="tkinter.messagebox.showwarning") as mock_showwarning:
            functions.copy_to_clipboard(text_to_copy="")
            assert mock_showwarning.called, "The warning message wasn't displayed."

            mock_showwarning.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_COPY_WARNING)

    def test_copy_to_clipboard_with_valid_input(self) -> None:
        """Test whether the function correctly copies the given string
        to the system clipboard, and displays an info message with
        the expected title and content.

        Returns:
              None
        """

        with patch(target="functions.messagebox.showinfo") as mock_showinfo, \
                patch(target="pyperclip.paste", return_value=TEST_TEXT) as mock_paste:
            functions.copy_to_clipboard(text_to_copy=TEST_TEXT)
            clipboard_content: str = mock_paste()

            assert clipboard_content == TEST_TEXT, "TEST_TEXT wasn't copied to the system clipboard."
            assert mock_showinfo.called, "The info message wasn't displayed."

            mock_showinfo.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_SUCCESS,
                message=globals.MESSAGEBOX_MSG_COPY_SUCCESS)


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

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.clear_all()
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CLEAR_ALL_LACK_ARG_ERROR)

    def test_wrong_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event at least
        one of the arguments is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.clear_all(tk.Entry(tk_root), 0)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CLEAR_ALL_WRONG_ARG_ERROR)

    def test_clear_success(self, tk_root) -> None:
        """Test whether the function correctly clears all text from
        valid arguments, all of which are instances of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var:
            mock_var.return_value = TEST_PATH

            arg1_clear_all = tk.Entry(tk_root)
            arg1_clear_all.insert(index=0, string=TEST_TEXT)
            arg1_clear_all.pack()

            arg2_clear_all = tk.Entry(tk_root)
            arg2_clear_all.insert(index=0, string=TEST_TEXT)
            arg2_clear_all.pack()

            functions.clear_all(arg1_clear_all, arg2_clear_all)
            mock_var.return_value = ""

            assert arg1_clear_all.get() == "", "The first argument wasn't set to an empty string."
            assert arg2_clear_all.get() == "", "The second argument wasn't set to an empty string."
            assert mock_var.return_value == "", ("The variable 'most_recent_audio_filepath' wasn't"
                                                 " set to the expected string.")
