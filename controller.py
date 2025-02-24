import customtkinter

from gui.inference_view import InferenceView
from gui.setup_view import SetupView
from hardware.nozzle import close_serial_port, set_serial_port

VID = "0x0483"
PID = "0x5740"


class AppController:
    def __init__(self) -> None:
        """アプリケーションのコントローラ"""
        self.root = customtkinter.CTk()
        self.setup_view = None
        self.inference_view = None
        self.serial_port = None

    def run(self) -> None:
        """アプリケーションを実行する"""
        self.show_setup_view()
        self.root.title("画像認識")
        self.root.geometry("1000x800")
        self.root.mainloop()

    def show_setup_view(self, params: dict = None) -> None:
        """
        セットアップ画面を表示する
        :param params: セットアップ画面に渡すパラメータ
        """
        self.clear_root()
        self.setup_view = SetupView(master=self.root, controller=self, execute_callback=self.show_inference_view)
        self.setup_view.pack(fill="both", expand=True)
        if params is not None:
            self.setup_view.set_params(params)

    def show_inference_view(self, params: dict) -> None:
        """
        推論画面を表示する
        :param params: 推論画面に渡すパラメータ
        """

        if params["is_serial"]:
            try:
                self.serial_port = set_serial_port(VID, PID)
            except Exception as e:
                self.setup_view.create_modal_windows(self.root, "error", f"シリアル通信の接続に失敗しました\n{e}")
                return
        else:
            self.serial_port = None

        self.clear_root()

        self.inference_view = InferenceView(
            master=self.root, controller=self, params=params, ser=self.serial_port, back_callback=self.back_to_setup
        )
        self.inference_view.pack(fill="both", expand=True)

    def back_to_setup(self, params: dict) -> None:
        """
        セットアップ画面に戻る

        :param params: セットアップ画面に渡すパラメータ
        """
        if self.inference_view:
            self.inference_view.destroy()
            self.inference_view = None
        if self.serial_port:
            close_serial_port(self.serial_port)
            self.serial_port = None
        self.show_setup_view(params)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
