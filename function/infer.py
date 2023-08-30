import os
import torch
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
from function.score import nms, xywh2xyxy
from function.nozzle import nozzle

class Model:
    def __init__(self, model_type, model_name, providers):
    
        self.model_type = model_type
    
        #さとうきびはこちら
        if model_name == "sugarcane":
            print("use sugarcane model")
            
            if model_type == "Yolo v7":
                self.model = ort.InferenceSession(f"./model/{model_name}_v7.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]

                self.outname = [self.model.get_outputs()[0].name]
                self.inname = [i.name for i in self.model.get_inputs()]

                
            elif model_type == "Yolo v8":
                self.model = ort.InferenceSession(f"./model/{model_name}_v8.onnx", providers=providers)
                self.label_names = ["sugarcane", "weed"]

                model_inputs = self.model.get_inputs()
                self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
                self.input_shape = model_inputs[0].shape

                model_output = self.model.get_outputs()
                self.output_names = [model_output[i].name for i in range(len(model_output))]
                
            #nasバージョンはこちら！
            #elif model_type == "Yolo nas":
            #   self.model = ort.InferenceSession(f"./model/{model_name}-yolonas.onnx", providers=providers)
            #   self.label_names = ["sugarcane", "weed"]
            
        #パイナップルはこちら
        elif model_name == "pineapple":
            print("use pineapple model")
            
            if model_type == "Yolo v7":
                self.model = ort.InferenceSession(f"./model/{model_name}_v7.onnx", providers=providers)
                self.label_names = ["pineapple", "weed"]

                self.outname = [self.model.get_outputs()[0].name]
                self.inname = [i.name for i in self.model.get_inputs()]

                
            elif model_type == "Yolo v8":
                self.model = ort.InferenceSession(f"./model/{model_name}_v8.onnx", providers=providers)
                self.label_names = ["pineapple", "weed"]

                model_inputs = self.model.get_inputs()
                self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
                self.input_shape = model_inputs[0].shape

                model_output = self.model.get_outputs()
                self.output_names = [model_output[i].name for i in range(len(model_output))]

            #nasバージョンはこちら！
            #elif model_type == "Yolo nas":
            #   self.model = ort.InferenceSession(f"./model/{model_name}-yolonas.onnx", providers=providers)
            #   self.label_names = ["sugarcane", "weed"]



        self.colors = {name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(self.label_names)}
    
    #改変？
    def infer(self, frame):

        print(f"model_type: {self.model_type}")


        if self.model_type == "Yolo v7":
            
            start_time = time.perf_counter()

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

            end_time = time.perf_counter()
            fps = int(1 / (end_time - start_time))
            print(f"FPS:{fps}")

            return frame, fps
        
        elif self.model_type == "Yolo v8":
            
            start_time = time.perf_counter()

            print(f"frame: {frame.shape}")

            image_height, image_width = frame.shape[0], frame.shape[1]
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

                # if cls == "weed":
                    
                #     nozzle(image_draw, bbox)


                #     tx = (bbox[0] - bbox[2]) * 0.5
                #     y = (bbox[1] - bbox[3]) * 0.5
                #     x = bbox[0] + tx
                #     ty = bbox[1] + y



                #     h, main, c = frame.shape
                #     main1 = main * 0.5 #-1,+1はハード側との微調整用
                #     main1_1 = main1 * 0.5 #0%-25%
                #     main2 = main1_1 + main1_1 #25%-50%
                #     main3 = main2 + main1_1 #50%-75%
                #     main4 = main3 + main1_1 #75%-100%

                # if ty <= h* 0.5: # 300～280の間の範囲で設定する
                #     #閾値の設定もここでできるようにしておく

                #     # main2 = main[1] * 0.5 
                #     #横
                #     if x <= main1_1: #-1,+1はハード側との微調整用　
                #             print(x)
                #             i =[1,0,0,0]
                #             print(i)
                #     if x >= main1_1 and x <= main2: #-1,+1はハード側との微調整用　
                #             print(x)
                #             i =[0,1,0,0]
                #             print(i)
                #     if x >= main2 and x <= main3: #-1,+1はハード側との微調整用　
                #             print(x)
                #             i =[0,0,1,0]
                #             print(i)
                #     if x >= main3 and x <= main4: #-1,+1はハード側との微調整用　
                #             print(x)
                #             i =[0,0,0,1]
                #             print(i)

                #     ser = serial.Serial('COM4',9600,timeout=None)
                #     ser.write(i)
                #     ser.close()


                color = (0,255,0)
                cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
                cv2.putText(image_draw,
                            f'{cls}:{int(score*100)}', (bbox[0], bbox[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.60, [0, 0, 0],
                            thickness=1)
            
            end_time = time.perf_counter()

            fps = int(1 / (end_time - start_time))
                
            return image_draw, fps