from . import properties
from .properties import SourceType, SnapType

def register():
    properties.register()

def unregister():
    properties.unregister()