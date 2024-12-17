import customtkinter

from frames import CropsFrame, InferenceModelFrame, ModelSelectionFrame, OptionFrame
from function.const.crop import CropType
from function.const.model import ModelType
from view_process import ViewProcess


class Setup(customtkinter.CTk):
    def __init__(self) -> None:
        """
        画面のセットアップを行う
        """
        super().__init__()

        # ウィンドウサイズ（幅x高さ）
        self.geometry(geometry_string="1000x800")

        # 作物のFrameを表示
        self.crops_frame = CropsFrame(self, self.model_selection)
        self.crops_frame.pack(side="left", padx=40, pady=10, anchor="center")

        # 推論モデルのFrameを表示
        self.inference_model_frame = InferenceModelFrame(self, self.model_selection)
        self.inference_model_frame.pack(side="left", padx=40, pady=10, anchor="center")

        # オプションのFrameを表示
        self.option_frame = OptionFrame(self)
        self.option_frame.pack(side="left", padx=40, pady=10, anchor="center")

        # モデル選択のFrameを表示
        self.set_model_selection(
            self.crops_frame.get_selected_rbtn_value(), self.inference_model_frame.get_selected_rbtn_value()
        )

        # 実行ボタン
        self.execute_button = customtkinter.CTkButton(master=self, text="実行", command=self.screen_transition)
        self.execute_button.pack(side="right", padx=10, pady=10, anchor="center")

    def model_selection(self) -> None:
        """
        モデル選択
        """
        self.model_selection_frame.destroy()
        self.set_model_selection(
            self.crops_frame.get_selected_rbtn_value(), self.inference_model_frame.get_selected_rbtn_value()
        )

    def set_model_selection(self, crop: CropType, model: ModelType) -> None:
        """
        モデル選択
        """
        self.model_selection_frame = ModelSelectionFrame(self, crop, model)
        self.model_selection_frame.pack(side="left", padx=40, pady=10, anchor="center")

    def screen_transition(self) -> None:
        """画面遷移"""
        crops_value = self.crops_frame.get_selected_rbtn_value()
        inference_model_value = self.inference_model_frame.get_selected_rbtn_value()
        is_test = self.option_frame.get_is_test()
        is_serial = self.option_frame.get_is_serial()
        model_path = self.model_selection_frame.get_model_path()
        print("Selected crops: ", crops_value)
        print("Selected inference model: ", inference_model_value)
        print("Is test mode: ", is_test)
        print("Is serial mode: ", is_serial)
        print("Selected model: ", model_path)

        if crops_value != "" and inference_model_value != "":
            print("両方選択されている")

            self.crops_frame.destroy()
            self.inference_model_frame.destroy()
            self.execute_button.destroy()
            self.option_frame.destroy()
            self.model_selection_frame.destroy()

            left_camera_index: str | int = 0
            right_camera_index: str | int = 1

            # テストモードの場合はカメラではなく動画を読み込む
            if is_test:
                left_camera_index = "video/tests/multi_data1.mp4"
                right_camera_index = "video/tests/multi_data2.mp4"

            # 左の画面設定
            self.left_view_process = ViewProcess(
                master=self,
                is_serial=is_serial,
                is_test=is_test,
                inference_model_value=inference_model_value,
                crops_value=crops_value,
                model_path=model_path,
                camera_index=left_camera_index,
            )
            self.left_view_process.pack(side="left", expand=True, fill="both")

            # 右の画面設定
            self.right_view_process = ViewProcess(
                master=self,
                is_serial=is_serial,
                is_test=is_test,
                inference_model_value=inference_model_value,
                crops_value=crops_value,
                model_path=model_path,
                camera_index=right_camera_index,
            )
            self.right_view_process.pack(side="right", expand=True, fill="both")

        else:
            print("両方選択されていない")
            # モーダルウィンドウを表示
            self.create_modal_windows()

    def create_modal_windows(self) -> None:
        modal_window = customtkinter.CTkToplevel(self)
        modal_window.geometry(geometry_string="400x300")

        text_label = customtkinter.CTkLabel(master=modal_window, text="作物と推論モデル両方を選択してください")
        text_label.pack(padx=10, pady=10)

        # モーダルにする
        modal_window.grab_set()
        # モーダルウィンドウにフォーカスする
        modal_window.focus_set()
        # タスクバーに表示しない
        modal_window.transient(master=self)

        # 閉じられるまで待つ
        app.wait_window(window=modal_window)
        print("モーダルウィンドウが閉じられた")


if __name__ == "__main__":
    app = Setup()
    app.title(string="画像認識")

    app.mainloop()
