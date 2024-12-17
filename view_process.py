import customtkinter

from function.const.crop import CropType
from function.const.model import ModelType
from image_recognition import ImageRecognition


class ViewProcess(customtkinter.CTkFrame):
    def __init__(
        self,
        master: customtkinter.CTkFrame,
        is_serial: bool,
        is_test: bool,
        inference_model_value: ModelType,
        crops_value: CropType,
        model_path: str,
        camera_index: int | str,
    ) -> None:
        """
        描画処理を行う
        :param master                : 親クラス
        :param is_serial             : シリアル通信モードかどうか
        :param is_test               : テストモードかどうか
        :param inference_model_value : 使用するモデルのバージョン
        :param crops_value           : 推論する作物の名前
        :param model_path            : モデルのパス
        :param camera_index          : 使用するカメラのインデックス or 動画のパス
        """
        super().__init__(master=master)

        self.image_recognition = ImageRecognition(
            master=self,
            is_serial=is_serial,
            is_test=is_test,
            model_type=inference_model_value,
            model_name=crops_value,
            model_path=model_path,
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
            fg_color="#b81f1a",
            hover_color="#DE433E",
        )
        self.stop_button.pack(side="left", padx=10, pady=10)

        self.restart_button = customtkinter.CTkButton(
            master=button_frame,
            text="再開",
            command=self.image_recognition.display_restart,
            state="normal",
            fg_color="#1c961a",
            hover_color="#42a340",
        )

        self.restart_button.pack(side="left", padx=10, pady=10)
