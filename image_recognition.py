import customtkinter
import cv2
from PIL import Image, ImageOps, ImageTk  # 画像データ用

from function.infer import Model


class ImageRecognition(customtkinter.CTkFrame):
    def __init__(self, master, model_type, model_name, camera_index):
        super().__init__(master=master)

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        canvas_width = window_width // 2
        canvas_height = window_height

        self.infer_image_canvas = customtkinter.CTkCanvas(
            master=self, width=canvas_width, height=canvas_height
        )  # type: ignore
        self.infer_image_canvas.pack(side="top", expand=True, fill="both")

        # TODO ここで二つのカメラの映像
        self.capture = cv2.VideoCapture(camera_index) # type: ignore

        self.display_id = ""

        self.model = Model(
            model_type=model_type,
            model_name=model_name,
            labels=["weed", model_name], # ラベル名の順序が異なっていたらこの部分の位置を逆にする
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )

        print(self.model)

        self.fps_label = customtkinter.CTkLabel(master=self, text="")
        self.fps_label.pack()

    def display_image(self):
        is_success, frame = self.capture.read()

        infer_frame, fps = self.model.infer(frame=frame) # type: ignore

        self.fps_label.configure(text=fps)
        self.fps_label.update()

        cv_image = cv2.cvtColor(src=infer_frame, code=cv2.COLOR_BGR2RGB) # type: ignore
        pil_image = Image.fromarray(obj=cv_image)

        canvas_width = self.infer_image_canvas.winfo_width()
        canvas_height = self.infer_image_canvas.winfo_height()

        pil_image = ImageOps.pad(image=pil_image, size=(canvas_width, canvas_height))

        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        self.infer_image_canvas.create_image(
            canvas_width / 2,
            canvas_height / 2,
            image=self.photo_image,
        )

        self.display_id = self.after(ms=10, func=self.display_image)

    def display_stop(self):
        """描画を一時停止する"""
        self.after_cancel(id=self.display_id)
        self.display_id = ""

    def display_restart(self):
        """描画を再開する"""
        if not self.display_id:
            self.display_image()
