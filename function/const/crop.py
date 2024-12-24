from typing import Literal

type CropType = Literal["sugarcane", "pineapple"]
type LabelName = Literal["sugarcane", "pineapple", "weed"]

CROP_NAME_LIST: list[CropType] = ["sugarcane", "pineapple"]
SUGARCANE_LABEL_LIST: list[LabelName] = ["sugarcane", "weed"]
PINEAPPLE_LABEL_LIST: list[LabelName] = ["pineapple", "weed"]
