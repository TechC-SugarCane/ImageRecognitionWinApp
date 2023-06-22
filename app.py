import tkinter
from tkinter import Tk, ttk


def show_selected_crops_value():
    print(selected_crops.get())


def show_selected_inference_model_value():
    print(selected_inference_model.get())


# 画面遷移
def screen_transition():
    crops_value = selected_crops.get()
    inference_model_value = selected_inference_model.get()

    if crops_value != "" and inference_model_value != "":
        print("両方選択されている")

        root.destroy()

        new_root = Tk()
        new_root.geometry("1000x800")
        new_root.title("ViewProcess")
        new_root.mainloop()


    else:
        print("選択されていない")


root = Tk()
root.geometry("1000x800")
root.title(u"setup")

frame = ttk.Frame(root)



# 作物フレーム
crops_frame = ttk.Frame(frame, borderwidth=5, relief="ridge", width=200, height=100)
# 推論モデルフレーム
inference_model_frame = ttk.Frame(
    frame, borderwidth=5, relief="ridge", width=200, height=100
)

# Frameサイズ固定
crops_frame.propagate(False)
inference_model_frame.propagate(False)

selected_crops = tkinter.StringVar()
selected_inference_model = tkinter.StringVar()

# radio button
# ? Radiobuttonのtextとvalueの違いは？
pineapple_rbtn = ttk.Radiobutton(
    crops_frame,
    text="パイナップル",
    variable=selected_crops,
    value="パイナップル",
    command=show_selected_crops_value,
)
pineapple_rbtn.pack()

sugarcane_rbtn = ttk.Radiobutton(
    crops_frame,
    text="サトウキビ",
    variable=selected_crops,
    value="サトウキビ",
    command=show_selected_crops_value,
)
sugarcane_rbtn.pack()

# radio button
# ? Radiobuttonのtextとvalueの違いは？
yolov7_rbtn = ttk.Radiobutton(
    inference_model_frame,
    text="Yolo v7",
    variable=selected_inference_model,
    value="Yolo v7",
    command=show_selected_inference_model_value,
)
yolov7_rbtn.pack()

yolov8_rbtn = ttk.Radiobutton(
    inference_model_frame,
    text="Yolo v8",
    variable=selected_inference_model,
    value="Yolo v8",
    command=show_selected_inference_model_value,
)
yolov8_rbtn.pack()

yolo_nas_rbtn = ttk.Radiobutton(
    inference_model_frame,
    text="Yolo NAS",
    variable=selected_inference_model,
    value="Yolo NAS",
    command=show_selected_inference_model_value,
)
yolo_nas_rbtn.pack()

# 実行ボタン
execute_button = ttk.Button(frame, text="実行", command=screen_transition)

frame.grid(column=0, row=0)
crops_frame.grid(column=1, row=0, columnspan=2, rowspan=3, sticky="nsew")
ttk.Frame(frame, width=10).grid(column=3, row=0)  # スペースを追加
inference_model_frame.grid(column=4, row=0, columnspan=2, rowspan=3, sticky="nsew")
execute_button.grid(column=6, row=1, columnspan=1, rowspan=1, sticky="nsew")


# 画面の中央に配置する
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)


root.mainloop()


"""
root
    - 作物frame
        - radioButton
    - 推論frame
        - radioButton
    - 実行button
        - 画面遷移

実行開始ボタン
作物button and 推論button の両方が押されていたら、実行開始ボタンを押せる。
両方押されていない場合は、「ボタンを押してください」的なウィンドウを表示したい


"""
