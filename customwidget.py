import customtkinter as ctk
from typing import Union, Callable


class CtkSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 min_value: int = 0,
                 max_value: int = 100,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 default: int = 0,
                 **kwargs):
        """
        A custom spinbox widget for the customtkinter module.

        Parameters
        ----------
        width : int, optional
            Width of the spinbox widget, by default 100
        height : int, optional
            Height of the spinbox widget, by default 32
        min_value : int, optional
            smallest possible value, default 0
        max_value : int, optional
            highest possible value, default 100
        step_size : [int, float], optional
            Step size of the increase or decrease , by default 1
        command : Callable, optional
            Commando that is executed when a button is pressed, by default None
        default : int, optional
            default start value of the spinbox, default 0
        """
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.min_value = min_value
        self.max_value = max_value

        self.configure(fg_color=("gray78", "gray28"))    # set color for frame

        # value entry
        self.entry = ctk.CTkEntry(self,
                                  width=width-(2 * height),
                                  height=height,
                                  border_width=0)
        self.entry.grid(row=0,
                        column=0, rowspan=2,
                        padx=1, pady=1,
                        sticky="ew")

        # increase button
        self.increase_btn = ctk.CTkButton(self,
                                          text="ᐱ",
                                          border_spacing=0.2,
                                          font=("Arial", (height * 0.5)),
                                          width=height * 0.2,
                                          height=height * 0.53,
                                          command=self.increase_btn_callback)
        self.increase_btn.grid(row=0, column=1, padx=(2, 0), pady=1)

        # decrease bttn
        self.decrease_btn = ctk.CTkButton(self,
                                          text="ᐯ",
                                          font=("Arial", (height * 0.5)),
                                          width=height * 0.2,
                                          height=height * 0.53,
                                          command=self.decrease_btn_callback)
        self.decrease_btn.grid(row=1, column=1, padx=(2, 0), pady=1)

        # Default entry value
        self.entry.insert(0, str(default))

    def increase_btn_callback(self):
        """
        increases the spinbox entry by step size
        """
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get())
            if value >= self.max_value:
                return
            else:
                value += self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def decrease_btn_callback(self):
        """
        decreases the spinbox entry by step size
        """
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get())
            if value <= self.min_value:
                return
            else:
                value -= self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)


if __name__ == "__main__":
    raise NotImplementedError(
        "This module is for creating and importing user defined customtkinter "
        "widgets only. A self call is not intended."
        )
