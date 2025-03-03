"""
This module contains all the user interface components for the
application.

It defines the layout and behavior of the GUI, including buttons,
entry fields, labels, and other Tkinter widgets.
"""

import tkinter as tk
from tkinter import messagebox
import morsecode.functions as functions
import morsecode.globals as global_const

# Root window setup with padding and bg color
root = tk.Tk()
root.title(string=global_const.APP_TITLE)
root.config(padx=global_const.ROOT_PAD_X, pady=global_const.ROOT_PAD_Y, bg=global_const.ROOT_BG_COLOR)

# Canvas for displaying the application logo
canvas = tk.Canvas(width=global_const.IMG_WIDTH, height=global_const.IMG_HEIGHT)

try:
    app_logo = tk.PhotoImage(file=global_const.LOGO_FILEPATH)

except FileNotFoundError:
    messagebox.showerror(title=global_const.MESSAGEBOX_TITLE_ERROR, message=global_const.MESSAGEBOX_MSG_LOGO_ERROR)

else:
    # Center the logo image on the canvas
    canvas.create_image(global_const.IMG_WIDTH // 2, global_const.IMG_HEIGHT // 2, image=app_logo)
    canvas.config(bg=global_const.ROOT_BG_COLOR, highlightthickness=0)
    canvas.grid(column=0, row=0, columnspan=4)

# Labels for i/o entry widgets with custom font and color
label_plain_text_io = tk.Label(text=global_const.LABEL_PLAIN_TEXT_IO_TEXT,
                               fg=global_const.STATIC_TEXT_COLOR,
                               bg=global_const.ROOT_BG_COLOR,
                               font=global_const.FONT_LABEL)
label_plain_text_io.grid(column=0, row=2)

label_morse_code_io = tk.Label(text=global_const.LABEL_MORSE_CODE_IO_TEXT,
                               fg=global_const.STATIC_TEXT_COLOR,
                               bg=global_const.ROOT_BG_COLOR,
                               font=global_const.FONT_LABEL)
label_morse_code_io.grid(column=0, row=3)

label_audio_status = tk.Label(text=global_const.LABEL_AUDIO_STATUS_TEXT,
                              fg=global_const.STATIC_TEXT_COLOR,
                              bg=global_const.ROOT_BG_COLOR,
                              font=global_const.FONT_LABEL)
label_audio_status.grid(column=0, row=4)

label_info = tk.Label(text=global_const.LABEL_INFO_TEXT,
                      fg=global_const.STATIC_TEXT_COLOR,
                      bg=global_const.ROOT_BG_COLOR,
                      font=global_const.FONT_INFO)
label_info.grid(column=0, row=6, columnspan=4, pady=global_const.LABEL_INFO_PAD_X)

# Entry widgets for plain text i/o, Morse code i/o,
# and audio status with custom width
entry_plain_text_io = tk.Entry(width=global_const.ENTRY_WIDTH)
entry_plain_text_io.focus()  # Automatically focus on the text entry field
entry_plain_text_io.grid(column=1, row=2)

entry_morse_code_io = tk.Entry(width=global_const.ENTRY_WIDTH)
entry_morse_code_io.grid(column=1, row=3)

entry_audio_status = tk.Entry(width=global_const.ENTRY_AUDIO_STATUS_WIDTH,
                              readonlybackground=global_const.READONLY_ENTRY_BG_COLOR)
entry_audio_status.config(state="readonly")  # Display audio file status, not editable by the user
entry_audio_status.grid(column=1, row=4, columnspan=2)

# Buttons for translating text, copying text,
# and playing audio with custom styles
button_translate_to_morse = tk.Button(text=global_const.BUTTON_TRANSLATE_TO_MORSE_TEXT,
                                      font=global_const.FONT_BUTTON,
                                      width=global_const.BUTTON_WIDTH,
                                      command=lambda: functions.translate_to_morse_code(
                                          user_plain_text=entry_plain_text_io.get(),
                                          audio_request=audio_requested.get(),
                                          audio_status=entry_audio_status,
                                          output_entry=entry_morse_code_io),
                                      bg=global_const.BUTTON_PRIMARY_BG_COLOR,
                                      fg=global_const.BUTTON_TEXT_COLOR,
                                      activebackground=global_const.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                                      activeforeground=global_const.BUTTON_TEXT_COLOR,
                                      border=global_const.BUTTON_BORDER_WIDTH)
button_translate_to_morse.grid(column=2, row=2, padx=global_const.BUTTON_PAD_X)

button_copy_plain = tk.Button(text=global_const.BUTTON_COPY_TEXT,
                              font=global_const.FONT_BUTTON,
                              width=global_const.BUTTON_WIDTH,
                              command=lambda: functions.copy_to_clipboard(text_to_copy=entry_plain_text_io.get()),
                              bg=global_const.BUTTON_PRIMARY_BG_COLOR,
                              fg=global_const.BUTTON_TEXT_COLOR,
                              activebackground=global_const.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                              activeforeground=global_const.BUTTON_TEXT_COLOR,
                              border=global_const.BUTTON_BORDER_WIDTH)
button_copy_plain.grid(column=3, row=2)

button_translate_to_plain = tk.Button(text=global_const.BUTTON_TRANSLATE_TO_PLAIN_TEXT,
                                      font=global_const.FONT_BUTTON,
                                      width=global_const.BUTTON_WIDTH,
                                      command=lambda: functions.translate_to_plain_text(
                                          user_morse_code_text=entry_morse_code_io.get().strip(),
                                          audio_request=audio_requested.get(),
                                          audio_status=entry_audio_status,
                                          output_entry=entry_plain_text_io),
                                      bg=global_const.BUTTON_PRIMARY_BG_COLOR,
                                      fg=global_const.BUTTON_TEXT_COLOR,
                                      activebackground=global_const.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                                      activeforeground=global_const.BUTTON_TEXT_COLOR,
                                      border=global_const.BUTTON_BORDER_WIDTH)
button_translate_to_plain.grid(column=2, row=3, padx=global_const.BUTTON_PAD_X)

button_copy_morse = tk.Button(text=global_const.BUTTON_COPY_TEXT,
                              font=global_const.FONT_BUTTON,
                              width=global_const.BUTTON_WIDTH,
                              command=lambda: functions.copy_to_clipboard(text_to_copy=entry_morse_code_io.get()),
                              bg=global_const.BUTTON_PRIMARY_BG_COLOR,
                              fg=global_const.BUTTON_TEXT_COLOR,
                              activebackground=global_const.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                              activeforeground=global_const.BUTTON_TEXT_COLOR,
                              border=global_const.BUTTON_BORDER_WIDTH)
button_copy_morse.grid(column=3, row=3)

button_play_audio = tk.Button(text=global_const.BUTTON_PLAY_TEXT,
                              font=global_const.FONT_BUTTON,
                              width=global_const.BUTTON_WIDTH,
                              command=lambda: functions.play_audio_file(audio_status=entry_audio_status.get()),
                              bg=global_const.BUTTON_PRIMARY_BG_COLOR,
                              fg=global_const.BUTTON_TEXT_COLOR,
                              activebackground=global_const.BUTTON_PRIMARY_PRESSED_BG_COLOR,
                              activeforeground=global_const.BUTTON_TEXT_COLOR,
                              border=global_const.BUTTON_BORDER_WIDTH)
button_play_audio.grid(column=3, row=4)

button_clear_all = tk.Button(text=global_const.BUTTON_CLEAR_TEXT,
                             font=global_const.FONT_BUTTON,
                             width=global_const.BUTTON_WIDTH,
                             command=lambda: functions.clear_all(entry_plain_text_io, entry_morse_code_io,
                                                                 entry_audio_status),
                             bg=global_const.BUTTON_SECOND_BG_COLOR,
                             fg=global_const.BUTTON_TEXT_COLOR,
                             activebackground=global_const.BUTTON_SECOND_PRESSED_BG_COLOR,
                             activeforeground=global_const.BUTTON_TEXT_COLOR,
                             border=global_const.BUTTON_BORDER_WIDTH)
button_clear_all.grid(column=1, row=5, columnspan=2)

# Checkbox for deciding whether to produce the audio file
audio_requested = tk.BooleanVar(value=global_const.CHECKBOX_VAL_OFF)  # Holds the current decision, defaults to off

checkbox_audio_request = tk.Checkbutton(text=global_const.CHECKBOX_TEXT,
                                        variable=audio_requested,
                                        onvalue=global_const.CHECKBOX_VAL_ON,
                                        offvalue=global_const.CHECKBOX_VAL_OFF,
                                        bg=global_const.ROOT_BG_COLOR,
                                        highlightthickness=0,
                                        font=global_const.FONT_CHECKBOX,
                                        fg=global_const.STATIC_TEXT_COLOR,
                                        activebackground=global_const.ROOT_BG_COLOR,
                                        activeforeground=global_const.STATIC_TEXT_COLOR,
                                        selectcolor=global_const.ROOT_BG_COLOR)
checkbox_audio_request.grid(column=1, row=1)
