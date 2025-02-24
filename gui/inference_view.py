from typing import Callable

import customtkinter
from serial import Serial

from gui.view_process import ViewProcess


class InferenceView(customtkinter.CTkFrame):
    def __init__(
        self, master: customtkinter.CTk, controller, params: dict, ser: Serial, back_callback: Callable
    ) -> None:
        """
        推論画面のview
        :param master    : 親クラス
        :param controller: コントローラ
        :param params    : 推論画面に渡すパラメータ
        """
        super().__init__(master=master)

        self.controller = controller
        self.back_callback = back_callback
        self.ser = ser
        self.params = params

        self.is_test = params["is_test"]
        self.is_serial = params["is_serial"]
        self.inference_model_value = params["inference_model_value"]
        self.crops_value = params["crops_value"]
        self.model_path = params["model_path"]
        self.left_camera_index = params["camera_index_left"]
        self.right_camera_index = params["camera_index_right"]

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        ウィジェットの作成

        :param params       : 推論画面に渡すパラメータ
        :param back_callback: 前の画面に戻る関数
        """
        # 前の画面に戻るボタン
        self.back_button = customtkinter.CTkButton(
            master=self,
            text="戻る",
            command=lambda: self.back_callback(self.params),
            width=70,
            text_color="black",
            fg_color=("gray", "white"),
            hover_color=("lightgray", "white"),
        )
        # 左上に配置
        self.back_button.pack(side="bottom", anchor="center", fill="both")

        # 左の画面設定
        self.left_view_process = ViewProcess(
            master=self,
            is_serial=self.is_serial,
            is_test=self.is_test,
            ser=self.ser,
            inference_model_value=self.inference_model_value,
            crops_value=self.crops_value,
            model_path=self.model_path,
            camera_index=self.left_camera_index,
        )
        self.left_view_process.pack(side="left", expand=True, fill="both")

        # 右の画面設定
        self.right_view_process = ViewProcess(
            master=self,
            is_serial=self.is_serial,
            is_test=self.is_test,
            ser=self.ser,
            inference_model_value=self.inference_model_value,
            crops_value=self.crops_value,
            model_path=self.model_path,
            camera_index=self.right_camera_index,
        )
        self.right_view_process.pack(side="right", expand=True, fill="both")
