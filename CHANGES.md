## [0.2.0] -- 2024-07-16
### Added
- A checkbox to allow the user to decide whether they want to generate an audio file.
- Symbols handling during translation to Morse code (for now, without the "@" symbol).
- Exception handling for permission errors during audio file creation, and audio playback errors.
- MessageBox titles and messages to cover error handling.

### Changed
- Changed the main filename to 'morse_code.py'
- Changed the UI layout to accomodate the addition of the checkbox.
- Changed the translate_to_morse_code function definition to accomodate the addition of the checkbox.
- Changed the create_audio_file function definition to display the newest audio filename instead of "READY & SAVED".
- Minor updates to the application title, comments and docstrings for better clarity.

### Fixed
- Typos in code comments for improved readability.

## [0.1.0] -- 2024-07-16
### Added
- Created basic functionality and UI.