import customtkinter
from glob import glob
from pathlib import Path

from function.const.crop import CROP_NAME_LIST, CropType
from function.const.model import MODEL_NAME_LIST, ModelType


class CropsFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, command: callable) -> None:
        """作物の選択画面"""
        super().__init__(master=master)

        self.command = command

        self.selected_rbtn = customtkinter.StringVar(value="sugarcane")

        self.set_crop_rbtn(CROP_NAME_LIST)

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
                command=self.command,
            )
            crop_rbtn.grid(row=idx, column=0, padx=10, pady=10)


class InferenceModelFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, command: callable) -> None:
        """推論モデルの選択画面"""
        super().__init__(master=master)

        self.command = command

        self.selected_rbtn = customtkinter.StringVar(value="YOLOv9")

        self.set_model_rbtn(MODEL_NAME_LIST)

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
                command=self.command,
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


class ModelSelectionFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, crop: CropType, inference_model: ModelType) -> None:
        """モデルの選択画面"""
        super().__init__(master=master)

        self.optionmenu_var = customtkinter.StringVar(value="YOLOv9s")

        models_path = f"models/{inference_model.lower()}-models/{crop}"

        models_path = glob(f"{models_path}/*.onnx")
        models_name = [Path(model_path).stem for model_path in models_path]

        self.models = {model_name: model_path for model_name, model_path in zip(models_name, models_path, strict=True)}

        optionmenu = customtkinter.CTkOptionMenu(
            self, values=models_name, command=self.optionmenu_callback, variable=self.optionmenu_var
        )

        optionmenu.grid(row=0, column=0, padx=10, pady=10)

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def get_model_path(self) -> str:
        """選択されたモデルを取得"""
        return self.models[self.optionmenu_var.get()]
