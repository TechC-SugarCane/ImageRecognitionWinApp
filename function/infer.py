import os
import random
import time
from typing import Optional, Tuple

from cv2.typing import MatLike
import numpy as np
import serial
from ultralytics import YOLO
import yaml

from function.const.crop import CropType
from function.const.model import ModelType
from function.draw import draw
from function.nozzle import calc_nozzle_byte_idx, execute_nozzle

# onnxでモデルを読み込んだ時のプロバイダー
PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]


def load_yaml_config(file_path: str) -> dict:
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


class Model:
    def __init__(
        self,
        model_type: ModelType,
        model_name: CropType,
        model_path: str,
    ) -> None:
        """
        モデルの読み込み、基礎設定を行う
        :param model_type : 使用するモデルのバージョン
        :param model_name : 使用するモデルの名前
        :param model_path : モデルのパス
        """

        self.model_type = model_type
        self.model_name = model_name

        task = "detect"

        # 選択されたモデルのバージョンをチェック
        print(f"Use {model_type} model. model name: {self.model_name}")
        # モデルの読み込み
        self.model = YOLO(model_path, task=task)
        self.labels = [name for _, name in self.model.names.items()]

        # ランダムでバウンディングボックスの色を決める
        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.labels)}

    def load_model(self, model_path: str, task: str) -> YOLO:
        """
        モデルを読み込む
        :param model_path : モデルのパス
        :param task       : タスク名
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        return YOLO(model_path, task=task)

    def infer(self, is_serial: bool, ser: Optional[serial.Serial], frame: MatLike) -> Tuple[MatLike, int]:
        """
        入力された画像を選択されたモデルを使用して推論を行う
        :param is_serial : シリアル通信モードかどうか
        :param ser       : シリアル用のオブジェクト
        :param frame     : 入力された画像データまたは動画データ

        :return frame    : バウンディングボックスが描画されているフレームデータ
        :return fps      : フレームレート
        """

        # モデルのバージョンごとにそれぞれ推論処理を行う
        # 時間の計測を開始
        start_time = time.perf_counter()

        copy_frame = frame.copy()
        outputs = self.model(copy_frame)[0]
        boxes_obj = outputs.boxes
        boxes = boxes_obj.xyxy.cpu().numpy()
        confidences = boxes_obj.conf.cpu().numpy()
        class_ids = boxes_obj.cls.cpu().numpy().astype(np.int32)

        if boxes is None or confidences is None or class_ids is None:
            raise ValueError("The values of boxes, confidences, and class_ids must not be None.")

        for box, confidence, class_id in zip(boxes, confidences, class_ids, strict=True):
            label_name = self.labels[class_id]
            score = round(float(confidence), 3)

            box = box.round().astype(np.int32).tolist()

            # シリアル通信モードの場合は、雑草のラベルのデータだったときノズルを噴出する
            if is_serial and label_name == "weed":
                nozzle_control_bytes = calc_nozzle_byte_idx(frame.shape, box)
                if nozzle_control_bytes is not None:
                    execute_nozzle(ser, nozzle_control_bytes)

            # 元フレームに上書きする形でバウンディングボックスを描画
            frame = draw(frame, label_name, score, box, self.colors)

        # 時間の計測を終了 fps の計算をする
        end_time = time.perf_counter()
        fps = int(1 / (end_time - start_time))

        return frame, fps
