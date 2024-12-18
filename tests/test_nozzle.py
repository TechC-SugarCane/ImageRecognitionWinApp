import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../function"))

from nozzle import calc_nozzle_byte_idx
import pytest

# 疑似フレームのサイズ
FRAME_SIZE = (640, 640, 3)


# テストをパラメータ化
@pytest.mark.parametrize(
    "weed_bbox, expected_output",
    [
        # bboxの中央が0~16に収まるパターン
        ([0, 280, 40, 300], bytes([0b10000000, 0b00000000])),  # ノズル1
        ([40, 280, 80, 300], bytes([0b01000000, 0b00000000])),  # ノズル2
        ([80, 280, 120, 300], bytes([0b00100000, 0b00000000])),  # ノズル3
        ([120, 280, 160, 300], bytes([0b00010000, 0b00000000])),  # ノズル4
        ([160, 280, 200, 300], bytes([0b00001000, 0b00000000])),  # ノズル5
        ([200, 280, 240, 300], bytes([0b00000100, 0b00000000])),  # ノズル6
        ([240, 280, 280, 300], bytes([0b00000010, 0b00000000])),  # ノズル7
        ([280, 280, 320, 300], bytes([0b00000001, 0b00000000])),  # ノズル8
        ([320, 280, 360, 300], bytes([0b00000000, 0b10000000])),  # ノズル9
        ([360, 280, 400, 300], bytes([0b00000000, 0b01000000])),  # ノズル10
        ([400, 280, 440, 300], bytes([0b00000000, 0b00100000])),  # ノズル11
        ([440, 280, 480, 300], bytes([0b00000000, 0b00010000])),  # ノズル12
        ([480, 280, 520, 300], bytes([0b00000000, 0b00001000])),  # ノズル13
        ([520, 280, 560, 300], bytes([0b00000000, 0b00000100])),  # ノズル14
        ([560, 280, 600, 300], bytes([0b00000000, 0b00000010])),  # ノズル15
        ([600, 280, 640, 300], bytes([0b00000000, 0b00000001])),  # ノズル16
        # bboxが範囲外（y座標が280未満）の場合はNoneが返る
        ([0, 200, 40, 250], None),
        # bboxが範囲外（y座標が300超過）の場合はNoneが返る
        ([0, 310, 40, 350], None),
    ],
)
def test_calc_nozzle_byte_idx(weed_bbox, expected_output):
    """
    calc_nozzle_byte_idx関数の出力が期待通りか確認するテスト
    """
    result = calc_nozzle_byte_idx(FRAME_SIZE, weed_bbox)
    assert result == expected_output
