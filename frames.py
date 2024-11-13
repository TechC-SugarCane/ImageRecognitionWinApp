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
            command=self.get_selected_rbtn_value,
        )
        pineapple_rbtn.grid(row=0, column=0, padx=10, pady=10)

        sugarcane_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="サトウキビ",
            variable=self.selected_rbtn,
            value="sugarcane",
            command=self.get_selected_rbtn_value,
        )
        sugarcane_rbtn.grid(row=1, column=0, padx=10, pady=10)

    def get_selected_rbtn_value(self) -> str:
        """選択された作物を取得"""
        crops = self.selected_rbtn.get()
        print("Selected crops: ", crops)
        return crops



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
            command=self.get_selected_rbtn_value,
        )
        yolov7_rbtn.grid(row=0, column=0, padx=10, pady=10)

        yolov10_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="YOLOv10",
            variable=self.selected_rbtn,
            value="YOLOv10",
            command=self.get_selected_rbtn_value,
        )
        yolov10_rbtn.grid(row=2, column=0, padx=10, pady=10)

    def get_selected_rbtn_value(self) -> str:
        """選択された推論モデルを取得"""
        inference_model = self.selected_rbtn.get()
        print("Selected inference model: ", inference_model)
        return inference_model


class OptionFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """オプションの選択画面"""
        super().__init__(master=master)

        self.is_serial = customtkinter.BooleanVar()

        serial_mode_toggle = customtkinter.CTkSwitch(
            master=self,
            text="シリアル通信モード",
            variable=self.is_serial,
            command=self.get_is_serial,
        )
        serial_mode_toggle.grid(row=0, column=0, padx=10, pady=10)

        self.is_test = customtkinter.BooleanVar()

        test_mode_toggle = customtkinter.CTkSwitch(
            master=self,
            text="テストモード(動画)",
            variable=self.is_test,
            command=self.get_is_test,
        )
        test_mode_toggle.grid(row=1, column=0, padx=10, pady=10)

    def get_is_serial(self) -> bool:
        """選択されたシリアル通信のモードを取得"""
        is_serial = self.is_serial.get()
        print("Selected serial mode: ", is_serial)
        return is_serial

    def get_is_test(self) -> bool:
        """選択されたテストモードのモードを取得"""
        is_test = self.is_test.get()
        print("Selected test mode: ", is_test)
        return is_test
