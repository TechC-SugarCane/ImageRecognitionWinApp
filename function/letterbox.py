from typing import Tuple

import cv2
import numpy as np


def letterbox(
    im: np.ndarray,
    new_shape: Tuple[int, int] = (640, 640),
    color: Tuple[int, int, int] = (114, 114, 114),
    auto: bool = True,
    scaleup: bool = True,
    stride: int = 32,
) -> Tuple[np.ndarray, float, Tuple[float, float]]:
    """
    画像をリサイズしてパディングする
    :param im        : 画像データ
    :param new_shape : リサイズ後の画像サイズ
    :param color     : パディングするときの色
    :param auto      : 自動でパディングするかどうか
    :param scaleup   : スケールアップするかどうか
    :param stride    : ストライドの大きさ

    :return im       : パディングされた画像データ
    :return r        : リサイズ後の画像サイズとリサイズ前の画像サイズの比率
    :return (dw, dh) : パディングした分の画像サイズ
    """
    # 画像のリサイズとパディングを行う
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # 大きさの比率を計算する (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # パディングするときの画像サイズを計算する
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    half_dw = dw / 2  # divide padding into 2 sides
    half_dh = dh / 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(half_dh - 0.1)), int(round(half_dh + 0.1))
    left, right = int(round(half_dw - 0.1)), int(round(half_dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (half_dw, half_dh)
