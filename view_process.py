import tkinter as tk
from tkinter import Tk, ttk

from image_recognition import ImageRecognition


class ViewProcess(tk.Frame):
    def __init__(self, master: Tk | None = None) -> None:
        super().__init__(master)

        if master is not None:
            self.master: Tk = master
            # ウィンドウタイトル
            self.master.title("view process")
            # ウィンドウサイズ
            self.master.geometry("1000x800")

            # 停止ボタン
            self.stop_button: ttk.Button = ttk.Button(self.master, text="停止")
            self.stop_button.pack()
            # 再開ボタン
            self.restart_button: ttk.Button = ttk.Button(self.master, text="再開")
            self.restart_button.pack()
            # 終了
            self.exit_button: ttk.Button = ttk.Button(self.master, text="終了")
            self.exit_button.pack()

            self.image_recognition: ImageRecognition = ImageRecognition(self.master)
            self.image_recognition.pack()
            self.image_recognition.display_image()
