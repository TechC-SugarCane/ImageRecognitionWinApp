import customtkinter


class Setup(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        
        
        
        self.frame = customtkinter.CTkFrame(self.master,
            width=500,
            height=300,
            corner_radius=10,
            )
        self.frame.place(x=20, y=20)
        
        self.label = customtkinter.CTkLabel(self.frame, text="設定")
        self.label.place(x=30, y=30)
        
        # 作物、推論モデルの選択肢フォーム
        # 作物選択肢
        self.label = customtkinter.CTkLabel(self.frame, text="作物")
        self.label.place(x=30, y=80)
        self.crops_combobox = customtkinter.CTkComboBox(self.frame, values=["サトウキビ", "トウモロコシ"])
        self.crops_combobox.place(x=30, y=100)
        
        # 推論モデル選択肢
        self.label = customtkinter.CTkLabel(self.frame, text="推論モデル")
        self.label.place(x=180, y=80)
        self.inferencemodel_combobox = customtkinter.CTkComboBox(self.frame, values=["Yolo v7", "Yolo v8", "Yolo NAS"])
        self.inferencemodel_combobox.place(x=180, y=100)
        
        # # 実行開始ボタン
        self.run_button = customtkinter.CTkButton(self.frame, command=self.run_button_callback, text="実行開始")
        self.run_button.place(x=330, y=100)
        
        # 「実行開始」ボタン押下でページ遷移
    def run_button_callback(self):
        print("callback")
        

def main():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = customtkinter.CTk()
    app.geometry("600*300+50+50")
    app.title("ImageRecognizationWinApp")
    Setup(app)
    app.mainloop()


if __name__ == "__main__":
    main()
    