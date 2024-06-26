from enum import Enum


class DesignParameterElement(Enum):
    EA = "EA"
    EI = "EI"
    LENGTH = "l"
    QX = "q_x"
    QZ = "q_z"


class DesignParameterNode(Enum):
    FX = "FX"
    FZ = "FZ"
    MY = "MY"
