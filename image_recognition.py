from datetime import datetime

import customtkinter
import cv2
from PIL import Image, ImageOps, ImageTk  # 画像データ用

from function.const.crop import CropType, SUGARCANE_LABEL_LIST, PINEAPPLE_LABEL_LIST
from function.const.model import ModelType
from function.infer import Model


class ImageRecognition(customtkinter.CTkFrame):
    def __init__(
        self,
        master: customtkinter.CTkFrame,
        is_serial: bool,
        is_test: bool,
        model_type: ModelType,
        model_name: CropType,
        model_path: str,
        camera_index: int | str,
    ) -> None:
        """
        画像描画用のクラス
        :param master       : 親クラス
        :param is_serial    : シリアル通信モードかどうか
        :param is_test      : テストモードかどうか
        :param model_type   : 使用するモデルのバージョン
        :param model_name   : 使用するモデルの名前
        :param model_path   : モデルのパス
        :param camera_index : 使用するカメラのインデックス or 動画のパス
        """
        super().__init__(master=master)

        self.is_serial = is_serial
        self.is_test = is_test

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        canvas_width = window_width // 2
        canvas_height = window_height

        self.infer_image_canvas = customtkinter.CTkCanvas(master=self, width=canvas_width, height=canvas_height)  # type: ignore
        self.infer_image_canvas.pack(side="top", expand=True, fill="both")

        # TODO ここで二つのカメラの映像
        self.capture = cv2.VideoCapture(camera_index)  # type: ignore

        if not is_test:
            # 保存用の動画ファイル設定
            w = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # 大体決め打ちで10fps, 石垣島PCで推論する時のfpsと合わせる
            fps = 10.0
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_video_path = f"video/{now}.mp4"
            save_infer_video_path = f"video/{now}_infer.mp4"
            self.save_video = cv2.VideoWriter(save_video_path, fourcc, fps, (w, h))
            self.save_infer_video = cv2.VideoWriter(save_infer_video_path, fourcc, fps, (w, h))

        self.display_id = ""

        self.model = Model(
            model_type=model_type,
            model_name=model_name,
            model_path=model_path,
            labels=SUGARCANE_LABEL_LIST if model_name == "sugarcane" else PINEAPPLE_LABEL_LIST,
        )

        self.fps_label = customtkinter.CTkLabel(master=self, text="")
        self.fps_label.pack()

    def display_image(self) -> None:
        """画像を描画する"""
        is_success, frame = self.capture.read()

        if not self.is_test:
            self.save_video.write(frame)

        infer_frame, fps = self.model.infer(self.is_serial, frame)  # type: ignore

        if not self.is_test:
            self.save_infer_video.write(infer_frame)

        self.fps_label.configure(text=fps)
        self.fps_label.update()

        cv_image = cv2.cvtColor(src=infer_frame, code=cv2.COLOR_BGR2RGB)  # type: ignore
        pil_image = Image.fromarray(obj=cv_image)

        canvas_width = self.infer_image_canvas.winfo_width()
        canvas_height = self.infer_image_canvas.winfo_height()

        pil_image = ImageOps.pad(image=pil_image, size=(canvas_width, canvas_height))

        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        self.infer_image_canvas.create_image(
            canvas_width / 2,
            canvas_height / 2,
            image=self.photo_image,
        )

        self.display_id = self.after(ms=10, func=self.display_image)

    def display_stop(self) -> None:
        """描画を一時停止する"""
        self.after_cancel(id=self.display_id)
        self.display_id = ""

    def display_restart(self) -> None:
        """描画を再開する"""
        if not self.display_id:
            self.display_image()

    def destroy(self) -> None:
        """ウィンドウを閉じる"""
        self.capture.release()
        if not self.is_test:
            self.save_video.release()
            self.save_infer_video.release()
        super().destroy()
