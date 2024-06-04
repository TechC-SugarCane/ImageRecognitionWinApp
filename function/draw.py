import cv2
import numpy as np
from .nozzle import nozzle

def draw(frame, outputs, ratio, dwdh, label_names, colors):
	"""
	推論した結果をフレームに描画させる
	:param frame   		: 入力された画像データまたは動画データ
	:param outputs 		: 推論されたデータ
	:param ratio 		: リサイズ後の画像サイズとリサイズ前の画像サイズの比率
	:param dwdh			: パディングした分の画像サイズ
	:param label_names  : ラベルのリスト

	:return frame 		: バウンディングボックスが描画されているフレームデータ
	"""

	# 1回の推論で検出したラベルの数だけ繰り返す
	for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(outputs):
		cls_id = int(cls_id)
		score = round(float(score),3)
		print(*label_names)
		print(cls_id)
		name = label_names[cls_id]

		# frame = copy_frame[int(batch_id)]
		box = np.array([x0,y0,x1,y1])
		box -= np.array(dwdh*2)
		box /= ratio
		box = box.round().astype(np.int32).tolist()

		# 雑草のラベルのデータだったときノズルを噴出するプログラムを実装させる
		if name == "weed":
			nozzle(frame, box)
			
		cls_id = int(cls_id)
		score = round(float(score),3)
		name = label_names[cls_id]
		color = colors[name]
		name += ' '+str(score)
		cv2.rectangle(frame,box[:2],box[2:],color,2)
		cv2.putText(frame,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2) 

	return frame