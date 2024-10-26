import math
from typing import Optional

from cv2.typing import MatLike
import serial


def calc_nozzle_byte_idx(
    frame: MatLike,
    weed_bbox: list[int, int, int, int],
) -> Optional[bytes]:
    """
    雑草のバウンディングボックスデータからノズルを制御するためのバイトデータを生成する
    :param frame: 入力された画像、動画フレーム
    :param box [x0, y0, x1, y1]: 雑草のバウンディングボックスデータ

    :return weedbyte: ノズルを制御するためのバイトデータ
    """

    # 雑草と認識されているバウンディングボックスの中心座標を求める
    bbox_width = weed_bbox[2] - weed_bbox[0]
    bbox_height = weed_bbox[3] - weed_bbox[1]
    bbox_center_x = weed_bbox[0] + bbox_width * 0.5
    bbox_center_y = weed_bbox[1] + bbox_height * 0.5

    # 現在の画面サイズを取得する
    h, w, c = frame.shape
    w16 = w // 16

    # 雑草の中央座標が0~16の範囲に収まるように変換
    nozzle_index = int(bbox_center_x // w16)

    # 発射部分
    if 280 <= bbox_center_y <= 300:
        frontbit = 0b00000000
        backbit = 0b00000000
        # 1バイト*2＝8ビット*2
        # 前半 1バイト目  1~8個目のノズルを制御
        if nozzle_index <= 7:
            # 移動する分のビットシフト
            bit = nozzle_index
            frontbit = 0b10000000 >> bit

        # 後半 2バイト目  9~16個目のノズルを制御
        else:
            bit = nozzle_index - 8
            backbit = 0b10000000 >> bit

        # 制御したいノズルのビットだけ立てる
        nozzle_control_bytes = bytes([frontbit, backbit])

        return nozzle_control_bytes

    return None


def execute_nozzle(
    nozzle_control_bytes: bytes,
) -> None:
    """
    ノズルを噴射させるための通信を行う

    :param nozzle_control_bytes: ノズルを制御するためのバイトデータ
    """

    # 送信部分
    ser = serial.Serial("COM4", 115200, timeout=None)
    ser.write(nozzle_control_bytes)
    ser.close()
