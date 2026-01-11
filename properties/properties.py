import bpy
class ST_PropertyGroup(bpy.types.PropertyGroup):
    pass

_classes = [
    ST_PropertyGroup
]


_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()
    bpy.types.Scene.snap_tools_settings = bpy.props.PointerProperty(type=ST_PropertyGroup, name="Snap Tools Settings")

def unregister():
    del bpy.types.Scene.snap_tools_settings
    _unregister()