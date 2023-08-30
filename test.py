import cv2
import onnxruntime as ort
import torch
from function.infer import Model
from function.models import load_net
from function.processing import Preprocessing, Postprocessing
from function.utils import Labels
from function.cli import get_configs
from function.processing import YOLO_NAS_DEFAULT_PROCESSING_STEPS
from function.infer import infer

# set model_name

model_name = "pineapple"
model_type = "Yolo NAS"

providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if torch.cuda.is_available() else ['CPUExecutionProvider']

# model = Model(model_type=model_type, model_name=model_name, providers=providers)

net = load_net("./model/pineapple_nas.onnx", gpu=True, dnn=False)  # load net
# net.assert_input_shape((640, 640, 3))  # check input shape
net.warmup()  # warmup net

_, _, input_height, input_width = net.input_shape  # get input height and width [b, c, h, w]

pre_process = Preprocessing(
    YOLO_NAS_DEFAULT_PROCESSING_STEPS, (640, 640)
)  # get preprocess
post_process = Postprocessing(
    YOLO_NAS_DEFAULT_PROCESSING_STEPS,
    0.1,
    0.1,
)  # get postprocess

labels = Labels(["pineapple", "weed"])


# Camera settings
cap = cv2.VideoCapture(1)

while cv2.waitKey(1) != 27:
    ret, frame = cap.read()

    # frame = model.infer(frame)
    # frame = model.infer(net, frame, pre_process, post_process, labels)
    frame = infer(net, frame, pre_process, post_process, labels)

    cv2.imshow("test", frame)

cap.release()
cv2.destroyAllWindows()