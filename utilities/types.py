from enum import Enum

class SourceType(Enum):
    OBJECT = 0,
    ARMATURE = 1,

class CaptureType(Enum):
    LOCATION = 0,
    RELATIVE_OBJECT = 1,
    RELATIVE_BONE = 2,
    # CURSOR = 2,
    # CAMERA = 3

class CaptureScope(Enum):
    PRESET = 0,
    SOURCE = 1,
    ELEMENT = 2

class ApplyScope(Enum):
    PRESET = 0,
    SOURCE = 1,
    ELEMENT = 2