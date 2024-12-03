from typing import Literal

import customtkinter


class CropsFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """作物の選択画面"""
        super().__init__(master=master)

        self.selected_rbtn = customtkinter.StringVar()

        pineapple_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="パイナップル",
            variable=self.selected_rbtn,
            value="pineapple",
        )
        pineapple_rbtn.grid(row=0, column=0, padx=10, pady=10)

        sugarcane_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="サトウキビ",
            variable=self.selected_rbtn,
            value="sugarcane",
        )
        sugarcane_rbtn.grid(row=1, column=0, padx=10, pady=10)

    def get_selected_rbtn_value(self) -> Literal["pineapple", "sugarcane"]:
        """選択された作物を取得"""
        return self.selected_rbtn.get()


class InferenceModelFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """推論モデルの選択画面"""
        super().__init__(master=master)

        self.selected_rbtn = customtkinter.StringVar()

        yolov7_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="YOLOv7",
            variable=self.selected_rbtn,
            value="YOLOv7",
        )
        yolov7_rbtn.grid(row=0, column=0, padx=10, pady=10)

        yolov10_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="YOLOv10",
            variable=self.selected_rbtn,
            value="YOLOv10",
        )
        yolov10_rbtn.grid(row=2, column=0, padx=10, pady=10)

    def get_selected_rbtn_value(self) -> Literal["YOLOv7", "YOLOv10"]:
        """選択された推論モデルを取得"""
        return self.selected_rbtn.get()


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
