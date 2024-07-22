## [v1.0.0] -- 2024-07-22
### Added
- The directory `tests`.
- The file `test_audio.wav` for testing the `play_audio_create` function.
- Two basic test suites (`tests_primary.py` and `tests_utility.py`) for the project.
- The file `py_test.ini` containing basic configuration for Pytest.
- The file `requirements-dev.txt`.
- A number of error message constants for `tkinter.messagebox.showerror`.
- A number of `try-except` blocks to functions in `functions.py` for better handling of invalid arguments.
- An intermediary variable to hold the sanitization check in the `translate_to_plain_text` function for readability.

### Changed
- Raised the minimal required version of Python from **3.7** to **3.9** (as determined by Vermin).
- Renamed a significant number of constants in `globals.py` for better uniformity.
- Introduced subsections for a better organization of error message constants in `globals.py`.
- Added visual cues that should help in determining sections and subsections of `globals.py`.
- Changed docstrings and comments in `functions.py` for improved readability.

### Removed
- The unnecessary casting of `re.search` return object to `bool` from the `create_audio_file` function.
- Eliminated several unnecessarily complex conditional statements from functions in `functions.py`.

### Fixed
- A defect allowing the function `translate_to_morse_code` to pass an empty string to `create_audio_file`.

### Upcoming Changes
- Current test suites will be split into proper unit and integration tests for improved coverage and maintainability.
- Manual test cases covering integration tests will be added to the `tests` directory.

## [v0.9.0] -- 2024-07-20
### Added
- Added a new button color for utility buttons.
- Added a new label and font for contact and license information.

### Changed
- Made all imports explicit.
- Renamed the modules directory to `morsecode`.
- Renamed the entry point to `mcode.py`.
- Applied the button bg color -- used so far for all buttons -- only to primary buttons.
- Decreased the Y-padding of the canvas to `10`.
- Changes the prefix of messagebox-related constants from `MSGBOX` to `MESSAGEBOX`.
- Minor changes in docstrings and comments for clarity and brevity.

### Removed
- Removed the unnecessary main function from `mcode.py`.

## [v0.8.0] -- 2024-07-20
### Added
- A utility function `change_most_recent_filepath()` that, as the name suggests, sets the global variable to a new value.
- A utility function `clear_all()` that will clear all input/output fields in the app (and will call the above-mentioned function, too).
- A new button `button_clear_all` and the related UI functionality.
- A main function in `morse_code.py` that will only be called if the file is run directly.
- A comment for the global variable `most_recent_audio_filepath`.

### Changed
- Functions will now call `change_most_recent_filepath()` instead of writing to `most_recent_audio_filepath` themselves.
- Regex patterns verbose descriptions for clarity.
- Module docstrings in `functions.py` for readibility.

## [v0.7.0] -- 2024-07-19
### Added
- A regex pattern used in searching for and, optionally, removing illegal characters (unsupported by the pycw module) in plain text input.
- A new messagebox message used to ask the user whether to automatically remove illegal characters before creating the audio file, or whether to skip the audio generation.
- A check in the `create_audio_file()` function that searches the normalized_text argument for the above-mentioned illegal characters, and prompts the user to make the above-mentioned decision.
- Some comments to clarify these additions.

## [v0.6.0] -- 2024-07-18
### Added
- Two warning message constants for when the user inputs valid characters that are still meaningless to Morse code, (e.g., "----------").
- A utility function `change_entry_text()` specialized in modifying entry widgets' texts while respecting the widgets' states ("normal"/"readonly").

### Changed
- Streamlined entry widgets' text modification. Functions that previously edited them, will now call the new utility function, instead.
- Some docstrings and comments for clarity.

## [v0.5.0] -- 2024-07-18
### Added
- A new constant `READONLY_ENTRY_BG_COLOR` to hold the new color for the `entry_audio_status` widget background.
- A new constant `ENTRY_AUDIO_STATUS_WIDTH` to hold the new width for the `entry_audio_status` widget.
- A new constant `BUTTON_BORDER_WIDTH` to hold the new width for buttons.
- A new constant `BUTTON_BG_COLOR` to hold the new background color for unpressed buttons.
- A new constant `BUTTON_PRESSED_BG_COLOR` to hold the new background color for pressed buttons.
- A screenshot of the app main window to the readme.

### Complete UI overhaul
- **Summary**: Completely overhauled the UI for improved user experience and accessibility.
- **Key Changes**:
  - Updated color palette to a modern scheme with a white background and Prussian Blue accents.
  - Redesigned buttons to enhance visibility and interactivity.
- **Detailed Changes**:
  - Changed button colors to include a Prussian Blue background with white text for primary actions.
  - Adjusted the layout to be more intuitive.
- **Impact**:
  - Enhanced contrast and legibility for users with visual impairments.

### Other changes
- Changed some docstrings, comments and variable names for clarity.

### Fixed
- Wrong dates in the changelog.
- Some typos.

### Removed
- The `BUTTON_LARGE_WIDTH` constant as it's no longer needed.

## [v0.4.1] -- 2024-07-17
### Fixed
- Eliminated an illegally used parameter in the call to `os.exists()` in the `create_audio_file()` function.

## [v0.4.0] -- 2024-07-17
### Added
- Created two directories: `modules` and `images`.
- Added exception handling and error message if the logo can't be found.
- Created the constant `DEFAULT_AUDIO_OUTPUT_DIR` which stores the directory name where the app will attempt to save audio files.
- Added parameters to most functions as they're now called with data by the lambdas in `UI.py`.
- The `create_audio_file()` function will now create the above-mentioned directory if it doesn't exist.

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