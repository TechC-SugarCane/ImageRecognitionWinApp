import customtkinter

from crops_frame import CropsFrame
from inference_model_frame import InferenceModelFrame
from view_process import ViewProcess


class Setup(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        
        if master is not None:
            self.master: customtkinter.CTk = master
            
            # ウィンドウタイトル
            self.master.title("Setup")
            # ウィンドウサイズ（幅x高さ）
            self.master.geometry("1000x800")
            
            self.frame = customtkinter.CTkFrame(self.master,
            width=500,
            height=300,
            corner_radius=10,
            )
            self.frame.place(x=20, y=20)
        
            self.label = customtkinter.CTkLabel(self.frame, text="設定")
            self.label.place(x=30, y=30)
        
            # 作物選択肢
            self.label = customtkinter.CTkLabel(self.frame, text="作物")
            self.label.place(x=180, y=80)
            self.crops_frame: CropsFrame = CropsFrame(self.master)
            self.crops_frame.pack(side="left", padx=40, pady=10, anchor="center")
        
            # 推論モデル選択肢
            self.label = customtkinter.CTkLabel(self.frame, text="推論モデル")
            self.label.place(x=180, y=80)
            self.inference_model_frame: InferenceModelFrame(self.master)
            self.inference_model_frame.place(side="left", padx=40, pady=10, anchor="center")
            
            # 実行開始ボタン
            self.run_button = customtkinter.CTkButton(self.frame, command=self.screen_transition, text="実行開始")
            self.run_button.place(x=330, y=100)
        
    
    def screen_transition(self):
        # 画面遷移する
        crops_value: str = self.crops_frame.show_selected_rbtn_value()
        inference_model_value: str = (
            self.inference_model_frame.show_selected_rbtn_value()
        )

        if crops_value != "" and inference_model_value != "":
            print("両方選択されている")

            # ! 下記のframeやbuttonを扱うframeを用意して、それをdestroyしたい
            self.crops_frame.destroy()
            self.inference_model_frame.destroy()
            self.execute_button.destroy()

            # TODO 新しいFrameを作る カメラの映像を表示する
            self.view_process: ViewProcess = ViewProcess(self.master)
            self.view_process.pack(expand=True, fill="both")

        else:
            print("両方選択されていない")
            # モーダルウィンドウを表示
            self.create_modal_window()
    
    def create_modal_window(self):
        # モーダルウィンドウを作る
        modal_window: customtkinter.CTk.Toplevel = customtkinter.CTk.Toplevel(self)
        modal_window.geometry("300x200")

        text_label: customtkinter.CTkLabel = customtkinter.CTkLabel(modal_window, text="作物と推論モデル両方を選択してください")
        text_label.pack(padx=10, pady=10)

        # モーダルにする
        modal_window.grab_set()
        # モーダルウィンドウにフォーカスする
        modal_window.focus_set()
        # タスクバーに表示しない
        modal_window.transient(self.master)

        # 閉じられるまで待つ
        setup.wait_window(modal_window)
        print("モーダルウィンドウが閉じられた")
        

if __name__ == "__main__":
    root: customtkinter.CTk = customtkinter.CTk()
    setup: Setup = Setup(master=root)
    setup.pack(expand=True, fill="both")
    setup.mainloop()
    