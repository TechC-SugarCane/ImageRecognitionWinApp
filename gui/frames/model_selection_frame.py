from glob import glob
from typing import Tuple
import os
from pathlib import Path
import customtkinter
from utils.constants.crop import CropType
from utils.constants.model import ModelType


class ModelSelectionFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, crop: CropType, inference_model: ModelType) -> None:
        """モデルの選択画面"""
        super().__init__(master=master)

        self.optionmenu_var = customtkinter.StringVar()

        self.models_name, self.models = self.get_models(crop, inference_model)

        self.optionmenu_var = customtkinter.StringVar(value=self.models_name[0])

        self.optionmenu = customtkinter.CTkOptionMenu(
            self, values=self.models_name, command=self.optionmenu_callback, variable=self.optionmenu_var
        )

        self.optionmenu.grid(row=0, column=0, padx=10, pady=10)

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def get_models(self, crop: CropType, inference_model: ModelType) -> Tuple[list[str], dict[str, str]]:
        """モデルを取得"""
        models_root_path = f"models/{inference_model.lower()}-models/{crop}"

        if not os.path.exists(models_root_path):
            message = (
                f"Model directory not found: {models_root_path}. Please see models/README.md and download the model."  # noqa
            )
            raise FileNotFoundError(message)

        models_path = glob(f"{models_root_path}/*.onnx")

        if models_path == []:
            message = (
                f"ONNX model file not found: {models_root_path}. Please see models/README.md and download the model."  # noqa
            )
            raise FileNotFoundError(message)

        models_name = [Path(model_path).stem for model_path in models_path]
        models = {model_name: model_path for model_name, model_path in zip(models_name, models_path, strict=True)}

        return models_name, models

    def get_model_name(self) -> str:
        return self.optionmenu_var.get()

    def get_model_path(self) -> str:
        """選択されたモデルを取得"""
        return self.models[self.optionmenu_var.get()]

    def set_model_path(self, value: str) -> None:
        self.optionmenu_var.set(value)

    def set_model_selection(self, crop: CropType, model: ModelType) -> None:
        """モデル選択"""
        self.models_name, self.models = self.get_models(crop, model)
        self.optionmenu.configure(values=self.models_name)
