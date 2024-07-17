## [0.3.0] -- 2024-07-17
### Added
- Functionality to translate Morse code into plain text.
- The copy_plain_text() function to call the utility function with the argument from the entry_text widget.
- The utility function copy_to_clipboard() to avoid repetition with the two copying functions.
- The "re" module to sanitize user input, and two compiled patterns for the same purpose.
- A MessageBox message to cover the added functions.

### Changed
- Reworked copy_morse_translation() definition to call the new utility function with the arg from the entry_morse_code_io widget.
- Changed the layout to accomodate new buttons.
- Renamed several global-scope variables for improved clarity.
- Modified the style of buttons to make them look more modern (not over yet, though).

### Fixed
- Some typos.

## [0.2.0] -- 2024-07-16
### Added
- A checkbox to allow the user to decide whether they want to generate an audio file.
- Symbols handling during translation to Morse code (for now, without the "@" symbol).
- Exception handling for permission errors during audio file creation, and audio playback errors.
- MessageBox titles and messages to cover error handling.

### Changed
- Changed the main filename to 'morse_code.py'
- Changed the UI layout to accomodate the addition of the checkbox.
- Changed the translate_to_morse_code() function definition to accomodate the addition of the checkbox.
- Changed the create_audio_file() function definition to display the newest audio filename instead of "READY & SAVED".
- Minor updates to the application title, comments and docstrings for better clarity.

### Fixed
- Typos in code comments for improved readability.

## [0.1.0] -- 2024-07-16
### Added
- Created basic functionality and UI.