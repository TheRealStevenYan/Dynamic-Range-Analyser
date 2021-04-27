import tkinter as tk
import tkinter.ttk as ttk

from operations.file_operations import AudioData, AudioDataLog


#TO DO: add an about section or a question mark or something which explains what dynamic range etc is


# This class will keep track of audio data using an AudioDataLog
class MainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.geometry("800x400")
        self.audio_data = AudioData()
        self.output_box = tk.Text(self.window, width=30, height=10)
        self.__audio_data_record = []

        self.__update_text_results()
        self.make_open_file_button()
        self.make_save_button()
        self.display_database()
        self.window.mainloop()

    # Makes a button which, when pressed, opens a window to select an audio file.
    # When an audio file is selected, it then parses the audio file and prints out its data.
    def make_open_file_button(self):
        open_button = tk.Button(self.window, text="Open File", width=50, height=5, command=lambda: self.__open_button_helper())
        open_button.grid(column=1)

    def make_save_button(self):
        save_button = tk.Button(self.window, text="Save Results", width=50, height=5, command=lambda:self.__save_button_helper())
        save_button.grid(column=1)

    def display_database(self):
        log = AudioDataLog()
        data = log.db_query()
        db_table = Table(headings=('File Name', 'Dynamic Range', 'Score'), rows=data)
        db_table.grid(row=0, column=2, rowspan=23)

    def __save_button_helper(self):
        log = AudioDataLog()
        log.db_insert(self.audio_data)
        self.display_database()

    # A helper function which handles what happens when the 'open file' button is pressed.
    def __open_button_helper(self):
        if self.audio_data.audio_segment is not None:
            self.__audio_data_record.append(self.audio_data)
            print(self.__audio_data_record)
        self.audio_data.open_file()
        self.__update_text_results()

    # Updates the text on the window. Bunch of tkinter stuff going on here.
    def __update_text_results(self):
        self.output_box.configure(state="normal", font=("Courier", 15))
        self.output_box.delete('1.0', tk.END)
        self.output_box.tag_configure("center", justify='center')
        self.__print_scores()
        self.output_box.tag_add("center", 1.0, "end")
        self.output_box.configure(state="disabled")
        self.output_box.grid(column=1)

    def __print_scores(self):
        self.output_box.insert(tk.INSERT, interpret_dr(self.audio_data.dynamic_range))
        self.output_box.insert(tk.INSERT, interpret_score(self.audio_data.dynamic_range_score))


# A custom tkinter-driven table class which uses displays SQLite databases. Has a scroll bar.
# To use: call constructor with the parent frame, headings in first arg and database query in second arg
class Table(tk.Frame):
    def __init__(self, headings=tuple(), rows=tuple()):
        super().__init__()

        table = ttk.Treeview(self, show="headings", selectmode="browse", height=18)
        table["columns"] = headings
        table["displaycolumns"] = headings

        for header in headings:
            table.heading(header, text=header, anchor=tk.CENTER)
            table.column(header, anchor=tk.CENTER, width=137)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scroll_table = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scroll_table.set)
        scroll_table.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def interpret_dr(dynamic_range):
    return "Dynamic Range: {dr} dB\n".format(dr=dynamic_range)


def interpret_score(score):
    return "Score: {sc}\n".format(sc=score)
