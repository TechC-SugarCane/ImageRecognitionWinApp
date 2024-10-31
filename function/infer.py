import os
import random
import time
from typing import Literal, Tuple

from cv2.typing import MatLike
import numpy as np
import onnxruntime as ort
import torch  # これ消すとエラー出る. onnxruntime側で必要みたい
import yaml

from function.draw import draw
from function.letterbox import letterbox
from function.nozzle import nozzle

# onnxでモデルを読み込んだ時のプロバイダー
PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]

def load_yaml_config(file_path: str) -> dict:
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


class Model:
    def __init__(
        self,
        model_type: Literal["YOLOv7", "YOLOv10"],
        model_name: Literal["sugarcane", "pineapple"],
        labels: list[Literal["sugarcane", "pineapple", "weed"]],
    ) -> None:
        """
        モデルの読み込み、基礎設定を行う
        :param model_type : 使用するモデルのバージョン
        :param model_name : 使用するモデルの名前
        :param labels     : ラベルの名前を格納したリスト
        """

        self.yolov10_cfg = load_yaml_config("./cfg/yolov10.yml")

        self.model_type = model_type
        self.model_name = model_name
        self.labels = labels

        # 選択されたモデルのバージョンをチェック
        if model_type == "YOLOv7":
            print(f"Use YOLO v7 model. model name: {self.model_name}")

            # モデルの読み込み
            self.model = self.load_model(f"./model/{self.model_name}_v7.onnx")
        elif model_type == "YOLOv10":
            print(f"Use YOLO v10 model. model name: {self.model_name}")

            # モデルの読み込み
            self.model = self.load_model(f"./model/{self.model_name}_v10.onnx")

        self.outname = [self.model.get_outputs()[0].name]
        self.inname = [i.name for i in self.model.get_inputs()]

        # ランダムでバウンディングボックスの色を決める
        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.labels)}

    def load_model(self, model_path: str) -> ort.InferenceSession:
        """
        モデルを読み込む
        :param model_path : モデルのパス
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        return ort.InferenceSession(model_path, providers=PROVIDERS)


    def infer(self, is_serial: bool, frame: MatLike) -> Tuple[MatLike, int]:
        """
        入力された画像を選択されたモデルを使用して推論を行う
        :param is_serial : シリアル通信モードかどうか
        :param frame     : 入力された画像データまたは動画データ

        :return frame    : バウンディングボックスが描画されているフレームデータ
        :return fps      : フレームレート
        """

        # モデルのバージョンごとにそれぞれ推論処理を行う
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

        boxes, confidences, class_ids = None, None, None

        if self.model_type == "YOLOv7":
            boxes, confidences, class_ids = self.post_process_yolov7(outputs)

        if self.model_type == "YOLOv10":
            boxes, confidences, class_ids = self.post_process_yolov10(outputs)

        if boxes is None or confidences is None or class_ids is None:
            raise ValueError("The values of boxes, confidences, and class_ids must not be None.")

        for box, confidence, class_id in zip(boxes, confidences, class_ids, strict=True):
            label_name = self.labels[class_id]
            score = round(float(confidence), 3)

            box -= np.array(dwdh * 2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()

            # シリアル通信モードの場合は、雑草のラベルのデータだったときノズルを噴出する
            if is_serial and label_name == "weed":
                nozzle(frame, box)

            # 元フレームに上書きする形でバウンディングボックスを描画
            frame = draw(frame, label_name, score, box, self.colors)

        # 時間の計測を終了 fps の計算をする
        end_time = time.perf_counter()
        fps = int(1 / (end_time - start_time))

        return frame, fps

    def post_process_yolov7(self, output: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        YOLO v7 の後処理

        :param output : 推論結果. (batch_id, x0, y0, x1, y1, cls_id, score)

        :return processed_outputs : 後処理後の推論結果. (boxes(x0, y0, x1, y1), confidences, class_ids)
        """
        return output[:, 1:5], output[:, 5], output[:, 6].astype(int)

    def post_process_yolov10(self, output: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        YOLO v10 の後処理

        :param output : 推論結果

        :return processed_outputs : 後処理後の推論結果. (boxes(x0, y0, x1, y1), confidences, class_ids)
        """
        output = output.squeeze()
        boxes = output[:, :-2]
        confidences = output[:, -2]
        class_ids = output[:, -1].astype(int)

        mask = confidences > self.yolov10_cfg["conf_thres"]
        boxes = boxes[mask, :]
        confidences = confidences[mask]
        class_ids = class_ids[mask]

        return boxes, confidences, class_ids
