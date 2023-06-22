import tkinter as tk
from tkinter import Tk, ttk


class CropsFrame(ttk.Frame):
    def __init__(self, master: Tk | None = None) -> None:
        super().__init__(master, borderwidth=5, relief="ridge", width=200, height=100)

        # Frameサイズを固定
        self.propagate(False)

        if master is not None:
            self.master: Tk = master

            # ラジオボタンの値を扱う
            self.selected_crops: tk.StringVar = tk.StringVar()

            pineapple_rbtn = ttk.Radiobutton(
                self,
                text="パイナップル",
                variable=self.selected_crops,
                value="パイナップル",
                command=self.show_selected_crops_value,
            )
            # pineapple_rbtn.pack()
            pineapple_rbtn.grid(row=0, column=0, padx=10, pady=10)

            sugarcane_rbtn = ttk.Radiobutton(
                self,
                text="サトウキビ",
                variable=self.selected_crops,
                value="サトウキビ",
                command=self.show_selected_crops_value,
            )
            # sugarcane_rbtn.pack()
            sugarcane_rbtn.grid(row=1, column=0, padx=10, pady=10)

    def show_selected_crops_value(self):
        print(self.selected_crops.get())

    def show_selected_inference_model_value(self):
        print(self.selected_crops.get())


"""

"""
