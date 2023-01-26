"""
Python Script to delete files in a directory which are older than X days
"""
from os import listdir
from os.path import isdir, getmtime
from datetime import datetime, timedelta
from tkinter import filedialog
import customtkinter as ctk
from customwidget import CtkSpinbox
from send2trash import send2trash


class AutoDeleteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x170")
        self.title("Auto Delete")
        self.resizable(False, False)
        self.time_2_delete = ctk.IntVar()
        self.dir = ctk.StringVar()
        self._layout()

    def _layout(self):
        """Sets the GUI layout"""
        # Master Frame
        master = ctk.CTkFrame(self)
        master.pack(fill=ctk.BOTH)

        # Frame for directory choosing
        dir_choose = ctk.CTkFrame(master)
        dir_choose.pack(fill=ctk.BOTH, padx=5, pady=5, anchor="center")

        dir_label = ctk.CTkLabel(dir_choose, text="Choose directory")
        dir_label.grid(row=0,
                       column=0, columnspan=2,
                       sticky='w',
                       padx=10, pady=1)

        self.dir_entry = ctk.CTkEntry(master=dir_choose,
                                      placeholder_text="Enter directory here",
                                      width=430,
                                      height=28,
                                      textvariable=self.dir
                                      )
        self.dir_entry.grid(row=1, column=0,
                            sticky='w',
                            padx=(7, 5), pady=5
                            )

        directory_button = ctk.CTkButton(master=dir_choose,
                                         text="Choose directory",
                                         command=self.dir_dialog_callback
                                         )
        directory_button.grid(row=1, column=1,
                              sticky='e',
                              padx=5, pady=5
                              )

        # ↓ Frame for deletion parametes
        param_choose = ctk.CTkFrame(master)
        param_choose.pack(fill=ctk.X, padx=5, pady=5, anchor='center')

        time_to_live_txt_1 = ctk.CTkLabel(param_choose,
                                          text="Delte all files older than")
        time_to_live_txt_1.grid(row=1, column=0,
                                sticky='w',
                                padx=(10, 5), pady=5
                                )

        self.time_to_live = CtkSpinbox(param_choose,
                                       height=14, width=60,
                                       command=self.set_days,
                                       min_value=1,
                                       default=30
                                       )
        self.time_to_live.grid(row=1, column=1,
                               sticky='w',
                               padx=5, pady=5)

        time_to_live_txt_2 = ctk.CTkLabel(param_choose,
                                          text="days")
        time_to_live_txt_2.grid(row=1, column=2,
                                sticky='w',
                                padx=5, pady=5
                                )

        execute_btn = ctk.CTkButton(master,
                                    text="Execute",
                                    command=self.execute_callback
                                    )
        execute_btn.pack(padx=5, pady=5)

    def dir_dialog_callback(self):
        """ Callback funktion for directory dialog"""
        self.dir = filedialog.askdirectory()
        self.dir_entry.delete(0, "end")
        self.dir_entry.insert(0, self.dir)

    def execute_callback(self):
        """ Executes the deletion process """
        self.dir = self.dir_entry.get()
        self.time_2_delete = self.time_to_live.get()
        if self.time_2_delete <= 0:
            self.msg_box("Value Error",
                         "Day to delte can't be smaller than 1\n"
                         "Please correct your input"
                         )
            return

        if not self.dir:
            self.msg_box("ERROR: Directory can' be empty",
                         "You have not specified a directory yet.",
                         "Please enter a directory or select it manually by "
                         "clicking the \"Choose directory\" button."
                         )
            return
        try:
            file_list = [f for f in listdir(self.dir)]
            counter: int = 0
            for file in file_list:
                dump_file = self.dir + "/" + file
                if isdir(dump_file):
                    continue
                last_modified = datetime.fromtimestamp(
                    getmtime(dump_file)
                )
                now = datetime.now()
                t_delta = timedelta(int(self.time_2_delete) * -1)
                date_threshold = now + t_delta
                if date_threshold > last_modified:
                    dump_file = dump_file.replace('/', "\\")
                    counter += 1
                    send2trash(dump_file)
            if counter == 0:
                self.msg_box("Process failed",
                             "Operation failed due to the directory not "
                             "having a file that meets the requirements."
                             )
            else:
                self.msg_box("Process sucessfull",
                             f"{counter} files sucessfully deleted.")
        except Exception as err:
            self.msg_box("Uncaught exception",
                         err,
                         "Please report this error to the to:",
                         "https://github.com/JuleZR/Auto_Delete/issues"
                         )

    def set_days(self):
        """
        Gets the maximum age in days of a file from the SpinBox widget
        """
        self.time_2_delete = self.time_to_live.get()

    def msg_box(self, *args: str):
        """
        Calls a message box
        First argument is the title of the box,
        all following arguments are aded as text leabels.
        """
        window = ctk.CTkToplevel(self)
        err_text: str = ""
        for arg in args:
            if args.index(arg) == 0:
                window.title(arg)
            else:
                err_text += str(arg) + "\n"
        err_label = ctk.CTkLabel(window, text=err_text)
        err_label.pack(padx=10, pady=(10, 5))
        err_btn = ctk.CTkButton(window,
                                text="OK",
                                fg_color="firebrick1",
                                hover_color="firebrick3",
                                command=window.destroy
                                )
        err_btn.pack(padx=10, pady=10)


def main():
    """Main  function"""
    auto_delete = AutoDeleteApp()
    auto_delete.mainloop()


if __name__ == "__main__":
    main()
