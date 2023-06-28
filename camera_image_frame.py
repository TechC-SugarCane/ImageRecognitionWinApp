import tkinter as tk
from tkinter import Tk, ttk

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageTk  # 画像データ用


class ImageRecognition(ttk.Frame):
    def __init__(self, master: Tk | None = None):
        super().__init__(master)

        if master is not None:
            self.master: Tk = master

            # ウィンドウのサイズ
            window_width: int = self.master.winfo_width()
            print(f"ウィンドウ 幅：{window_width}")
            window_height: int = self.master.winfo_height()
            print(f"ウィンドウ 高さ：{window_height}")

            # キャンバスのサイズ
            canvas_width: int = window_width // 2
            canvas_height: int = window_height

            self.canvas: tk.Canvas = tk.Canvas(
                self.master, width=canvas_width, height=canvas_height
            )
            self.canvas.pack(side="left", expand=True, fill="both")

            # カメラを起動する
            self.capture: cv2.VideoCapture = cv2.VideoCapture(0)

            # self.display_image()
            self.display_id: str = ""

    def display_image(self):
        """画像をCanvasに表示する"""

        # フレーム画像を取得
        is_success, frame = self.capture.read()
        # print(frame)

        # BGRからRGBへ変換
        cv_image: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # NumpyのndarrayからPillowのImageへ変換
        pil_image = Image.fromarray(cv_image)

        # Canvasのサイズを取得
        canvas_width: int = self.canvas.winfo_width()
        canvas_height: int = self.canvas.winfo_height()

        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        # PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.create_image(
            canvas_width / 2,  # 画像表示位置(Canvasの中心)
            canvas_height / 2,
            image=self.photo_image,  # 表示画像データ
        )

        # display_image()を10msec後に実行する
        self.display_id = self.after(10, self.display_image)

    def display_stop(self):
        """描画を停止する"""
        self.after_cancel(self.display_id)
        self.display_id = ""

    def display_restart(self):
        """描画を再開する"""
        self.display_image()

    def display_exit(self):
        """アプリを終了する"""


"""
カメラ起動する時、明らかに処理が重いな

TODO 停止ボタンを押したらカメラを止める after_cancel
TODO 再開ボタンを押したらdisplay_imageを実行
TODO 終了ボタンを押したら、アプリ終了 setup画面に遷移でも良いかも
"""
