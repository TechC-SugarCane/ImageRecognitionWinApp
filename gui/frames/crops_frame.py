import customtkinter

from typing import Callable

from utils.constants.crop import CROP_NAME_LIST, CropType

class CropsFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, command: Callable) -> None:
        """作物の選択画面"""
        super().__init__(master=master)

        self.command = command

        self.selected_rbtn = customtkinter.StringVar(value=CROP_NAME_LIST[0])

        self.set_crop_rbtn(CROP_NAME_LIST)

    def get_selected_rbtn_value(self) -> CropType:
        """選択された作物を取得"""
        return self.selected_rbtn.get()

    def set_rbtn_value(self, value: str) -> None:
        self.selected_rbtn.set(value)

    def set_crop_rbtn(self, crop_types: list[CropType]) -> None:
        """選択された作物をセット"""

        for idx, crop_type in enumerate(crop_types):
            crop_rbtn = customtkinter.CTkRadioButton(
                master=self,
                text=crop_type,
                variable=self.selected_rbtn,
                value=crop_type,
                command=self.command,
            )
            crop_rbtn.grid(row=idx, column=0, padx=10, pady=10)
