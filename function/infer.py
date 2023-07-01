import os
import torch
import random
import cv2
import onnxruntime as ort
import numpy as np
from PIL import Image
from function.letterbox import letterbox
from function.draw import draw

class Model:

    def __init__(self, model_type, model_name, providers):
    
        if model_type == "Yolo v7": # ここはのちにクラス継承などを使って判別させる予定

            if model_name == "sugarcane":
                print("use sugarcane model")

                self.model = ort.InferenceSession(f"./model/{model_name}_v7.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]

            elif model_name == "pineapple":
                print("use pineapple model")

                self.model = ort.InferenceSession(f"./model/{model_name}_v7.onnx", providers=providers)
                self.label_names = ["pineapple", "weed"]

            else:
                print("This model is not supported")
        
        else:
            print("this model type has not supported")


        self.outname = [self.model.get_outputs()[0].name]
        self.inname = [i.name for i in self.model.get_inputs()]

        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.label_names)}
    
    def infer(self, frame):

        copy_frame = frame.copy()

        # Preprocessing frame (type: numpy -> type: tensor)
        copy_frame, ratio, dwdh = letterbox(copy_frame, auto=False)
        copy_frame = copy_frame.transpose((2, 0, 1))
        copy_frame = np.expand_dims(copy_frame, 0)
        copy_frame = np.ascontiguousarray(copy_frame)
        copy_frame = copy_frame.astype(np.float32)
        copy_frame /= 255

        # run inference
        inp = {self.inname[0] : copy_frame}
        outputs = self.model.run(self.outname, inp)[0]


        # draw result


        frame = draw(frame, outputs, ratio, dwdh, self.label_names, self.colors)

        return frame