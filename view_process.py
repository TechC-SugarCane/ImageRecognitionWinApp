import customtkinter

from image_recognition import ImageRecognition


class ViewProcess(customtkinter.CTkFrame):
    def __init__(self, master, crops_value, inference_model_value):
        super().__init__(master=master)

        self.image_recognition = ImageRecognition(
            master=self, model_type=inference_model_value, model_name=crops_value
        )  # type: ignore
        self.image_recognition.pack(side="top", fill="both", expand="True")
        self.image_recognition.display_image()

        button_frame = customtkinter.CTkFrame(master=self)
        button_frame.pack(side="bottom", pady=10)

        self.stop_button = customtkinter.CTkButton(
            master=button_frame,
            text="停止",
            command=lambda: [
                self.image_recognition.display_stop(),
                self.toggle_stop_button_state(),
            ],  # type: ignore
            state="normal",
        )
        self.stop_button.pack(side="left", padx=10)

        self.restart_button = customtkinter.CTkButton(
            master=button_frame,
            text="再開",
            command=lambda: [
                self.image_recognition.display_restart(),
                self.toggle_restart_button_state(),
            ],  # type: ignore
            state="normal",
        )
        self.restart_button.pack(side="left", padx=10)

        self.exit_button = customtkinter.CTkButton(
            master=button_frame, text="終了", command=self.image_recognition.display_exit
        )
        self.exit_button.pack(side="left", padx=10)

    # ! 下記の処理はバグっている
    # ! 意図した挙動の時と、そうでない時の違いが分からん
    # ? 設計として良くないな
    def toggle_stop_button_state(self) -> None:
        """停止ボタンの有効/無効を切り替える"""

        # ! このt \printを消すと、意図した挙動にならない ???
        print(self.stop_button["state"])

        if self.stop_button["state"] == "normal":
            self.stop_button["state"] = "disable"
            print("True")
        elif self.stop_button["state"] == "disable":
            self.stop_button["state"] = "normal"
            print("False")
        print(self.stop_button["state"])

        # * 停止ボタンが押されたときに、再開ボタンが無効なら有効にする
        if self.restart_button["state"] == "disable":
            self.toggle_restart_button_state()

    def toggle_restart_button_state(self) -> None:
        """
        再開ボタンの有効/無効を切り替える
        停止ボタンを有効にする
        """

        print(self.restart_button["state"])

        if self.restart_button["state"] == "normal":
            self.restart_button["state"] = "disable"
        elif self.restart_button["state"] == "disable":
            self.restart_button["state"] = "normal"

        # * 再開ボタンが押されたときに、停止ボタンが無効なら有効にする
        if self.stop_button["state"] == "disable":
            self.toggle_stop_button_state()
