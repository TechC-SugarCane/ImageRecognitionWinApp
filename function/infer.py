import os
import random
import time
from typing import Literal, Tuple

import cv2
from cv2.typing import MatLike
import numpy as np
import onnxruntime as ort
import yaml

from function.draw import draw
from function.letterbox import letterbox
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
            self.model = self.load_model(f"./models/{self.model_name}_v7.onnx")
        elif model_type == "YOLOv10":
            print(f"Use YOLO v10 model. model name: {self.model_name}")

            # モデルの読み込み
            self.model = self.load_model(f"./models/{self.model_name}_v10.onnx")

        self.outname = [self.model.get_outputs()[0].name]
        model_inputs = self.model.get_inputs()
        self.inname = [i.name for i in model_inputs]

        input_shape = model_inputs[0].shape
        self.input_width = input_shape[2]
        self.input_height = input_shape[3]

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
        ratio = 1.0
        dwdh = (0.0, 0.0)

        # preprocess
        if self.model_type == "YOLOv7":
            copy_frame, ratio, dwdh = self.pre_process_yolov7(copy_frame)

        if self.model_type == "YOLOv10":
            copy_frame = self.pre_process_yolov10(copy_frame)

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

            if self.model_type == "YOLOv7":
                box -= np.array(dwdh * 2)
                box /= ratio

            box = box.round().astype(np.int32).tolist()

            # シリアル通信モードの場合は、雑草のラベルのデータだったときノズルを噴出する
            if is_serial and label_name == "weed":
                nozzle_control_bytes = calc_nozzle_byte_idx(frame.shape, box)
                if nozzle_control_bytes is not None:
                    execute_nozzle(nozzle_control_bytes)

            # 元フレームに上書きする形でバウンディングボックスを描画
            frame = draw(frame, label_name, score, box, self.colors)

        # 時間の計測を終了 fps の計算をする
        end_time = time.perf_counter()
        fps = int(1 / (end_time - start_time))

        return frame, fps

    def pre_process_yolov7(self, frame: MatLike) -> Tuple[MatLike, float, Tuple[float, float]]:
        """
        YOLO v7 の前処理

        :param frame : 入力画像データ

        :return processed_frame : 前処理後の画像データ
        :return ratio           : リサイズ後の画像サイズとリサイズ前の画像サイズの比率
        :return (dw, dh)        : パディングした分の画像サイズ
        """
        # コピーされたフレームを処理して推論用の型に変換する (type: numpy -> type: tensor)
        frame, ratio, dwdh = letterbox(frame, auto=False)
        frame = frame.transpose((2, 0, 1))
        frame = np.expand_dims(frame, 0)
        frame = np.ascontiguousarray(frame)
        frame = frame.astype(np.float32)
        frame /= 255  # type: ignore
        return frame, ratio, dwdh

    def post_process_yolov7(self, output: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        YOLO v7 の後処理

        :param output : 推論結果. (batch_id, x0, y0, x1, y1, cls_id, score)

        :return processed_outputs : 後処理後の推論結果. (boxes(x0, y0, x1, y1), confidences, class_ids)
        """
        return output[:, 1:5], output[:, 6], output[:, 5].astype(int)

    def pre_process_yolov10(self, frame: MatLike) -> np.ndarray:
        """
        YOLO v10 の前処理

        :param frame : 入力画像データ

        :return processed_tensor : 前処理後の画像データ
        """
        self.img_height, self.img_width = frame.shape[:2]

        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize input image
        processed_frame = cv2.resize(processed_frame, (self.input_width, self.input_height))

        # Scale input pixel values to 0 to 1
        processed_frame = processed_frame / 255.0
        processed_frame = processed_frame.transpose(2, 0, 1)
        processed_tensor = processed_frame[np.newaxis, :, :, :].astype(np.float32)

        return processed_tensor

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

        boxes = self.rescale_boxes(boxes)

        return boxes, confidences, class_ids

    def rescale_boxes(self, boxes: np.ndarray) -> np.ndarray:
        """
        バウンディングボックスをリスケールする

        :param boxes : バウンディングボックスの座標

        :return rescaled_boxes : リスケール後のバウンディングボックスの座標
        """
        rescaled_boxes = boxes.copy()
        input_shape = np.array([self.input_width, self.input_height, self.input_width, self.input_height])
        rescaled_boxes = np.divide(rescaled_boxes, input_shape)
        rescaled_boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])

        return rescaled_boxes
