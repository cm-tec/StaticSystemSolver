from enum import Enum


class Support(Enum):
    PINNED = "pinned"
    CLAMPED = "clamped"
    HORIZONTAL_ROLLER = "horizontal_roller"
    VERTICAL_ROLLER = "vertical_roller"
    NONE = "none"
