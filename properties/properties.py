import bpy
class ST_SnapSource(bpy.types.PropertyGroup):
    snap_source_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Snap Object"
        )

class ST_Preset(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="name", default="preset")
    snap_sources: bpy.props.CollectionProperty(
        type=ST_SnapSource,
        name="Snap Objects"
    )
    relative_location: bpy.props.FloatVectorProperty(
        name="Relative Location",
        subtype="XYZ"
    )
    relative_object: bpy.props.PointerProperty(
        type=bpy.types.Object, 
        name="Relative Object"
    )
    relative_bone: bpy.props.StringProperty(
        name="Relative Bone"
    )
    relative_vertex_group: bpy.props.StringProperty(
        name="Relative Vertex Group"
    )

class ST_PropertyGroup(bpy.types.PropertyGroup):
    presets: bpy.props.CollectionProperty(type=ST_Preset, name= "Presets")
    active_preset_index: bpy.props.IntProperty(
        name="Active Preset Index",
        default=0
    )
    relative_location: bpy.props.FloatVectorProperty(
        name="Relative Location",
        subtype="XYZ"
    )
    relative_object: bpy.props.PointerProperty(
        type=bpy.types.Object, 
        name="Relative Object"
    )


_classes = [
    ST_SnapSource,
    ST_Preset,
    ST_PropertyGroup
]


_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()
    bpy.types.Scene.snap_tools_settings = bpy.props.PointerProperty(type=ST_PropertyGroup, name="Snap Tools Settings")

def unregister():
    del bpy.types.Scene.snap_tools_settings
    _unregister()