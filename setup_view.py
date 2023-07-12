import tkinter as tk
from tkinter import Tk, ttk

from crops_frame import CropsFrame
from inference_model_frame import InferenceModelFrame
from view_process import ViewProcess


class SetupView(ttk.Frame):
    def __init__(self, master: Tk | None = None) -> None:
        super().__init__(master)

        if master is not None:
            self.master: Tk = master
            # ウィンドウタイトル
            self.master.title("setup")
            # ウィンドウサイズ（幅x高さ）
            self.master.geometry("1000x800")

            # 作物のFrameを表示
            self.crops_frame: CropsFrame = CropsFrame(self.master)
            self.crops_frame.pack(side="left", padx=40, pady=10, anchor="center")

            # 推論モデルのFrameを表示
            self.inference_model_frame: InferenceModelFrame = InferenceModelFrame(
                self.master
            )
            self.inference_model_frame.pack(
                side="left", padx=40, pady=10, anchor="center"
            )

            # 実行ボタン
            self.execute_button: ttk.Button = ttk.Button(
                self.master, text="実行", command=self.screen_transition
            )
            self.execute_button.pack(side="right", padx=10, pady=10, anchor="center")

    def screen_transition(self):
        """画面遷移する"""
        crops_value: str = self.crops_frame.show_selected_rbtn_value()
        inference_model_value: str = (
            self.inference_model_frame.show_selected_rbtn_value()
        )

        if crops_value != "" and inference_model_value != "":
            print("両方選択されている")

            self.crops_frame.destroy()
            self.inference_model_frame.destroy()
            self.execute_button.destroy()

            # TODO 新しいFrameを作る カメラの映像を表示する
            self.view_process: ViewProcess = ViewProcess(
                self.master, crops_value, inference_model_value
            )
            self.view_process.pack(expand=True, fill="both")

        else:
            print("両方選択されていない")
            # モーダルウィンドウを表示
            self.create_modal_window()

    def create_modal_window(self) -> None:
        """モーダルウィンドウを作る"""
        modal_window: tk.Toplevel = tk.Toplevel(self)
        modal_window.geometry("300x200")

        text_label: ttk.Label = ttk.Label(modal_window, text="作物と推論モデル両方を選択してください")
        text_label.pack(padx=10, pady=10)

        # モーダルにする
        modal_window.grab_set()
        # モーダルウィンドウにフォーカスする
        modal_window.focus_set()
        # タスクバーに表示しない
        modal_window.transient(self.master)

        # 閉じられるまで待つ
        setup_view.wait_window(modal_window)
        print("モーダルウィンドウが閉じられた")


if __name__ == "__main__":
    root: Tk = Tk()
    setup_view: SetupView = SetupView(master=root)
    setup_view.pack(expand=True, fill="both")
    setup_view.mainloop()

"""
setup
作物
推論モデル
で各classを作ったほうが良いかも

TODO crops_frameの上にcrops_labelを表示したい
"""
