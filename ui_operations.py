import tkinter as tk
import tkinter.ttk as ttk

from file_operations import AudioData, AudioDataLog


# A custom tkinter-driven table class which uses displays SQLite databases. Has a scroll bar.
# Double clicking on an entry deletes it.
# To use: call constructor with the parent frame, headings in first arg and database query in second arg
class Table(tk.Frame):
    # Constructor. Call: Table(headings = <HEADERS AS A TUPLE>, rows = <DATABASE DATA AS A TUPLE>)
    def __init__(self, headings=tuple(), rows=tuple()):
        super().__init__()

        self.table = ttk.Treeview(self, show="headings", selectmode="browse", height=18)
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings

        for header in headings:
            self.table.heading(header, text=header, anchor=tk.CENTER)
            self.table.column(header, anchor=tk.CENTER, width=137)
            self.table.bind('<Double-Button-1>', self.double_click_delete)

        for row in rows:
            self.table.insert('', tk.END, values=tuple(row))

        scroll_table = tk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll_table.set)
        scroll_table.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    # Deletes an entry from the table gui and the database when an entry is double clicked.
    def double_click_delete(self, arg):
        cur_sel = self.table.focus()
        cur_item = self.table.item(cur_sel)
        cur_item_name = cur_item.get('values')[0]
        log = AudioDataLog()
        log.db_delete(cur_item_name)
        display_database()


# Makes a button which, when pressed, opens a window to select an audio file.
# When an audio file is selected, it then parses the audio file and prints out its data.
def make_open_file_button():
    open_button = tk.Button(window, text="Open File", width=50, height=5, command=lambda: __open_button_helper())
    open_button.grid(column=1)


# Makes the save button.
# Calls a helper which does exactly that when it is clicked.
def make_save_button():
    save_button = tk.Button(window, text="Save Results", width=50, height=5, command=lambda:__save_button_helper())
    save_button.grid(column=1)


# Displays the database onto the tkinter GUI.
def display_database():
    log = AudioDataLog()
    data = log.db_query()
    db_table = Table(headings=('File Name', 'Dynamic Range', 'Score'), rows=data)
    db_table.grid(row=0, column=2, rowspan=23)


# Updates the text on the window. Bunch of tkinter stuff going on here.
def update_text_results():
    output_box.configure(state="normal", font=("Courier", 15))
    output_box.delete('1.0', tk.END)
    output_box.tag_configure("center", justify='center')
    __print_scores()
    output_box.tag_add("center", 1.0, "end")
    output_box.configure(state="disabled")
    output_box.grid(column=1)


# Private. Helper function which handles saving to the database.
def __save_button_helper():
    log = AudioDataLog()
    log.db_insert(audio_data)
    display_database()


# Private. A helper function which handles what happens when the 'open file' button is pressed.
def __open_button_helper():
    if audio_data.audio_segment is not None:
        audio_data_record.append(audio_data)
    audio_data.open_file()
    update_text_results()


# Private. Prints the file name and scores of everything onto a tkinter text box.
def __print_scores():
    output_box.insert(tk.INSERT, audio_data.file_name)
    output_box.insert(tk.INSERT, __interpret_dr(audio_data.dynamic_range))
    output_box.insert(tk.INSERT, __interpret_score(audio_data.dynamic_range_score))


# Private. Formats a string with dynamic range info.
def __interpret_dr(dynamic_range):
    return "Dynamic Range: {dr} dB\n".format(dr=dynamic_range)


# Private. Formats a string with score info.
def __interpret_score(score):
    return "Score: {sc}\n".format(sc=score)


window = tk.Tk()
window.resizable(False, False)
window.geometry("800x397")
audio_data = AudioData()
output_box = tk.Text(window, width=30, height=10)
audio_data_record = []

update_text_results()
make_open_file_button()
make_save_button()
display_database()
window.mainloop()