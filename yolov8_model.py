import requests
import cv2
import torch
import infery
import numpy as np
import matplotlib.pyplot as plt


# define visualize funciton
def visualize(image, predictions, categories):
    cm = plt.get_cmap("gist_rainbow")
    plt.figure(figsize=(10, 10))
    for cat_id, cat_name in enumerate(categories):
        boxes = predictions[predictions[:, -1] == cat_id, 0:4]
        plt.plot(boxes[:, [0, 2, 2, 0, 0]].T, boxes[:, [1, 1, 3, 3, 1]].T, '.-', color=cm(cat_id*50), label=cat_name)
    
    plt.imshow(image)
    plt.legend()
    plt.show()

image = cv2.imread("./imagerecognitionwinapp_screen.png")
image_tensor = torch.tensor(np.array(image)[:, :, ::-1].copy()).permute(2, 0, 1).unsqueeze(dim=0).float().cuda()


onnx_model = infery.load("./model/sugarcane_nas.onnx", framework_type="onnx", inference_hardware="cpu")

raw_predictions = [torch.tensor(onnx_model.predict(image_tensor.cpu().numpy())[0])]
predictions = YoloPostPredictionCallback(conf=0.1, iou=0.5)(raw_predictions)[0]

# Visualize
visualize(image, predictions, ["sugarcane", "weed"])