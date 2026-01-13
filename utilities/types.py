from enum import Enum

class SourceType(Enum):
    OBJECT = 0,
    ARMATURE = 1,

class SnapType(Enum):
    LOCATION = 0,
    RELATIVE = 1,
    CURSOR = 2,
    CAMERA = 3