import os
import random
import time

import cv2
import numpy as np
import onnxruntime as ort
import torch
from PIL import Image

from function.draw import draw
from function.letterbox import letterbox


class Model:
    def __init__(self, model_type, model_name, providers):
        if model_type == "Yolo v7":  # ここはのちにクラス継承などを使って判別させる予定
            if model_name == "sugarcane":
                print("use sugarcane model")

                self.model = ort.InferenceSession(
                    f"./model/{model_name}_v7.onnx", providers=providers
                )
                self.label_names = ["sugarcane", "weed"]

            elif model_name == "pineapple":
                print("use pineapple model")

                self.model = ort.InferenceSession(
                    f"./model/{model_name}_v7.onnx", providers=providers
                )
                self.label_names = ["pineapple", "weed"]

            else:
                print("This model is not supported")

        else:
            print("this model type has not supported")

        self.outname = [self.model.get_outputs()[0].name]
        self.inname = [i.name for i in self.model.get_inputs()]

        self.colors = {
            name: [random.randint(0, 255) for _ in range(3)]
            for i, name in enumerate(self.label_names)
        }

        self.prev_time = time.time()  # 前回のフレームの時刻

    def infer(self, frame, current_time):
        # FPS計算
        elapsed_time = current_time - self.prev_time
        self.prev_time = current_time
        fps = 1 / elapsed_time

        print(f"fps: {fps}")

        copy_frame = frame.copy()

        # Preprocessing frame (type: numpy -> type: tensor)
        copy_frame, ratio, dwdh = letterbox(copy_frame, auto=False)
        copy_frame = copy_frame.transpose((2, 0, 1))
        copy_frame = np.expand_dims(copy_frame, 0)
        copy_frame = np.ascontiguousarray(copy_frame)
        copy_frame = copy_frame.astype(np.float32)
        copy_frame /= 255

        # run inference
        inp = {self.inname[0]: copy_frame}
        outputs = self.model.run(self.outname, inp)[0]

        # draw result

        frame = draw(frame, outputs, ratio, dwdh, self.label_names, self.colors)

        return frame
