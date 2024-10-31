import customtkinter


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
