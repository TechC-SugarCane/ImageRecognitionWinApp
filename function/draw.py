import cv2
import numpy as np
from .nozzle import nozzle
def draw(frame, outputs, ratio, dwdh, label_names, colors):


	for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(outputs):
		cls_id = int(cls_id)
		score = round(float(score),3)
		name = label_names[cls_id]

		# frame = copy_frame[int(batch_id)]
		box = np.array([x0,y0,x1,y1])
		box -= np.array(dwdh*2)
		box /= ratio
		box = box.round().astype(np.int32).tolist()

		# if name == "weed":
                      
		# 		nozzle(frame, box)
            
			# tx = (box[0] - box[2]) * 0.5
			# y = (box[1] - box[3]) * 0.5
			# x = box[0] + tx
			# ty = box[1] + y

			# h, main, c = frame.shape
			# main1 = main * 0.5 #-1,+1はハード側との微調整用
			# main1_1 = main1 * 0.5 #0%-25%
			# main2 = main1_1 + main1_1 #25%-50%
			# main3 = main2 + main1_1 #50%-75%
			# main4 = main3 + main1_1 #75%-100%
            
			# if ty <= h* 0.5: # 300～280の間の範囲で設定する
			# 	#閾値の設定もここでできるようにしておく

			# 	# main2 = main[1] * 0.5 
			# 	#横
			# 	if x <= main1_1: #-1,+1はハード側との微調整用　
			# 			print(x)
			# 			i =[1,0,0,0]
			# 			print(i)
			# 	if x >= main1_1 and x <= main2: #-1,+1はハード側との微調整用　
			# 			print(x)
			# 			i =[0,1,0,0]
			# 			print(i)
			# 	if x >= main2 and x <= main3: #-1,+1はハード側との微調整用　
			# 			print(x)
			# 			i =[0,0,1,0]
			# 			print(i)
			# 	if x >= main3 and x <= main4: #-1,+1はハード側との微調整用　
			# 			print(x)
			# 			i =[0,0,0,1]
			# 			print(i)

			# 	ser = serial.Serial('COM4',9600,timeout=None)
			# 	ser.write(i)
			# 	ser.close()

		cls_id = int(cls_id)
		score = round(float(score),3)
		name = label_names[cls_id]
		color = colors[name]
		name += ' '+str(score)
		cv2.rectangle(frame,box[:2],box[2:],color,2)
		cv2.putText(frame,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2) 

	return frame

def plot_bbox(frame, bboxes):
    for bbox in bboxes:
        bbox = bbox.astype(int)

        print(f"bbox: {bbox}")

        frame = cv2.rectangle(frame, bbox[0:2], bbox[2:4], (0, 255, 0), 2)
    return frame

def draw_box(frame, box, label, score, color, alpha=0.25):
    """Draw boxes on images"""
    # fill box
    crop_box = frame[
        box[1] : (box[1] + box[3]), box[0] : (box[0] + box[2])
    ]  # crop box from frame
    color_box = np.ones([*crop_box.shape[:2], 1], dtype=np.uint8) * np.asarray(
        color, dtype=np.uint8
    )  # color box (same size with crop). [h, w, 1] * [c] => [h, w, c]
    cv2.addWeighted(
        crop_box, 1 - alpha, color_box, alpha, 1.0, crop_box
    )  # weighted from color box to frame

    cv2.rectangle(frame, box, color, 2)  # draw box

    # measuring text
    size = min(frame.shape[:2]) * 0.0007
    thickness = int(min(frame.shape[:2]) * 0.001)
    (label_width, label_height), _ = cv2.getTextSize(
        f"{label} - {round(score, 2)}%",
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        thickness,
    )
    # draw labels (filled rect with text inside)
    cv2.rectangle(
        frame,
        (box[0] - 1, box[1] - int(label_height * 2)),
        (box[0] + int(label_width * 1.1), box[1]),
        color,
        cv2.FILLED,
    )
    cv2.putText(
        frame,
        f"{label} - {round(score, 2)}%",
        (box[0], box[1] - int(label_height * 0.7)),
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        [255, 255, 255],
        thickness,
        cv2.LINE_AA,
    )

    return frame