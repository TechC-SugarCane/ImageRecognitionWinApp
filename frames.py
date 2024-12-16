from typing import Literal

import customtkinter

from function.const.model import ModelType
from function.const.crop import CropType


class CropsFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """作物の選択画面"""
        super().__init__(master=master)

        self.selected_rbtn = customtkinter.StringVar()

        self.set_crop_rbtn(list(CropType.__args__))

    def get_selected_rbtn_value(self) -> CropType:
        """選択された作物を取得"""
        return self.selected_rbtn.get()

    def set_crop_rbtn(self, crop_types: list[CropType]) -> None:
        """選択された作物をセット"""

        for idx, crop_type in enumerate(crop_types):
            crop_rbtn = customtkinter.CTkRadioButton(
                master=self,
                text=crop_type,
                variable=self.selected_rbtn,
                value=crop_type,
            )
            crop_rbtn.grid(row=idx, column=0, padx=10, pady=10)


class InferenceModelFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """推論モデルの選択画面"""
        super().__init__(master=master)

        self.selected_rbtn = customtkinter.StringVar()

        self.set_model_rbtn(list(ModelType.__args__))

    def get_selected_rbtn_value(self) -> ModelType:
        """選択された推論モデルを取得"""
        return self.selected_rbtn.get()

    def set_model_rbtn(self, model_types: list[ModelType]) -> None:
        """選択された推論モデルをセット"""

        for idx, model_type in enumerate(model_types):
            model_rbtn = customtkinter.CTkRadioButton(
                master=self,
                text=model_type,
                variable=self.selected_rbtn,
                value=model_type,
            )
            model_rbtn.grid(row=idx, column=0, padx=10, pady=10)


class OptionFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """オプションの選択画面"""
        super().__init__(master=master)

        self.is_test = customtkinter.BooleanVar()
        self.is_serial = customtkinter.BooleanVar()

        test_mode_toggle = customtkinter.CTkSwitch(
            master=self,
            text="テストモード(動画)",
            variable=self.is_test,
        )
        test_mode_toggle.grid(row=0, column=0, padx=10, pady=10)

        serial_mode_toggle = customtkinter.CTkSwitch(
            master=self,
            text="シリアル通信モード",
            variable=self.is_serial,
        )
        serial_mode_toggle.grid(row=1, column=0, padx=10, pady=10)

    def get_is_test(self) -> bool:
        """選択されたテストモードのモードを取得"""
        return self.is_test.get()

    def get_is_serial(self) -> bool:
        """選択されたシリアル通信のモードを取得"""
        return self.is_serial.get()
