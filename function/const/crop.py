from typing import Literal

type CropType = Literal["sugarcane", "pineapple"]
type LabelName = Literal["weed"]

CROP_NAME_LIST: list[CropType] = ["sugarcane", "pineapple"]
# メンテナンス性を考慮して、各作物のラベル名を管理
SUGARCANE_LABEL_LIST: list[LabelName] = ["weed"]
PINEAPPLE_LABEL_LIST: list[LabelName] = ["weed"]
