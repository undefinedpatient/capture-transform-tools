import bpy

_classes = [
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()