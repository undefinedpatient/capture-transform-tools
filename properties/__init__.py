from . import properties
from .properties import SourceType

def register():
    properties.register()

def unregister():
    properties.unregister()