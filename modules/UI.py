"""
This module contains all the user interface components for the
Morse Code Translator application.

It defines the layout and behavior of the GUI, including buttons,
entry fields, labels, and other Tkinter widgets.
"""

from modules.functions import *

# Root window setup with padding and bg color
root = tk.Tk()
root.title(string=APP_TITLE)
root.config(padx=PADD_X, pady=PADD_Y, bg=BG_COLOR)

# Canvas for displaying the application logo
canvas = tk.Canvas(width=IMG_WIDTH, height=IMG_HEIGHT)

try:
    app_logo = tk.PhotoImage(file=LOGO_FILEPATH)

except FileNotFoundError:
    msgbox.showerror(title=MSGBOX_TITLE_ERROR, message=MSGBOX_MSG_LOGO_ERROR)

else:
    # Center the logo image on the canvas
    canvas.create_image(IMG_WIDTH // 2, IMG_HEIGHT // 2, image=app_logo)
    canvas.config(bg=BG_COLOR, highlightthickness=0)
    canvas.grid(column=0, row=0, columnspan=4)

# Labels for i/o entry widgets with custom font and color
label_plain_text_io = tk.Label(text=LABEL_PLAIN_TEXT_IO_TEXT,
                               fg=STATIC_TEXT_COLOR,
                               bg=BG_COLOR,
                               font=LABEL_FONT)
label_plain_text_io.grid(column=0, row=2)

label_morse_code_io = tk.Label(text=LABEL_MORSE_CODE_IO_TEXT,
                               fg=STATIC_TEXT_COLOR,
                               bg=BG_COLOR,
                               font=LABEL_FONT)
label_morse_code_io.grid(column=0, row=3)

label_audio_status = tk.Label(text=LABEL_AUDIO_STATUS_TEXT,
                              fg=STATIC_TEXT_COLOR,
                              bg=BG_COLOR,
                              font=LABEL_FONT)
label_audio_status.grid(column=0, row=4)

# Entry widgets for plain text i/o, Morse code i/o,
# and audio status with custom width
entry_plain_text_io = tk.Entry(width=ENTRY_WIDTH)
entry_plain_text_io.focus()  # Automatically focus on the text entry field
entry_plain_text_io.grid(column=1, row=2)

entry_morse_code_io = tk.Entry(width=ENTRY_WIDTH)
entry_morse_code_io.grid(column=1, row=3)

entry_audio_status = tk.Entry(width=ENTRY_WIDTH)
entry_audio_status.config(state="readonly")  # Display audio file status, not editable by the user
entry_audio_status.grid(column=1, row=4)

# Buttons for translating text, copying text,
# and playing audio with custom styles
button_translate_to_morse = tk.Button(text=BUTTON_TRANSLATE_TO_MORSE_TEXT,
                                      font=BUTTON_FONT,
                                      width=BUTTON_SMALL_WIDTH,
                                      command=lambda: translate_to_morse_code(user_plain_text=entry_plain_text_io.get(),
                                                                              output_entry=entry_morse_code_io,
                                                                              audio_request=audio_requested.get(),
                                                                              audio_status=entry_audio_status),
                                      bg=BG_COLOR,
                                      fg=STATIC_TEXT_COLOR,
                                      activebackground=BG_COLOR,
                                      activeforeground=STATIC_TEXT_COLOR)
button_translate_to_morse.grid(column=2, row=2, padx=BUTTON_X_PADD)

button_copy_plain = tk.Button(text=BUTTON_COPY_TEXT,
                              font=BUTTON_FONT,
                              width=BUTTON_SMALL_WIDTH,
                              command=lambda: copy_to_clipboard(text_to_copy=entry_plain_text_io.get()),
                              bg=BG_COLOR,
                              fg=STATIC_TEXT_COLOR,
                              activebackground=BG_COLOR,
                              activeforeground=STATIC_TEXT_COLOR)
button_copy_plain.grid(column=3, row=2)

button_translate_to_plain = tk.Button(text=BUTTON_TRANSLATE_TO_PLAIN_TEXT,
                                      font=BUTTON_FONT,
                                      width=BUTTON_SMALL_WIDTH,
                                      command=lambda: translate_to_plain_text(
                                          user_morse_code_text=entry_morse_code_io.get().strip(),
                                          output_entry=entry_plain_text_io,
                                          audio_status=entry_audio_status),
                                      bg=BG_COLOR,
                                      fg=STATIC_TEXT_COLOR,
                                      activebackground=BG_COLOR,
                                      activeforeground=STATIC_TEXT_COLOR)
button_translate_to_plain.grid(column=2, row=3, padx=BUTTON_X_PADD)

button_copy_morse = tk.Button(text=BUTTON_COPY_TEXT,
                              font=BUTTON_FONT,
                              width=BUTTON_SMALL_WIDTH,
                              command=lambda: copy_to_clipboard(text_to_copy=entry_morse_code_io.get()),
                              bg=BG_COLOR,
                              fg=STATIC_TEXT_COLOR,
                              activebackground=BG_COLOR,
                              activeforeground=STATIC_TEXT_COLOR)
button_copy_morse.grid(column=3, row=3)

button_play_audio = tk.Button(text=BUTTON_PLAY_TEXT,
                              font=BUTTON_FONT,
                              width=BUTTON_LARGE_WIDTH,
                              command=lambda: play_audio_file(audio_status=entry_audio_status.get()),
                              bg=BG_COLOR,
                              fg=STATIC_TEXT_COLOR,
                              activebackground=BG_COLOR,
                              activeforeground=STATIC_TEXT_COLOR)
button_play_audio.grid(column=2,
                       row=4,
                       padx=BUTTON_X_PADD,
                       columnspan=2)

# Checkbox for deciding whether to produce the audio file
audio_requested = tk.BooleanVar(value=VAL_OFF_CHECKBOX)  # Holds the current decision (bool), defaults to off (False)

checkbox_audio_request = tk.Checkbutton(text=CHECKBOX_TEXT,
                                        variable=audio_requested,
                                        onvalue=VAL_ON_CHECKBOX,
                                        offvalue=VAL_OFF_CHECKBOX,
                                        bg=BG_COLOR,
                                        highlightthickness=0,
                                        font=CHECKBOX_FONT,
                                        fg=STATIC_TEXT_COLOR,
                                        activebackground=BG_COLOR,
                                        activeforeground=STATIC_TEXT_COLOR,
                                        selectcolor=BG_COLOR)
checkbox_audio_request.grid(column=1, row=1)
