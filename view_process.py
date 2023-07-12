import tkinter as tk
from tkinter import Tk, ttk

from image_recognition import ImageRecognition


class ViewProcess(tk.Frame):
    def __init__(self, master, crops_value, inference_model_value) -> None:
        super().__init__(master)

        if master is not None:
            self.master: Tk = master
            # ウィンドウタイトル
            self.master.title("view process")
            # ウィンドウサイズ
            self.master.geometry("1000x800")

            self.image_recognition: ImageRecognition = ImageRecognition(self.master, model_type=inference_model_value, model_name=crops_value)
            self.image_recognition.pack(side="top", fill="both", expand=True)
            self.image_recognition.display_image()

            # ボタンフレーム
            button_frame = ttk.Frame(self.master)
            button_frame.pack(side="bottom", pady=10)

            # 停止ボタン
            self.stop_button: ttk.Button = ttk.Button(
                button_frame,
                text="停止",
                command=lambda: [
                    self.image_recognition.display_stop(),
                    self.toggle_stop_button_state(),
                ],
                state="normal",
            )
            self.stop_button.pack(side="left", padx=10)
            # 再開ボタン
            self.restart_button: ttk.Button = ttk.Button(
                button_frame,
                text="再開",
                command=lambda: [
                    self.image_recognition.display_restart(),
                    self.toggle_restart_button_state(),
                ],
                state="normal",
            )
            self.restart_button.pack(side="left", padx=10)
            # 終了
            self.exit_button: ttk.Button = ttk.Button(
                button_frame, text="終了", command=self.image_recognition.display_exit
            )
            self.exit_button.pack(side="left", padx=10)

    # ! 下記の処理はバグっている
    # ! 意図した挙動の時と、そうでない時の違いが分からん
    # ? 設計として良くないな
    def toggle_stop_button_state(self) -> None:
        """停止ボタンの有効/無効を切り替える"""

        # ! このt \printを消すと、意図した挙動にならない ???
        print(self.stop_button["state"])

        if self.stop_button["state"] == "normal":
            self.stop_button["state"] = "disable"
            print("True")
        elif self.stop_button["state"] == "disable":
            self.stop_button["state"] = "normal"
            print("False")
        print(self.stop_button["state"])

        # * 停止ボタンが押されたときに、再開ボタンが無効なら有効にする
        if self.restart_button["state"] == "disable":
            self.toggle_restart_button_state()

    def toggle_restart_button_state(self) -> None:
        """
        再開ボタンの有効/無効を切り替える
        停止ボタンを有効にする
        """

        print(self.restart_button["state"])

        if self.restart_button["state"] == "normal":
            self.restart_button["state"] = "disable"
        elif self.restart_button["state"] == "disable":
            self.restart_button["state"] = "normal"

        # * 再開ボタンが押されたときに、停止ボタンが無効なら有効にする
        if self.stop_button["state"] == "disable":
            self.toggle_stop_button_state()


"""
! 処理激重
停止は問題なさそう
再開ボタンを連打すると挙動がヤバイ
display_imageが複数実行されているかも
描画されているときは、再開ボタンを押せないようにする
描画が停止しているときは、停止ボタンは押せない and 再開ボタンは押せる
"""
