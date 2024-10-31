import cv2
from cv2.typing import MatLike


def draw(
    frame: MatLike,
    label_name: str,
    score: float,
    box: list[int, int, int, int],
    colors: dict[str, list[int]],
) -> MatLike:
    """
    推論した結果をフレームに描画させる
    :param frame   		: 入力された画像データまたは動画データ
    :param colors 		: バウンディングボックスの色
    :param label_name   : 推論結果の名前
    :param score  		: 推論結果のスコア
    :param box    		: バウンディングボックスの座標 (x0, y0, x1, y1)
    :return frame 		: バウンディングボックスが描画されているフレームデータ
    """
    color = colors[label_name]
    label_name += " " + str(score)
    cv2.rectangle(frame, box[:2], box[2:], color, 5)
    cv2.putText(frame, label_name, (box[0], box[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [225, 255, 255], thickness=2)

    return frame
