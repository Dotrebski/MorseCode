"""
This module is the entry point for the GUI application.

It initializes the main window and starts the event loop.
The application provides a user-friendly interface for translating
plain text to Morse code and vice versa, and generating audio files
with Morse code based on either Morse code or plain text input.
"""

from morsecode.UI import tk

if __name__ == "__main__":
    tk.mainloop()
