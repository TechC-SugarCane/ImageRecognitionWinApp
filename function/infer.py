import os
#import torch
import random
import cv2
import onnxruntime as ort
import numpy as np
from PIL import Image
from function.letterbox import letterbox
from function.draw import draw
from function.score import nms, xywh2xyxy

class Model:

    def __init__(self, model_type, model_name, providers):
    
        self.model_type = model_name
    
        #さとうきびはこちら
        if model_name == "sugarcane":
            print("use sugarcane model")
            
            if model_type == "Yolo v7":
                self.model = ort.InferenceSession(f"./model/{model_name}-yolov7.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]
                
            elif model_type == "Yolo v8":
                self.model = ort.InferenceSession(f"./model/{model_name}-yolov8.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]
                
            #nasバージョンはこちら！
            #elif model_type == "Yolo nas":
            #   self.model = ort.InferenceSession(f"./model/{model_name}-yolonas.onnx", providers=providers)
            #   self.label_names = ["sugarcane", "weed"]
            
        #パイナップルはこちら
        elif model_name == "pineapple":
            print("use pineapple model")
            
            if model_type == "Yolo v7":
                self.model = ort.InferenceSession(f"./model/{model_name}-yolov7.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]
                
            elif model_type == "Yolo v8":
                self.model = ort.InferenceSession(f"./model/{model_name}-yolov8.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]
                
            #nasバージョンはこちら！
            #elif model_type == "Yolo nas":
            #   self.model = ort.InferenceSession(f"./model/{model_name}-yolonas.onnx", providers=providers)
            #   self.label_names = ["sugarcane", "weed"]
        
        ''' 過去データ
        #yolov8
        if model_type == "Yolo v8": # ここはのちにクラス継承などを使って判別させる予定

            if model_name == "sugarcane":
                print("use sugarcane model")

                self.model = ort.InferenceSession(f"./model/{model_name}-yolov8.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]

            elif model_name == "pineapple":
                print("use pineapple model")

                self.model = ort.InferenceSession(f"./model/{model_name}-yolov8.onnx", providers=providers)
                self.label_names = ["pineapple", "weed"]

            else:
                print("This model is not supported")
        
        else:
            print("this model type has not supported")
        '''    

        for i in self.model.get_outputs():
            print(i)

        self.outname = [self.model.get_outputs()[0].name]
        self.inname = [i.name for i in self.model.get_inputs()]
        self.input_shape = self.inname[0]

        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.label_names)}
    
    #改変？
    def infer(self, frame):

        if self.model_type == "Yolo v7":    
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
        
        elif self.model_type == "Yolo v8":
            image_height, image_width = frame.shape[:2]
            Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            input_height, input_width = self.input_shape[2:]
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(image_rgb, (input_width, input_height))

            # Scale input pixel value to 0 to 1
            input_image = resized / 255.0
            input_image = input_image.transpose(2,0,1)
            input_tensor = input_image[np.newaxis, :, :, :].astype(np.float32)
            
            outputs = self.model.run(self.output_names, {self.input_names[0]: input_tensor})[0]
            
            predictions = np.squeeze(outputs).T
            conf_thresold = 0.2
            
            # Filter out object confidence scores below threshold
            scores = np.max(predictions[:, 4:], axis=1)
            predictions = predictions[scores > conf_thresold, :]
            scores = scores[scores > conf_thresold]
            
            # Get the class with the highest confidence
            class_ids = np.argmax(predictions[:, 4:], axis=1)
            
            # Get bounding boxes for each object
            boxes = predictions[:, :4]

            #rescale box
            input_shape = np.array([input_width, input_height, input_width, input_height])
            boxes = np.divide(boxes, input_shape, dtype=np.float32)
            boxes *= np.array([image_width, image_height, image_width, image_height])
            boxes = boxes.astype(np.int32)
            
            # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
            indices = nms(boxes, scores, 0.3)
            
            image_draw = frame.copy()
            for (bbox, score, label) in zip(xywh2xyxy(boxes[indices]), scores[indices], class_ids[indices]):
                bbox = bbox.round().astype(np.int32).tolist()
                cls_id = int(label)
                cls = self.label_names[cls_id]
                color = (0,255,0)
                cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
                cv2.putText(image_draw,
                            f'{cls}:{int(score*100)}', (bbox[0], bbox[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.60, [0, 0, 0],
                            thickness=1)
                
            return image_draw