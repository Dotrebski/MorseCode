## [v0.4.0] -- 2024-07-18
### Added
- Created two directories: `modules` and `images`.
- Added exception handling and error message if the logo can't be found.

### Changed
- Split the entire application into `morse_code.py` and three modules: `UI.py`, `functions.py` and `globals.py`.
- The three modules were moved to the `modules` directory.
- The `app_logo.png` image was moved to the `images` directory.
- Renamed several functions, UI labels, widgets, and buttons to make them shorter and more indicative of their purpose.
- Adopted explicit parameter names when calling functions and methods.
- Expanded function and method calls with 4+ args (3+ if the call is in a lambda), so that each arg is on a separate line for readability.
- Replaced all named function from the UI with lambdas.
- Removed the `copy_plain_text()` and `copy_morse_translation()` functions as they're no longer needed.
- Moved the `most_recent_audio_filepath` variable to `functions.py`.
- Added parameters to most functions as they're now called with data by the lambdas in `UI.py`.
- Created the constant `DEFAULT_AUDIO_OUTPUT_DIR` which stores the directory name where the app will attempt to save audio files.
- The `create_audio_file()` function will now create the above-mentioned directory if it doesn't exist.
- Changed the main font to Arial and adjusted its size for the three types of texts.

### Fixed
- Eliminated some typos in the changelog.
- Fixed the regex pattern that reduces spaces in Morse code input.

## [v0.3.0] -- 2024-07-17
### Added
- Functionality to translate Morse code into plain text.
- The `copy_plain_text()` function to call the utility function with the argument from the entry_text widget.
- The utility function `copy_to_clipboard()` to avoid repetition with the two copying functions.
- The "re" module to sanitize user input, and two compiled patterns for the same purpose.
- A MessageBox message to cover the added functions.

### Changed
- Reworked `copy_morse_translation()` definition to call the new utility function with the arg from the `entry_morse_code_io` widget.
- Changed the layout to accommodate new buttons.
- Renamed several global-scope variables for improved clarity.
- Modified the style of buttons to make them look more modern (not over yet, though).

### Fixed
- Some typos.

## [v0.2.0] -- 2024-07-16
### Added
- A checkbox to allow the user to decide whether they want to generate an audio file.
- Symbols handling during translation to Morse code (for now, without the "@" symbol).
- Exception handling for permission errors during audio file creation, and audio playback errors.
- MessageBox titles and messages to cover error handling.

### Changed
- Changed the main filename to 'morse_code.py'
- Changed the UI layout to accommodate the addition of the checkbox.
- Changed the `translate_to_morse_code()` function definition to accommodate the addition of the checkbox.
- Changed the `create_audio_file()` function definition to display the newest audio filename instead of "READY & SAVED".
- Minor updates to the application title, comments and docstrings for better clarity.

### Fixed
- Typos in code comments for improved readability.

## [v0.1.0] -- 2024-07-16
### Added
- Created basic functionality and UI.