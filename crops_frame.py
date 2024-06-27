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
