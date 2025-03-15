from glob import glob
import random

import customtkinter

from gui.frames import CropsFrame, InferenceModelFrame, ModelSelectionFrame, OptionFrame
from utils.constants.crop import CropType
from utils.constants.model import ModelType


# 読み込む動画パスを乱数で指定
def get_video_path(crop_type: CropType) -> str:
    """
    ランダムに動画を選択

    :param crop_type: 作物の種類
    :return video_path: 動画のパス
    """
    video_list = glob(f"video/tests/{crop_type}/*.mp4")
    if len(video_list) == 0:
        raise FileNotFoundError(
            f"テストに使用できる動画が存在しません: video/tests/{crop_type}/\n`video/README.md`に従って動画をダウンロードしてください"  # noqa
        )
    return random.choice(video_list)


class SetupView(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk, controller, execute_callback) -> None:
        """
        画面のセットアップを行う
        """
        super().__init__(master=master)

        self.controller = controller

        self.execute_callback = execute_callback

        self.create_widgets()

    def create_widgets(self) -> None:
        # 作物のFrameを表示
        self.crops_frame = CropsFrame(self, self.model_selection)
        self.crops_frame.pack(side="left", padx=30, pady=10, anchor="center")

        # 推論モデルのFrameを表示
        self.inference_model_frame = InferenceModelFrame(self, self.model_selection)
        self.inference_model_frame.pack(side="left", padx=30, pady=10, anchor="center")

        # オプションのFrameを表示
        self.option_frame = OptionFrame(self)
        self.option_frame.pack(side="left", padx=30, pady=10, anchor="center")

        # モデル選択のFrameを表示
        self.set_model_selection(
            self.crops_frame.get_selected_rbtn_value(), self.inference_model_frame.get_selected_rbtn_value()
        )

        # 実行ボタン
        self.execute_button = customtkinter.CTkButton(
            master=self, text="推論画面へ", fg_color="#1c961a", hover_color="#42a340", command=self.on_execute
        )
        self.execute_button.pack(side="right", padx=20, pady=10, anchor="center")

    def model_selection(self) -> None:
        """
        モデル選択
        """
        self.model_selection_frame.destroy()
        self.set_model_selection(
            self.crops_frame.get_selected_rbtn_value(), self.inference_model_frame.get_selected_rbtn_value()
        )

    def set_model_selection(self, crop: CropType, model: ModelType) -> None:
        """
        モデル選択
        """
        self.model_selection_frame = ModelSelectionFrame(self, crop, model)
        self.model_selection_frame.pack(side="left", padx=30, pady=10, anchor="center")

    def on_execute(self) -> None:
        """画面遷移"""
        crop_value = self.crops_frame.get_selected_rbtn_value()
        inference_model_value = self.inference_model_frame.get_selected_rbtn_value()
        is_test = self.option_frame.get_is_test()
        is_serial = self.option_frame.get_is_serial()
        model_name = self.model_selection_frame.get_model_name()
        model_path = self.model_selection_frame.get_model_path()
        camera_index_left = 0 if not is_test else get_video_path(crop_value)
        camera_index_right = 1 if not is_test else get_video_path(crop_value)

        params = {
            "crops_value": crop_value,
            "inference_model_value": inference_model_value,
            "is_serial": is_serial,
            "is_test": is_test,
            "model_path": model_path,
            "model_name": model_name,
            "camera_index_left": camera_index_left,
            "camera_index_right": camera_index_right,
        }

        self.execute_callback(params)

    def set_params(self, params: dict) -> None:
        """
        パラメータをセット
        :param params: パラメータ
        """

        self.crops_frame.set_rbtn_value(params["crops_value"])
        self.inference_model_frame.set_rbtn_value(params["inference_model_value"])
        self.option_frame.set_is_serial(params["is_serial"])
        self.option_frame.set_is_test(params["is_test"])
        self.model_selection_frame.set_model_selection(params["crops_value"], params["inference_model_value"])
        self.model_selection_frame.set_model_name(params["model_name"])

    def create_modal_windows(self, master: customtkinter.CTk, title: str, message: str) -> None:
        """
        モーダルウィンドウを作成する
        :param title: タイトル
        :param message: 表示するメッセージ
        """
        modal_window = customtkinter.CTkToplevel(master)
        modal_window.geometry(geometry_string="400x300")
        modal_window.title(title)
        modal_window.bell()

        text_label = customtkinter.CTkLabel(master=modal_window, text=message)
        text_label.pack(padx=10, pady=10)

        modal_window.grab_set()
        modal_window.focus_set()
        modal_window.transient(master=master)

        master.wait_window(window=modal_window)
