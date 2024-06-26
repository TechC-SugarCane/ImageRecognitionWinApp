import os
import random
import time

import serial
import cv2
import numpy as np
import onnxruntime as ort
import torch
from PIL import Image

from function.letterbox import letterbox
from function.draw import draw
from function.nozzle import nozzle

class Model:
    def __init__(self, model_type, model_name, labels, providers):
        """
        モデルの読み込み、基礎設定を行う
        :param model_type : 使用するモデルのバージョン (Yolo v7 or Yolo nas)
        :param model_name : 使用するモデルの名前 (sugarcane or pineapple)
        :param labels     : ラベルの名前を格納したリスト
        :param providers  : onnxでモデルを読み込んだ時のプロバイダー ['CUDAExecutionProvider', 'CPUExecutionProvider']
        """
    
        self.model_type = model_type
        self.model_name = model_name
        self.providers = providers
        self.labels = labels
    
        # 選択されたモデルのバージョンをチェック
        if model_type == "Yolo v7":
            print(f"use YOLO v7 model. model name: {self.model_name}")

            # モデルの読み込み
            self.model = ort.InferenceSession(f"./model/{self.model_name}_v7.onnx", providers=providers)

            self.outname = [self.model.get_outputs()[0].name]
            self.inname = [i.name for i in self.model.get_inputs()]

        # elif model_type == "Yolo nas":
        #   self.model = ort.InferenceSession(f"./model/{model_name}-yolonas.onnx", providers=providers)
        #   self.label_names = labels.append(self.model_name)

        # ランダムでバウンディングボックスの色を決める
        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.labels)}
    
    def infer(self, frame):
        """
        入力された画像を選択されたモデルを使用して推論を行う
        :param frame: 入力された画像データまたは動画データ

        :return frame: バウンディングボックスが描画されているフレームデータ
        :return fps  : フレームレート
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
            inp = {self.inname[0] : copy_frame}
            outputs = self.model.run(self.outname, inp)[0]

            # バウンディングボックスを入力されたフレームに描画する
            frame = draw(frame, outputs, ratio, dwdh, self.labels, self.colors)
            
            # 時間の計測を終了 fps の計算をする
            end_time = time.perf_counter()
            fps = int(1 / (end_time - start_time))

            return frame, fps