import customtkinter

from crops_frame import CropsFrame
from inference_model_frame import InferenceModelFrame
from view_process import ViewProcess


class Setup(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # ウィンドウサイズ（幅x高さ）
        self.geometry(geometry_string="1000x800")

        # 作物のFrameを表示
        self.crops_frame = CropsFrame(self)
        self.crops_frame.pack(side="left", padx=40, pady=10, anchor="center")

        # 推論モデルのFrameを表示
        self.inference_model_frame = InferenceModelFrame(self)
        self.inference_model_frame.pack(side="left", padx=40, pady=10, anchor="center")

        # 実行ボタン
        self.execute_button = customtkinter.CTkButton(master=self, text="実行", command=self.screen_transition)
        self.execute_button.pack(side="right", padx=10, pady=10, anchor="center")

    def screen_transition(self) -> None:
        """画面遷移"""
        crops_value = self.crops_frame.get_selected_rbtn_value()
        inference_model_value = self.inference_model_frame.get_selected_rbtn_value()

        if crops_value != "" and inference_model_value != "":
            print("両方選択されている")

            self.crops_frame.destroy()
            self.inference_model_frame.destroy()
            self.execute_button.destroy()

            # 二つのViewProcessインスタンスを作成
            self.view_process1 = ViewProcess(
                master=self,
                inference_model_value=inference_model_value,
                crops_value=crops_value,
                camera_index=0,  # ここで読み込ませる動画の設定を行う
            )
            self.view_process1.pack(side="left", expand=True, fill="both")

            self.view_process2 = ViewProcess(
                master=self,
                inference_model_value=inference_model_value,
                crops_value=crops_value,
                camera_index=1,  # videoフォルダーの下にある動画に置き換えてください
            )
            self.view_process2.pack(side="right", expand=True, fill="both")

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
