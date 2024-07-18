"""
Morse Code Translator & Audio Generator v0.5.0

This script provides a GUI application to translate text to Morse code, and vice versa,
generate audio files for the Morse code, and play them back.

Dependencies:
- tkinter for the GUI
- unidecode for transliteration of Unicode into ASCII
- pyperclip for clipboard operations
- pycw for Morse code audio generation
- playsound3 for audio playback

Usage:
Run this script directly to launch the application.
No command-line arguments are required.
"""

import modules.UI as UI

# Entering the main loop
UI.tk.mainloop()
