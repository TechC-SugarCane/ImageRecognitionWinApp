from ultralytics import YOLO

# Load model
model = YOLO("./pineapple_v8.pt")

model.export(format="onnx")