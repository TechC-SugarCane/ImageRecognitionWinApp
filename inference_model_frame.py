import customtkinter


class InferenceModelFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame) -> None:
        """推論モデルの選択画面"""
        super().__init__(master=master)

        self.selected_rbtn = customtkinter.StringVar()

        yolov7_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="Yolo v7",
            variable=self.selected_rbtn,
            value="Yolo v7",
            command=self.get_selected_rbtn_value,
        )
        yolov7_rbtn.grid(row=0, column=0, padx=10, pady=10)

        yolov_nas_rbtn = customtkinter.CTkRadioButton(
            master=self,
            text="Yolo NAS",
            variable=self.selected_rbtn,
            value="Yolo NAS",
            command=self.get_selected_rbtn_value,
        )
        yolov_nas_rbtn.grid(row=2, column=0, padx=10, pady=10)

    def get_selected_rbtn_value(self) -> str:
        """選択された推論モデルを取得"""
        inference_model = self.selected_rbtn.get()
        print("Selected inference model: ", inference_model)
        return inference_model
