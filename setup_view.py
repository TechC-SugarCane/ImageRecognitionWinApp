import tkinter as tk
from tkinter import Tk, ttk

from crops_frame import CropsFrame


class SetupView(ttk.Frame):
    def __init__(self, master: Tk | None = None) -> None:
        super().__init__(master)

        if master is not None:
            self.master: Tk = master
            # ウィンドウタイトル
            self.master.title("setup")
            # ウィンドウサイズ（幅x高さ）
            self.master.geometry("1000x800")

            # 作物のラベルを表示
            crops_label = ttk.Label(self.master, text="作物")
            crops_label.pack(side="top", padx=10, pady=10)

            # 作物のFrameを表示
            crops_frame: CropsFrame = CropsFrame(self.master)
            crops_frame.pack(side="left", padx=40, pady=10, anchor="center")


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
