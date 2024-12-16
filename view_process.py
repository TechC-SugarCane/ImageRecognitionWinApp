from typing import Literal

import customtkinter

from function.const.model import ModelType
from function.const.crop import CropType
from image_recognition import ImageRecognition


class ViewProcess(customtkinter.CTkFrame):
    def __init__(
        self,
        master: customtkinter.CTkFrame,
        is_serial: bool,
        is_test: bool,
        inference_model_value: ModelType,
        crops_value: CropType,
        camera_index: int | str,
    ) -> None:
        """
        描画処理を行う
        :param master                : 親クラス
        :param is_serial             : シリアル通信モードかどうか
        :param is_test               : テストモードかどうか
        :param inference_model_value : 使用するモデルのバージョン
        :param crops_value           : 推論する作物の名前
        :param camera_index          : 使用するカメラのインデックス or 動画のパス
        """
        super().__init__(master=master)

        self.image_recognition = ImageRecognition(
            master=self,
            is_serial=is_serial,
            is_test=is_test,
            model_type=inference_model_value,
            model_name=crops_value,
            camera_index=camera_index,
        )
        self.image_recognition.pack(side="top", fill="both", expand="True")

        button_frame = customtkinter.CTkFrame(master=self)
        button_frame.pack(side="bottom", pady=10)

        self.stop_button = customtkinter.CTkButton(
            master=button_frame,
            text="停止",
            command=self.image_recognition.display_stop,
            state="normal",
        )
        self.stop_button.pack(side="left", padx=10)

        self.restart_button = customtkinter.CTkButton(
            master=button_frame,
            text="再開",
            command=self.image_recognition.display_restart,
            state="normal",
        )

        self.restart_button.pack(side="left", padx=10)
