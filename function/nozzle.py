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

    # 現在の画面サイズを取得する
    h, w, c = frame.shape
    w16 = w // 16

    # 雑草の中央座標が0~16の範囲に収まるように変換
    weedbox = x // w16

    # 発射部分
    if 280 <= ty <= 300:
        frontbit = 0b00000000
        backbit = 0b00000000
        # 1バイト*2＝8ビット*2
        # 前半 1バイト目  1~8個目のノズルを制御
        if weedbox <= 8:
            # 移動する分のビットシフト
            bit = weedbox - 1
            frontbit = 0b10000000 >> bit

        # 後半 2バイト目  9~16個目のノズルを制御
        else:
            bit = weedbox - 9
            backbit = 0b10000000 >> bit

        # 制御したいノズルのビットだけ立てる
        weedbyte = bytes([frontbit, backbit])

        # 送信部分
        ser = serial.Serial("COM4", 115200, timeout=None)
        ser.write(weedbyte)
        ser.close()
