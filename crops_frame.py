import customtkinter


# 作物、推論モデルの選択肢フォーム
class CropsFrame(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, borderwidth=5, relief="ridge", width=200, height=100)

        # Frameサイズを固定
        self.propagate(False)

        if master is not None:
            self.master: customtkinter = master

            # ラジオボタンの値を扱う
            self.selected_rbtn: customtkinter.CTk.StringVar = customtkinter.CTk.StringVar()

        pineapple_rbtn = customtkinter.CTkComboBox(
            self,
            text="パイナップル",
            variable=self.selected_rbtn,
            value="パイナップル",
            command=self.show_selected_rbtn_value,
        )
        pineapple_rbtn.grid(row=0, column=0, padx=10, pady=10)

        sugarcane_rbtn = customtkinter.CTk.Radiobutton(
            self,
            text="サトウキビ",
            variable=self.selected_rbtn,
            value="サトウキビ",
            command=self.show_selected_rbtn_value,
        )
        sugarcane_rbtn.grid(row=1, column=0, padx=10, pady=10)

    def show_selected_rbtn_value(self) -> str:
        print(self.selected_rbtn.get())
        return self.selected_rbtn.get()


"""

"""
