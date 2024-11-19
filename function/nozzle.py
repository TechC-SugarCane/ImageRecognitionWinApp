from typing import Optional

import serial
import serial.tools.list_ports

def find_serial_port(vid: str, pid: str) -> Optional[str]:
    """
    デバイスのVIDとPIDを使用してシリアルポートを検出する
    :param vid: デバイスのVID
    :param pid: デバイスのPID

    :return: 検出されたシリアルポートの名前
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == int(vid, 16) and port.pid == int(pid, 16):
            return port.device
    return None

def calc_nozzle_byte_idx(
    image_shape: tuple[int, int, int],
    weed_bbox: list[int],
) -> Optional[bytes]:
    """
    雑草のバウンディングボックスデータからノズルを制御するためのバイトデータを生成する
    :param image_shape [h, w, c]: 画像のサイズ
    :param box [x0, y0, x1, y1]: 雑草のバウンディングボックスデータ

    :return weedbyte: ノズルを制御するためのバイトデータ
    """

    # 雑草と認識されているバウンディングボックスの中心座標を求める
    bbox_width = weed_bbox[2] - weed_bbox[0]
    bbox_height = weed_bbox[3] - weed_bbox[1]
    bbox_center_x = weed_bbox[0] + bbox_width * 0.5
    bbox_center_y = weed_bbox[1] + bbox_height * 0.5

    # 現在の画面サイズを取得する
    h, w, c = image_shape
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

    # 自動でシリアルポートを認識して接続する
    vid = "0x0483"
    pid = "0x5740"
    port = find_serial_port(vid, pid)
    if port is None:
        raise Exception("No serial port found for the given VID and PID")

    # 送信部分
    ser = serial.Serial(port, 115200, timeout=None)
    ser.write(nozzle_control_bytes)
    ser.close()
