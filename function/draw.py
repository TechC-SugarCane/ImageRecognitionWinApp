import cv2
import numpy as np


def draw(frame, outputs, ratio, dwdh, label_names, colors):

    for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(outputs):
        # frame = copy_frame[int(batch_id)]
        box = np.array([x0,y0,x1,y1])
        box -= np.array(dwdh*2)
        box /= ratio
        box = box.round().astype(np.int32).tolist()
        cls_id = int(cls_id)
        score = round(float(score),3)
        name = label_names[cls_id]
        color = colors[name]
        name += ' '+str(score)
        cv2.rectangle(frame,box[:2],box[2:],color,2)
        cv2.putText(frame,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2) 

    return frame
