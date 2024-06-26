import serial


def nozzle(frame, box):
    """
    ノズルを噴射させるための通信を行う
    :param frame: 入力された画像、動画フレーム
    :param box  : 雑草のバウンディングボックスデータ
    """

    # 雑草と認識されているバウンディングボックスの中心座標を求める
    tx = (box[0] - box[2]) * 0.5
    y = (box[1] - box[3]) * 0.5
    x = box[0] + tx
    ty = box[1] + y  # 雑草　座標　中心？

    # 現在のフレームのサイズを取得する
    h, w, c = frame.shape
    w16 = w // 16

    # 雑草の位置を認識する
    weedbox = ty // w16

    # 発射部分
    if ty <= 300 and ty <= 280:
        # 1バイト*2＝8ビット*2
        # 前半 1バイト目
        if weedbox <= 8:
            # 移動する分のビット 左シフト？
            bit = weedbox - 1
            frontbit = 0x10000000 >> bit

        # 後半 2バイト目
        else:
            bit = weedbox - 9
            backbit = 0x10000000 >> bit

        # リストにする 数値→バイナリ
        weedbyte = bytes([frontbit, backbit])

        # 送信部分
        ser = serial.Serial("COM4", 115200, timeout=None)
        ser.write(weedbyte)
        ser.close()
