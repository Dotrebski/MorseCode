"""These unit tests evaluate whether the primary functions used
by the app work as expected, and whether they can handle some
edge cases.

The tested functions are:
1. play_audio_file,
2. create_audio_file,
3. translate_to_morse_code,
4. and translate_to_plain_text.
"""

import os
import tempfile
import tkinter as tk
from unittest.mock import patch, PropertyMock
import pytest
from playsound3.playsound3 import PlaysoundException
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

    def test_no_args(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with no arguments.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.play_audio_file()  # noqa

    def test_more_than_one_arg(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with more than one argument.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.play_audio_file("arg1", "arg2")  # noqa

    def test_wrong_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not of type str.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.play_audio_file(audio_status=2)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_PLAY_WRONG_ARG_ERROR
            )

    def test_wrong_file(self) -> None:
        """Test whether the function can handle a filepath
        to a non-existing audio file by raising PlaysoundException,
        and displaying an error message with the expected title
        and content.

        Returns:
              None
        """

        error_message: str = "Error message"

        with patch(target='playsound3.playsound', side_effect=PlaysoundException(error_message)), \
                patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.play_audio_file(audio_status=TEST_TEXT)  # The value doesn't matter as long as it's not empty.
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=functions.globals.MESSAGEBOX_TITLE_ERROR,
                message=error_message)

    def test_no_file_yet(self) -> None:
        """Test whether the function displays a warning message with
        the expected title and content in the event the argument
        'audio_status' is an empty string.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_WARN) as mock_showwarn:
            functions.play_audio_file("")
            assert mock_showwarn.called, "The warning message wasn't displayed."

            mock_showwarn.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_PLAY_WARNING)

    def test_play_existing_file(self) -> None:
        """Test whether the function can play back a valid .wav file
        a warning message with the expected title and content
        in the event the argument 'audio_status' is an empty string.

        Returns:
              None
        """

        try:
            functions.play_audio_file("tests/test_audio.wav")
        except Exception as e:
            pytest.fail(f"An unexpected exception was raised: {e}")


class Test_CreateAudioFile:
    """Group of tests for the 'create_audio_file' function.

    These tests ensure the function can create a valid .wav file,
    handle invalid inputs, PermissionError, and allow the user
    to decide whether they want invalid characters removed from their
    input automatically.
    """

    def test_no_args(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with no arguments.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.create_audio_file()  # noqa

    def test_more_than_two_args(self) -> None:
        """Test whether the function raises TypeError in the event
        it's called with more than two arguments.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.create_audio_file("arg1", "arg2", "arg3")  # noqa

    def test_wrong_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'normalized_text' is not of type str.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.create_audio_file(normalized_text=3, audio_status=tk.Entry(tk_root))  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CREATE_AUDIO_FIRST_ARG_WRONG_ERROR)

    def test_wrong_second_arg(self) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not an instance of tkinter.Entry.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.create_audio_file(normalized_text=TEST_TEXT, audio_status=3.9)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_CREATE_AUDIO_SECOND_ARG_WRONG_ERROR)

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

        invalid_text: str = "#test@"
        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with patch(target='functions.messagebox.askyesno', return_value=False) as mock_askyesno, \
                patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var:
            mock_var.return_value = TEST_PATH
            functions.create_audio_file(normalized_text=invalid_text, audio_status=audio_status)
            mock_var.return_value = ""

            assert mock_askyesno.called, "The confirmation prompt wasn't displayed."
            assert invalid_text == "#test@", "The invalid input was sanitized."
            assert audio_status.get() == "", "The variable 'audio_status' wasn't set to an empty string."
            assert audio_status.cget("state") == "readonly", ("The variable 'audio_status' wasn't restored"
                                                              "to its original state ('readonly').")
            assert mock_var.return_value == "", ("The variable 'most_recent_audio_filepath' wasn't"
                                                 " set to an empty string.")

            mock_askyesno.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_CONFIRM,
                message=globals.MESSAGEBOX_MSG_AUTO_CLEANUP_CONFIRM
            )

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

        invalid_test: str = "@test#"
        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with patch(target="functions.messagebox.askyesno", return_value=True) as mock_askyesno, \
                patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var, \
                tempfile.TemporaryDirectory() as tmp_dir, \
                patch(target="globals.DEFAULT_AUDIO_OUTPUT_DIR", new=tmp_dir):
            mock_var.return_value = ""
            functions.create_audio_file(normalized_text=invalid_test, audio_status=audio_status)
            audio_filepath: str = f"{tmp_dir}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
            mock_var.return_value = audio_filepath

            assert os.path.isdir(tmp_dir), "The directory wasn't created in the test directory."
            assert os.path.exists(audio_filepath), f"The file {audio_filepath} wasn't created."
            assert mock_var.return_value == audio_filepath, \
                "The variable most_recent_audio_filepath wasn't set to audio_filepath."

            ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
            assert audio_status.get() == ready_message, "The entry audio_status wasn't set to ready_message."

            mock_askyesno.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_CONFIRM,
                message=globals.MESSAGEBOX_MSG_AUTO_CLEANUP_CONFIRM
            )

    def test_happy_path(self, tk_root) -> None:
        """Test whether the function can create an audio file given
        the right arguments.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        normalized_text: str = TEST_TEXT
        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var, \
                tempfile.TemporaryDirectory() as tmp_dir, \
                patch(target="globals.DEFAULT_AUDIO_OUTPUT_DIR", new=tmp_dir):
            mock_var.return_value = ""
            functions.create_audio_file(normalized_text=normalized_text, audio_status=audio_status)
            audio_filepath = f"{tmp_dir}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
            mock_var.return_value = audio_filepath

            assert os.path.isdir(tmp_dir), "The directory wasn't created in the test directory."
            assert os.path.exists(audio_filepath), f"The file {audio_filepath} wasn't created."
            assert mock_var.return_value == audio_filepath, \
                "The variable 'most_recent_audio_filepath' wasn't set to audio_filepath'."

            ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
            assert audio_status.get() == ready_message, "The entry audio_status wasn't set to ready_message."

    def test_perm_err(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the correct title and content in the event PermissionError
        is raised.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target='functions.os.makedirs', side_effect=PermissionError), \
                patch(target='builtins.open', side_effect=PermissionError), \
                patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.create_audio_file(normalized_text=TEST_TEXT, audio_status=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_MORSE_PERM_ERROR)


class Test_TranslateToMorseCode:
    """Group of tests for the 'translate_to_morse_code' function.

    These tests ensure the function can handle normal usage
    and edge cases, translating valid inputs into Morse code,
    and calling the create_audio_file function if the user wishes so.
    """

    def test_no_args(self) -> None:
        """Test whether the function raises TypeError in the event
         it's called with no arguments.

         Returns:
               None
         """

        with pytest.raises(expected_exception=TypeError):
            functions.translate_to_morse_code()  # noqa

    def test_more_than_four_args(self, tk_root) -> None:
        """Test whether the function raises TypeError in the event
        it's called with more than four arguments.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.translate_to_morse_code("test text",
                                              False,
                                              tk.Entry(tk_root),
                                              tk.Entry(tk_root),
                                              7)  # noqa

    def test_wrong_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_plain_text' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_morse_code(user_plain_text=1,  # noqa
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_MORSE_FIRST_ARG_WRONG_ERROR)

    def test_wrong_second_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_request' is not of type bool.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_morse_code(user_plain_text=TEST_TEXT,
                                              audio_request=2,  # noqa
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_MORSE_SECOND_ARG_WRONG_ERROR)

    def test_wrong_third_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_morse_code(user_plain_text=TEST_TEXT,
                                              audio_request=True,
                                              audio_status=1,  # noqa
                                              output_entry=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_MORSE_THIRD_ARG_WRONG_ERROR)

    def test_wrong_fourth_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
         the expected title and content in the event the argument
         'output_entry' is not an instance of tkinter.Entry.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_morse_code(user_plain_text=TEST_TEXT,
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=1)  # noqa
            assert mock_showerror.called, "The error wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_MORSE_FOURTH_ARG_WRONG_ERROR)

    def test_empty_first_arg(self, tk_root) -> None:
        """Test whether the function displays a warning message with
         the expected title and content in the event the argument
         'user_plain_text' is an empty string.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        with patch(target=TK_MESSAGE_WARN) as mock_showwarning:
            functions.translate_to_morse_code(user_plain_text="",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showwarning.called, "The warning message wasn't displayed."

            mock_showwarning.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING)

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

        audio_status = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with patch(target=TK_MESSAGE_WARN) as mock_showwarning, \
                patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var:
            mock_var.return_value = TEST_TEXT

            functions.translate_to_morse_code(user_plain_text="##",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=tk.Entry(tk_root))
            mock_var.return_value = ""

            assert mock_var.return_value == "", ("The variable most_recent_audio_filepath"
                                                 " wasn't set to an empty string.")
            assert audio_status.get() == "", "The audio_status text wasn't set to an empty string."
            assert audio_status.cget("state") == "readonly", "The audio_status state wasn't set back to 'readonly'."
            assert mock_showwarning.called, "The warning message wasn't displayed."

            mock_showwarning.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING)

    def test_happy_no_audio(self, tk_root) -> None:
        """Test whether the function can correctly translate a valid
        plain-text input into Morse code, but don't generate
        the audio file.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        expected_morse_code: str = ".... . -.--"  # "HEY"
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        functions.translate_to_morse_code(user_plain_text="  hey ",
                                          audio_request=False,
                                          audio_status=tk.Entry(tk_root),
                                          output_entry=output_entry)

        assert output_entry.get() == expected_morse_code, "output_entry text didn't match the expected Morse code."
        assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

    def test_happy_no_audio_diacritics(self, tk_root) -> None:
        """Test whether the function can correctly translate a valid
        plain-text input containing diacritical letters into
        Morse code, but don't generate the audio file.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        expected_morse_code: str = "--.. --- .-.. -.-."  # "ZOLC"
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        functions.translate_to_morse_code(user_plain_text="żóŁć ",
                                          audio_request=False,
                                          audio_status=tk.Entry(tk_root),
                                          output_entry=output_entry)

        assert output_entry.get() == expected_morse_code, "output_entry text didn't match the expected Morse code."
        assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

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
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var, \
                tempfile.TemporaryDirectory() as tmp_dir, \
                patch('globals.DEFAULT_AUDIO_OUTPUT_DIR', new=tmp_dir):
            audio_filepath: str = f"{tmp_dir}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
            mock_var.return_value = ""
            functions.translate_to_morse_code(user_plain_text=" 2 SeAs",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=output_entry)
            mock_var.return_value = audio_filepath

            assert output_entry.get() == expected_morse_code, ("output_entry text didn't match the expected"
                                                               " Morse code.")
            assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

            assert os.path.isdir(tmp_dir), "The directory wasn't created in the test directory."
            assert os.path.exists(audio_filepath), "The audio file wasn't created."
            assert mock_var.return_value == audio_filepath, \
                "The variable most_recent_audio_filepath wasn't set to the generated audio file filepath."
            ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
            assert audio_status.get() == ready_message, "audio_status text didn't match ready_message."


class Test_TranslateToPlainText:
    """Group of tests for the 'translate_to_plain_text' function.

    These tests ensure the function can handle normal usage
    and edge cases, translating valid inputs into plain text,
    and calling the create_audio_file function if the user wishes so.
    """

    def test_no_args(self) -> None:
        """Test whether the function raises TypeError in the event
         it's called with no arguments.

         Returns:
               None
         """

        with pytest.raises(expected_exception=TypeError):
            functions.translate_to_plain_text()  # noqa

    def test_more_than_four_args(self, tk_root) -> None:
        """Test whether the function raises TypeError in the event
        it's called with more than four arguments.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with pytest.raises(expected_exception=TypeError):
            functions.translate_to_plain_text(".",
                                              False,
                                              tk.Entry(tk_root),
                                              tk.Entry(tk_root),
                                              7)  # noqa

    def test_wrong_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_plain_text(user_morse_code_text=2,  # noqa
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_PLAIN_FIRST_ARG_WRONG_ERROR)

    def test_wrong_second_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_request' is not of type str.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_plain_text(user_morse_code_text=".",
                                              audio_request=2,  # noqa
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_PLAIN_SECOND_ARG_WRONG_ERROR)

    def test_wrong_third_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'audio_status' is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_plain_text(user_morse_code_text="-",
                                              audio_request=True,
                                              audio_status=-3,  # noqa
                                              output_entry=tk.Entry(tk_root))
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_PLAIN_THIRD_ARG_WRONG_ERROR)

    def test_wrong_fourth_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'output_entry' is not an instance of tkinter.Entry.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_ERROR) as mock_showerror:
            functions.translate_to_plain_text(user_morse_code_text="-",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=1)  # noqa
            assert mock_showerror.called, "The error message wasn't displayed."

            mock_showerror.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_ERROR,
                message=globals.MESSAGEBOX_MSG_TO_PLAIN_FOURTH_ARG_WRONG_ERROR)

    def test_empty_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' is an empty string.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_WARN) as mock_showwarning:
            functions.translate_to_plain_text(user_morse_code_text="",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showwarning.called, "The warning message wasn't displayed."

            mock_showwarning.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_NOTHING_TO_TRANSLATE_WARNING)

    def test_bad_chars_first_arg(self, tk_root) -> None:
        """Test whether the function displays an error message with
        the expected title and content in the event the argument
        'user_morse_code_text' contains illegal characters.

        Args:
            tk_root: A top-level tkinter widget.

        Returns:
              None
        """

        with patch(target=TK_MESSAGE_WARN) as mock_showwarning:
            functions.translate_to_plain_text(user_morse_code_text="#$gaw",
                                              audio_request=True,
                                              audio_status=tk.Entry(tk_root),
                                              output_entry=tk.Entry(tk_root))
            assert mock_showwarning.called, "The warning message wasn't displayed."

            mock_showwarning.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_TRANSLATE_TO_PLAIN_WARNING)

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

        audio_status = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with patch(target=TK_MESSAGE_WARN) as mock_showwarning, \
                patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var:
            mock_var.return_value = TEST_TEXT
            functions.translate_to_plain_text(user_morse_code_text="-----------",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=tk.Entry(tk_root))
            mock_var.return_value = ""

            assert mock_var.return_value == "", ("The variable 'most_recent_audio_filepath'"
                                                 " wasn't set to an empty string.")
            assert audio_status.get() == "", "audio_status text wasn't set to an empty string."
            assert audio_status.cget("state") == "readonly", "audio_status state wasn't reverted to its original state."
            assert mock_showwarning.called, "The warning message wasn't displayed."

            mock_showwarning.assert_called_once_with(
                title=globals.MESSAGEBOX_TITLE_WARNING,
                message=globals.MESSAGEBOX_MSG_MEANINGLESS_INPUT_WARNING)

    def test_happy_no_audio(self, tk_root) -> None:
        """Test whether the function can correctly translate a valid
        Morse code input into plain text, but don't generate
        the audio file.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        expected_plain_text: str = "HEY"  # ".... . -.--"
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        functions.translate_to_plain_text(user_morse_code_text=" .... . -.-- ",
                                          audio_request=False,
                                          audio_status=tk.Entry(tk_root),
                                          output_entry=output_entry)

        assert output_entry.get() == expected_plain_text, "output_entry text didn't match expected_plain_text."
        assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

    def test_happy_with_audio(self, tk_root) -> None:
        """Test whether the function can correctly translate a valid
        Morse code input into plain text, and whether it can call
        the create_audio_file function to generate the audio file.

         Args:
             tk_root: A top-level tkinter widget.

         Returns:
               None
         """

        expected_plain_text = "2 SEAS"  # "..--- / ... . .- ..."
        output_entry = tk.Entry(tk_root)
        output_entry.insert(index=0, string=TEST_TEXT)
        output_entry.pack()

        audio_status: tk.Entry = tk.Entry(tk_root)
        audio_status.insert(index=0, string=TEST_TEXT)
        audio_status.config(state="readonly")
        audio_status.pack()

        with tempfile.TemporaryDirectory() as tmp_dir, \
                patch(target="globals.DEFAULT_AUDIO_OUTPUT_DIR", new=tmp_dir), \
                patch(target="functions.most_recent_audio_filepath", new_callable=PropertyMock) as mock_var:

            audio_filepath = f"{tmp_dir}/{globals.DEFAULT_AUDIO_OUTPUT_FILE}"
            mock_var.return_value = ""
            functions.translate_to_plain_text(user_morse_code_text="..--- / ... . .- ...",
                                              audio_request=True,
                                              audio_status=audio_status,
                                              output_entry=output_entry)
            mock_var.return_value = audio_filepath

            assert output_entry.get() == expected_plain_text, "output_entry didn't match expected_plain_text."
            assert output_entry.cget("state") == "normal", "output_entry state didn't match the original."

            assert os.path.isdir(tmp_dir), "The directory wasn't created in the test directory."
            assert os.path.exists(audio_filepath), "The audio file wasn't created."
            assert mock_var.return_value == audio_filepath, \
                "The variable most_recent_audio_filepath wasn't set to audio_filepath."

            ready_message: str = f"{globals.AUDIO_READY_MESSAGE} {audio_filepath}"
            assert audio_status.get() == ready_message, "audio_status text wasn't set to ready_message."
