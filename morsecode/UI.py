"""
This module contains all the user interface components for the
application.

It defines the layout and behavior of the GUI, including buttons,
entry fields, labels, and other Tkinter widgets.
"""

import tkinter as tk
from tkinter import messagebox
import functions
import globals

# Root window setup with padding and bg color
root = tk.Tk()
root.title(string=globals.APP_TITLE)
root.config(padx=globals.PADD_X, pady=globals.PADD_Y, bg=globals.BG_COLOR)

# Canvas for displaying the application logo
canvas = tk.Canvas(width=globals.IMG_WIDTH, height=globals.IMG_HEIGHT)

try:
    app_logo = tk.PhotoImage(file=globals.LOGO_FILEPATH)

except FileNotFoundError:
    messagebox.showerror(title=globals.MESSAGEBOX_TITLE_ERROR, message=globals.MESSAGEBOX_MSG_LOGO_ERROR)

else:
    # Center the logo image on the canvas
    canvas.create_image(globals.IMG_WIDTH // 2, globals.IMG_HEIGHT // 2, image=app_logo)
    canvas.config(bg=globals.BG_COLOR, highlightthickness=0)
    canvas.grid(column=0, row=0, columnspan=4)

# Labels for i/o entry widgets with custom font and color
label_plain_text_io = tk.Label(text=globals.LABEL_PLAIN_TEXT_IO_TEXT,
                               fg=globals.STATIC_TEXT_COLOR,
                               bg=globals.BG_COLOR,
                               font=globals.FONT_LABEL)
label_plain_text_io.grid(column=0, row=2)

label_morse_code_io = tk.Label(text=globals.LABEL_MORSE_CODE_IO_TEXT,
                               fg=globals.STATIC_TEXT_COLOR,
                               bg=globals.BG_COLOR,
                               font=globals.FONT_LABEL)
label_morse_code_io.grid(column=0, row=3)

label_audio_status = tk.Label(text=globals.LABEL_AUDIO_STATUS_TEXT,
                              fg=globals.STATIC_TEXT_COLOR,
                              bg=globals.BG_COLOR,
                              font=globals.FONT_LABEL)
label_audio_status.grid(column=0, row=4)

label_info = tk.Label(text=globals.LABEL_INFO_TEXT,
                      fg=globals.STATIC_TEXT_COLOR,
                      bg=globals.BG_COLOR,
                      font=globals.FONT_INFO)
label_info.grid(column=0, row=6, columnspan=4, pady=globals.LABEL_INFO_Y_PADD)

# Entry widgets for plain text i/o, Morse code i/o,
# and audio status with custom width
entry_plain_text_io = tk.Entry(width=globals.ENTRY_WIDTH)
entry_plain_text_io.focus()  # Automatically focus on the text entry field
entry_plain_text_io.grid(column=1, row=2)

entry_morse_code_io = tk.Entry(width=globals.ENTRY_WIDTH)
entry_morse_code_io.grid(column=1, row=3)

entry_audio_status = tk.Entry(width=globals.ENTRY_AUDIO_STATUS_WIDTH,
                              readonlybackground=globals.READONLY_ENTRY_BG_COLOR)
entry_audio_status.config(state="readonly")  # Display audio file status, not editable by the user
entry_audio_status.grid(column=1, row=4, columnspan=2)

# Buttons for translating text, copying text,
# and playing audio with custom styles
button_translate_to_morse = tk.Button(text=globals.BUTTON_TRANSLATE_TO_MORSE_TEXT,
                                      font=globals.FONT_BUTTON,
                                      width=globals.BUTTON_WIDTH,
                                      command=lambda: functions.translate_to_morse_code(
                                          user_plain_text=entry_plain_text_io.get(),
                                          audio_request=audio_requested.get(),
                                          audio_status=entry_audio_status,
                                          output_entry=entry_morse_code_io),
                                      bg=globals.BUTTON_PRIMARY_BG_COLOR,
                                      fg=globals.BUTTON_TEXT_COLOR,
                                      activebackground=globals.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                                      activeforeground=globals.BUTTON_TEXT_COLOR,
                                      border=globals.BUTTON_BORDER_WIDTH)
button_translate_to_morse.grid(column=2, row=2, padx=globals.BUTTON_X_PADD)

button_copy_plain = tk.Button(text=globals.BUTTON_COPY_TEXT,
                              font=globals.FONT_BUTTON,
                              width=globals.BUTTON_WIDTH,
                              command=lambda: functions.copy_to_clipboard(text_to_copy=entry_plain_text_io.get()),
                              bg=globals.BUTTON_PRIMARY_BG_COLOR,
                              fg=globals.BUTTON_TEXT_COLOR,
                              activebackground=globals.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                              activeforeground=globals.BUTTON_TEXT_COLOR,
                              border=globals.BUTTON_BORDER_WIDTH)
button_copy_plain.grid(column=3, row=2)

button_translate_to_plain = tk.Button(text=globals.BUTTON_TRANSLATE_TO_PLAIN_TEXT,
                                      font=globals.FONT_BUTTON,
                                      width=globals.BUTTON_WIDTH,
                                      command=lambda: functions.translate_to_plain_text(
                                          user_morse_code_text=entry_morse_code_io.get().strip(),
                                          audio_request=audio_requested.get(),
                                          audio_status=entry_audio_status,
                                          output_entry=entry_plain_text_io),
                                      bg=globals.BUTTON_PRIMARY_BG_COLOR,
                                      fg=globals.BUTTON_TEXT_COLOR,
                                      activebackground=globals.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                                      activeforeground=globals.BUTTON_TEXT_COLOR,
                                      border=globals.BUTTON_BORDER_WIDTH)
button_translate_to_plain.grid(column=2, row=3, padx=globals.BUTTON_X_PADD)

button_copy_morse = tk.Button(text=globals.BUTTON_COPY_TEXT,
                              font=globals.FONT_BUTTON,
                              width=globals.BUTTON_WIDTH,
                              command=lambda: functions.copy_to_clipboard(text_to_copy=entry_morse_code_io.get()),
                              bg=globals.BUTTON_PRIMARY_BG_COLOR,
                              fg=globals.BUTTON_TEXT_COLOR,
                              activebackground=globals.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                              activeforeground=globals.BUTTON_TEXT_COLOR,
                              border=globals.BUTTON_BORDER_WIDTH)
button_copy_morse.grid(column=3, row=3)

button_play_audio = tk.Button(text=globals.BUTTON_PLAY_TEXT,
                              font=globals.FONT_BUTTON,
                              width=globals.BUTTON_WIDTH,
                              command=lambda: functions.play_audio_file(audio_status=entry_audio_status.get()),
                              bg=globals.BUTTON_PRIMARY_BG_COLOR,
                              fg=globals.BUTTON_TEXT_COLOR,
                              activebackground=globals.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                              activeforeground=globals.BUTTON_TEXT_COLOR,
                              border=globals.BUTTON_BORDER_WIDTH)
button_play_audio.grid(column=3, row=4)

button_clear_all = tk.Button(text=globals.BUTTON_CLEAR_TEXT,
                             font=globals.FONT_BUTTON,
                             width=globals.BUTTON_WIDTH,
                             command=lambda: functions.clear_all(entry_plain_text_io, entry_morse_code_io,
                                                                 entry_audio_status),
                             bg=globals.BUTTON_SECOND_BG_COLOR,
                             fg=globals.BUTTON_TEXT_COLOR,
                             activebackground=globals.BUTTON_SECOND_PRESSED_BG_COLOR,
                             activeforeground=globals.BUTTON_TEXT_COLOR,
                             border=globals.BUTTON_BORDER_WIDTH)
button_clear_all.grid(column=1, row=5, columnspan=2)

# Checkbox for deciding whether to produce the audio file
audio_requested = tk.BooleanVar(value=globals.CHECKBOX_VAL_OFF)  # Holds the current decision (bool), defaults to False

checkbox_audio_request = tk.Checkbutton(text=globals.CHECKBOX_TEXT,
                                        variable=audio_requested,
                                        onvalue=globals.CHECKBOX_VAL_ON,
                                        offvalue=globals.CHECKBOX_VAL_OFF,
                                        bg=globals.BG_COLOR,
                                        highlightthickness=0,
                                        font=globals.FONT_CHECKBOX,
                                        fg=globals.STATIC_TEXT_COLOR,
                                        activebackground=globals.BG_COLOR,
                                        activeforeground=globals.STATIC_TEXT_COLOR,
                                        selectcolor=globals.BG_COLOR)
checkbox_audio_request.grid(column=1, row=1)
