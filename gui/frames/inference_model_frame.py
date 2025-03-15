from typing import Callable

import customtkinter

from utils.constants.model import MODEL_NAME_LIST, ModelType


class InferenceModelFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, command: Callable) -> None:
        """推論モデルの選択画面"""
        super().__init__(master=master)

        self.command = command

        self.selected_rbtn = customtkinter.StringVar(value=MODEL_NAME_LIST[0])

        self.set_model_rbtn(MODEL_NAME_LIST)

    def get_selected_rbtn_value(self) -> ModelType:
        """選択された推論モデルを取得"""
        return self.selected_rbtn.get()

    def set_rbtn_value(self, value: str) -> None:
        self.selected_rbtn.set(value)

    def set_model_rbtn(self, model_types: list[ModelType]) -> None:
        """選択された推論モデルをセット"""

        for idx, model_type in enumerate(model_types):
            model_rbtn = customtkinter.CTkRadioButton(
                master=self,
                text=model_type,
                variable=self.selected_rbtn,
                value=model_type,
                command=self.command,
            )
            model_rbtn.grid(row=idx, column=0, padx=10, pady=10)
