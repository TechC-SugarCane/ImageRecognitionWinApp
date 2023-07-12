import os
import random
import time

import cv2
import numpy as np
import onnxruntime as ort
import torch
from PIL import Image

from function.draw import draw, plot_bbox, draw_box
from function.letterbox import letterbox, cxcywh2xyxy


class Model:
    def __init__(self, model_type, model_name, providers):
        if model_type == "Yolo NAS":  # ここはのちにクラス継承などを使って判別させる予定
            if model_name == "sugarcane":
                print("use sugarcane model")

                self.model = ort.InferenceSession(
                    f"./model/{model_name}_nas.onnx", providers=providers
                )
                self.label_names = ["sugarcane", "weed"]

            elif model_name == "pineapple":
                print("use pineapple model")

                self.model = ort.InferenceSession(
                    f"./model/{model_name}_nas.onnx", providers=providers
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

    # def infer(self, frame):

    #     start_time = time.perf_counter()

    #     copy_frame = frame.copy()

    #     # Preprocessing frame (type: numpy -> type: tensor)
    #     copy_frame, ratio, dwdh = letterbox(copy_frame, auto=False)
    #     copy_frame = copy_frame.transpose((2, 0, 1))
    #     copy_frame = np.expand_dims(copy_frame, 0)
    #     copy_frame = np.ascontiguousarray(copy_frame)
    #     copy_frame = copy_frame.astype(np.float32)
    #     copy_frame /= 255

    #     # run inference
    #     inp = {self.inname[0]: copy_frame}
    #     output = self.model.run(self.outname, inp)[0]
    #     # output = output[output[:, 3] > 0.8]


    #     output = cxcywh2xyxy(output)

    #     # draw result

    #     # frame = draw(frame, outputs, ratio, dwdh, self.label_names, self.colors)

    #     # frame = plot_bbox(frame, output)

    #     end_time = time.perf_counter()

    #     fps = 1 / (end_time - start_time)
    #     print(f"fps: {fps}")

    #     return frame

def infer(net, frame, pre_process, post_process, labels):

    start_time = time.perf_counter()


    """Detect Image/Frame array"""
    copy_frame = frame.copy()  # copy frame array
    input_, prep_meta = pre_process(copy_frame)  # run preprocess
    outputs = net.forward(input_)  # forward

    print(f"input: {input_}")
    print(f"prep_meta: {prep_meta}")
    print(outputs)

    boxes, scores, classes = post_process(outputs, prep_meta)  # postprocess output

    print(post_process.score_thres)
    print(post_process.iou_thres)
    print(f"boxes: {type(boxes)}")
    print(f"scores: {type(scores)}")
    print(f"classes: {classes}")


    selected = cv2.dnn.NMSBoxes(
        boxes, scores, 0.01, 0.01
        )  # run nms to filter boxes

    print(f"selected: {selected}")

    for i in selected:  # loop through selected idx
        box = boxes[i, :].astype(np.int32).flatten()  # get box
        score = float(scores[i]) * 100  # percentage score
        label, color = labels(classes[i], use_bgr=True)  # get label and color class_id



        frame = draw_box(frame, box, label, score, color)  # draw boxes

    end_time = time.perf_counter()
    fps = 1 / (end_time - start_time)

    print(f"fps: {fps}")

    return frame  # Image array after draw process
