import customtkinter

from image_recognition import ImageRecognition


class ViewProcess(customtkinter.CTkFrame):
    def __init__(self, master, crops_value, inference_model_value, camera_index):
        super().__init__(master=master)

        self.image_recognition = ImageRecognition(
            master=self, model_type=inference_model_value, model_name=crops_value, camera_index=camera_index
        )
        self.image_recognition.pack(side="top", fill="both", expand="True")

        button_frame = customtkinter.CTkFrame(master=self)
        button_frame.pack(side="bottom", pady=10)

        self.stop_button = customtkinter.CTkButton(
            master=button_frame,
            text="停止",
            command=self.image_recognition.display_stop,
            state="normal",
        )
        self.stop_button.pack(side="left", padx=10)

        self.restart_button = customtkinter.CTkButton(
            master=button_frame,
            text="再開",
            command=self.image_recognition.display_restart,
            state="normal",
        )

        self.restart_button.pack(side="left", padx=10)
