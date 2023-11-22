import customtkinter
import cv2
from PIL import Image, ImageOps, ImageTk

from function.infer import Model


class ImageRecognition(customtkinter.CTkFrame):
    def __init__(self, master, model_type, model_name):
        super().__init__(master=master)

        # ウィンドウサイズを取得
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # キャンバスサイズを設定
        canvas_width = window_width // 2
        canvas_height = window_height

        # 一台目のカメラキャンバス
        self.infer_image_canvas1 = customtkinter.CTkCanvas(
            master=self, width=canvas_width, height=canvas_height
        )
        self.infer_image_canvas1.pack(side="left", expand=True, fill="both")

        # 二台目のカメラキャンバス
        self.infer_image_canvas2 = customtkinter.CTkCanvas(
            master=self, width=canvas_width, height=canvas_height
        )
        self.infer_image_canvas2.pack(side="right", expand=True, fill="both")

        # 一台目のカメラ
        self.capture1 = cv2.VideoCapture(0)

        # 二台目のカメラ
        self.capture2 = cv2.VideoCapture(1)

        # モデルとFPSラベルの初期化
        self.model = Model(model_type, model_name, ["CUDAExecutionProvider", "CPUExecutionProvider"])
        self.fps_label = customtkinter.CTkLabel(master=self, text="")
        self.fps_label.pack()

        # 映像表示開始
        self.display_image()

    def display_image(self):
        # 一台目のカメラからの映像を取得
        is_success1, frame1 = self.capture1.read()
        if is_success1:
            self.update_canvas(self.infer_image_canvas1, frame1)

        # 二台目のカメラからの映像を取得
        is_success2, frame2 = self.capture2.read()
        if is_success2:
            self.update_canvas(self.infer_image_canvas2, frame2)

        self.display_id = self.after(ms=10, func=self.display_image)

    def update_canvas(self, canvas, frame):
        infer_frame, fps = self.model.infer(frame)
        self.fps_label.configure(text=fps)
        cv_image = cv2.cvtColor(infer_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        # キャンバスサイズに合わせて調整
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        pil_image = ImageOps.pad(pil_image, size=(canvas_width, canvas_height))

        photo_image = ImageTk.PhotoImage(image=pil_image)
        canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo_image)
        canvas.image = photo_image  # 参照を保持

    def display_stop(self):
        self.after_cancel(self.display_id)

    def display_restart(self):
        if not self.display_id:
            self.display_image()
            self.display_image()
