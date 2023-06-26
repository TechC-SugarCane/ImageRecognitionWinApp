import cv2
import onnxruntime as ort
import torch
from function.infer import Model

# set model_name

model_name = "pineapple"
model_type = "Yolo v7"

providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if torch.cuda.is_available() else ['CPUExecutionProvider']

model = Model(model_type=model_type, model_name=model_name, providers=providers)

# Camera settings
cap = cv2.VideoCapture(0)

while cv2.waitKey(1) != 27:
    ret, frame = cap.read()

    frame = model.infer(frame)

    cv2.imshow("test", frame)

cap.release()
cv2.destroyAllWindows()