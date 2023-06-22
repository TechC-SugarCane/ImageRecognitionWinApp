import tkinter as tk
from tkinter import Tk, ttk


class InferenceModelFrame(ttk.Frame):
    def __init__(self, master: Tk | None = None) -> None:
        super().__init__(master, borderwidth=5, relief="ridge", width=200, height=100)

        # Frameサイズを固定
        self.propagate(False)

        if master is not None:
            self.master: Tk = master

            # ラジオボタンの値を扱う
            self.selected_rbtn: tk.StringVar = tk.StringVar()

            yolov7_rbtn = ttk.Radiobutton(
                self,
                text="Yolo v7",
                variable=self.selected_rbtn,
                value="Yolo v7",
                command=self.show_selected_rbtn_value,
            )
            yolov7_rbtn.grid(row=0, column=0, padx=10, pady=10)

            yolov8_rbtn = ttk.Radiobutton(
                self,
                text="Yolo v8",
                variable=self.selected_rbtn,
                value="Yolo v8",
                command=self.show_selected_rbtn_value,
            )
            yolov8_rbtn.grid(row=1, column=0, padx=10, pady=10)

            yolo_nas_rbtn = ttk.Radiobutton(
                self,
                text="Yolo NAS",
                variable=self.selected_rbtn,
                value="Yolo NAS",
                command=self.show_selected_rbtn_value,
            )
            yolo_nas_rbtn.grid(row=2, column=0, padx=10, pady=10)

    def show_selected_rbtn_value(self):
        print(self.selected_rbtn.get())
