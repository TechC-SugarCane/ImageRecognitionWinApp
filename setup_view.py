from typing import Optional

import customtkinter
import serial

from frames import CropsFrame, InferenceModelFrame, ModelSelectionFrame, OptionFrame
from function.const.crop import CropType
from function.const.model import ModelType
from function.nozzle import close_serial_port, set_serial_port
from view_process import ViewProcess

VID = "0x0483"
PID = "0x5740"


class Setup(customtkinter.CTk):
    def __init__(self) -> None:
        """
        画面のセットアップを行う
        """
        super().__init__()

        self.ser: Optional[serial.Serial] = None

        # ウィンドウサイズ（幅x高さ）
        self.geometry(geometry_string="1000x800")

        self.set_setup_frame()

    def set_setup_frame(self) -> None:
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
            master=self, text="推論画面へ", fg_color="#1c961a", hover_color="#42a340", command=self.screen_transition
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

    def screen_transition(self) -> None:
        """画面遷移"""
        self.crops_value = self.crops_frame.get_selected_rbtn_value()
        self.inference_model_value = self.inference_model_frame.get_selected_rbtn_value()
        self.is_test = self.option_frame.get_is_test()
        self.is_serial = self.option_frame.get_is_serial()
        self.model_name = self.model_selection_frame.get_model_name()
        self.model_path = self.model_selection_frame.get_model_path()
        print("Selected crops: ", self.crops_value)
        print("Selected inference model: ", self.inference_model_value)
        print("Is test mode: ", self.is_test)
        print("Is serial mode: ", self.is_serial)
        print("Selected model: ", self.model_path)

        # 前の画面のframeを削除
        self.destroy_pre_frame()

        if self.is_serial:
            self.ser = set_serial_port(VID, PID)

        left_camera_index: str | int = 0
        right_camera_index: str | int = 1

        # テストモードの場合はカメラではなく動画を読み込む
        if self.is_test:
            left_camera_index = "video/tests/multi_data1.mp4"
            right_camera_index = "video/tests/multi_data2.mp4"

        # 前の画面に戻るボタン
        self.back_button = customtkinter.CTkButton(
            master=self,
            text="戻る",
            command=self.back_screen,
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
            camera_index=left_camera_index,
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
            camera_index=right_camera_index,
        )
        self.right_view_process.pack(side="right", expand=True, fill="both")

    def destroy_pre_frame(self) -> None:
        """前画面(フレーム)を削除"""
        self.crops_frame.destroy()
        self.inference_model_frame.destroy()
        self.execute_button.destroy()
        self.option_frame.destroy()
        self.model_selection_frame.destroy()

    def back_screen(self) -> None:
        """前の画面に戻る"""
        self.left_view_process.destroy()
        self.right_view_process.destroy()
        self.back_button.destroy()
        if self.is_serial:
            close_serial_port(self.ser)

        self.set_setup_frame()

        self.crops_frame.set_rbtn_value(self.crops_value)
        self.inference_model_frame.set_rbtn_value(self.inference_model_value)
        self.option_frame.set_is_serial(self.is_serial)
        self.option_frame.set_is_test(self.is_test)
        self.model_selection_frame.set_model_path(self.model_name)


if __name__ == "__main__":
    app = Setup()
    app.title(string="画像認識")

    app.mainloop()
