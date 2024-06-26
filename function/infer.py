import random
import time
from typing import Literal, Tuple

from cv2.typing import MatLike
import numpy as np
import onnxruntime as ort
import torch  # これ消すとエラー出る. onnxruntime側で必要みたい

from function.draw import draw
from function.letterbox import letterbox

# onnxでモデルを読み込んだ時のプロバイダー
PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]


class Model:
    def __init__(
        self,
        model_type: Literal["Yolo v7", "Yolo NAS"],
        model_name: Literal["sugarcane", "pineapple"],
        labels: list[Literal["sugarcane", "pineapple", "weed"]],
    ) -> None:
        """
        モデルの読み込み、基礎設定を行う
        :param model_type : 使用するモデルのバージョン
        :param model_name : 使用するモデルの名前
        :param labels     : ラベルの名前を格納したリスト
        """

        self.model_type = model_type
        self.model_name = model_name
        self.labels = labels

        # 選択されたモデルのバージョンをチェック
        if model_type == "Yolo v7":
            print(f"Use YOLO v7 model. model name: {self.model_name}")

            # モデルの読み込み
            self.model = ort.InferenceSession(f"./model/{self.model_name}_v7.onnx", providers=PROVIDERS)

            self.outname = [self.model.get_outputs()[0].name]
            self.inname = [i.name for i in self.model.get_inputs()]

        # elif model_type == "Yolo NAS":
        #     print(f"Use YOLO NAS model. model name: {self.model_name}")
        #     self.model = ort.InferenceSession(f"./model/{model_name}_nas.onnx", providers=providers)

        #     self.outname = [self.model.get_outputs()[0].name]
        #     self.inname = [i.name for i in self.model.get_inputs()]

        # ランダムでバウンディングボックスの色を決める
        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.labels)}

    def infer(self, is_serial: bool, frame: MatLike) -> Tuple[MatLike, int]:
        """
        入力された画像を選択されたモデルを使用して推論を行う
        :param is_serial : シリアル通信モードかどうか
        :param frame     : 入力された画像データまたは動画データ

        :return frame    : バウンディングボックスが描画されているフレームデータ
        :return fps      : フレームレート
        """

        # モデルのバージョンごとにそれぞれ推論処理を行う
        if self.model_type == "Yolo v7":
            # 時間の計測を開始
            start_time = time.perf_counter()

            copy_frame = frame.copy()

            # コピーされたフレームを処理して推論用の型に変換する (type: numpy -> type: tensor)
            copy_frame, ratio, dwdh = letterbox(copy_frame, auto=False)
            copy_frame = copy_frame.transpose((2, 0, 1))
            copy_frame = np.expand_dims(copy_frame, 0)
            copy_frame = np.ascontiguousarray(copy_frame)
            copy_frame = copy_frame.astype(np.float32)
            copy_frame /= 255

            # 推論処理の実装
            inp = {self.inname[0]: copy_frame}
            outputs = self.model.run(self.outname, inp)[0]

            # バウンディングボックスを入力されたフレームに描画する
            frame = draw(is_serial, frame, outputs, ratio, dwdh, self.labels, self.colors)

            # 時間の計測を終了 fps の計算をする
            end_time = time.perf_counter()
            fps = int(1 / (end_time - start_time))

            return frame, fps
