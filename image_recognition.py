import tkinter as tk
from tkinter import Tk, ttk

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageTk  # 画像データ用

from function.infer import Model


class ImageRecognition(ttk.Frame):
    """カメラ映像と認識後画像を扱うカメラ"""

    def __init__(self, master, model_type, model_name):
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

            # カメラ映像のキャンバス
            self.camera_image_canvas: tk.Canvas = tk.Canvas(
                self.master, width=canvas_width, height=canvas_height
            )
            self.camera_image_canvas.pack(side="left", expand=True, fill="both")

            # 認識後画像のキャンバス
            self.infer_image_canvas: tk.Canvas = tk.Canvas(
                self.master, width=canvas_width, height=canvas_height
            )
            self.infer_image_canvas.pack(side="right", expand=True, fill="both")

            # カメラを起動する
            self.capture: cv2.VideoCapture = cv2.VideoCapture(0)

            self.display_id: str = ""

            # self.model: Model = Model("Yolo v7", "sugarcane", "CPUExecutionProvider")
            self.model: Model = Model(
                model_type=model_type,
                model_name=model_name,
                providers="CPUExecutionProvider",
            )

            # FPSを表示するラベル
            self.fps_label = tk.Label(self.master, text="")  # type: ignore
            self.fps_label.pack()

    def display_image(self):
        """画像をCanvasに表示する"""

        # フレーム画像を取得
        is_success, frame = self.capture.read()

        infer_frame, fps = self.model.infer(frame)

        # FPSのテキストを更新
        self.fps_label.config(text=fps)
        self.fps_label.update()

        # BGRからRGBへ変換
        cv_image2: np.ndarray = cv2.cvtColor(infer_frame, cv2.COLOR_BGR2RGB)

        # NumpyのndarrayからPillowのImageへ変換
        pil_image2 = Image.fromarray(cv_image2)

        # Canvasのサイズを取得
        canvas_width: int = self.camera_image_canvas.winfo_width()
        canvas_height: int = self.camera_image_canvas.winfo_height()

        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image2 = ImageOps.pad(pil_image2, (canvas_width, canvas_height))

        # PIL.ImageからPhotoImageへ変換する
        self.photo_image2 = ImageTk.PhotoImage(image=pil_image2)

        # 認識後画像のcanvasに画像を描画
        self.infer_image_canvas.create_image(
            canvas_width / 2,
            canvas_height / 2,
            image=self.photo_image2,
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
カメラ映像のcanvasを用意する
camera_image_canvas
認識後画像のcanvasを用意する
infer_image_canvas

カメラ映像のframeをModel.inferに渡す
"""
