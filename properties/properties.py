import bpy
from ..utilities import *
class ST_SnapElement_Object(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="name", default="")
    element: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="object"
    )
    transformation: bpy.props.FloatVectorProperty(
        name="transformation",
        subtype="MATRIX"
    )

class ST_SnapElement_PoseBone(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="name", default="")
    element: bpy.props.StringProperty(
        name="bone"
    )
    transformation: bpy.props.FloatVectorProperty(
        name="transformation",
        subtype="MATRIX"
    )

class ST_SnapSource(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="name", default="source")
    # Type of source
    type: bpy.props.EnumProperty(
        items=[
            (SourceType.OBJECT.name, "Object", "Empty", "OBJECT_DATA", 0),
            (SourceType.ARMATURE.name, "Armature", "Empty", "POSE_HLT", 1),
        ],
    )
    # Type of snapping, either absolute location in global space, or offset with objects
    snap_type: bpy.props.EnumProperty(
        items=[
            (SnapType.LOCATION.name, "Location", "Empty", "ORIENTATION_GLOBAL", 0),
            (SnapType.RELATIVE.name, "Relative", "Empty", "PIVOT_ACTIVE", 1),
        ]
    )
    # The object containing the elements
    source_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="The object from which the data are taken"
        )
    active_element_index: bpy.props.IntProperty(
        name="Active Element Index",
        default=-1
    )

    #
    #   Elements
    #
    element_objects: bpy.props.CollectionProperty(
        type=ST_SnapElement_Object,
        name="Element Objects"
    )
    element_bones: bpy.props.CollectionProperty(
        type=ST_SnapElement_PoseBone,
        name="Elemenet Bones"
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

class ST_Group(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="name", default="group")
    sources: bpy.props.CollectionProperty(
        type=ST_SnapSource,
        name="Sources"
    )
    active_source_index: bpy.props.IntProperty(
        name="Active Source Index",
        default=-1
    )

class ST_PropertyGroup(bpy.types.PropertyGroup):
    groups: bpy.props.CollectionProperty(type=ST_Group, name= "groups")
    active_group_index: bpy.props.IntProperty(
        name="Active group Index",
        default=-1
    )


_classes = [
    ST_SnapElement_Object,
    ST_SnapElement_PoseBone,
    ST_SnapSource,
    ST_Group,
    ST_PropertyGroup
]


_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()
    bpy.types.Scene.snap_tools_settings = bpy.props.PointerProperty(type=ST_PropertyGroup, name="Snap Tools Settings")

def unregister():
    del bpy.types.Scene.snap_tools_settings
    _unregister()