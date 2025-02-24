import customtkinter


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

    def set_is_test(self, value: bool) -> None:
        self.is_test.set(value)

    def get_is_serial(self) -> bool:
        """選択されたシリアル通信のモードを取得"""
        return self.is_serial.get()

    def set_is_serial(self, value: bool) -> None:
        self.is_serial.set(value)
