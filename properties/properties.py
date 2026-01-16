import bpy
from ..utilities import *

class CT_Element_Bone(bpy.types.PropertyGroup):
    transformation: bpy.props.FloatVectorProperty(
        name="transformation",
        size=16,
        default=(
            1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            0,0,0,1
        ),
        subtype="MATRIX"
    )
    locked: bpy.props.BoolProperty(
        name="Locked",
        default=False
    )

class CT_SnapSource(bpy.types.PropertyGroup):
    # Type of source
    type: bpy.props.EnumProperty(
        items=[
            (SourceType.OBJECT.name, "Object", "Empty", "OBJECT_DATA", 0),
            (SourceType.ARMATURE.name, "Armature", "Empty", "POSE_HLT", 1),
        ],
    )
    # The object containing the elements
    source_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Source Object",
        description="The object from which the data are taken"
        )
    # Column Major, matrix based on relative location/object
    transformation: bpy.props.FloatVectorProperty(
        name="transformation",
        size=16,
        default=(
            1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            0,0,0,1
        ),
        subtype="MATRIX"
    )
    active_element_index: bpy.props.IntProperty(
        name="Active Element Index",
        default=-1
    )
    locked: bpy.props.BoolProperty(
        name="Locked",
        default=False
    )
    #
    #   Elements
    #
    element_bones: bpy.props.CollectionProperty(
        type=CT_Element_Bone,
        name="Element Bones"
    )

class CT_Group(bpy.types.PropertyGroup):
    sources: bpy.props.CollectionProperty(
        type=CT_SnapSource,
        name="Sources"
    )
    active_source_index: bpy.props.IntProperty(
        name="Active Source Index",
        default=-1
    )
    locked: bpy.props.BoolProperty(
        name="Locked",
        default=False
    )

    # Type of snapping, either absolute location in global space, or offset with objects
    capture_type: bpy.props.EnumProperty(
        name="Snap Type",
        items=[
            (CaptureType.LOCATION.name, "Location", "Empty", "ORIENTATION_GLOBAL", 0),
            (CaptureType.RELATIVE_OBJECT.name, "Relative (Object)", "Empty", "PIVOT_ACTIVE", 1),
            (CaptureType.RELATIVE_BONE.name, "Relative (Bone)", "Empty", "BONE_DATA", 2),
        ]
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
    groups: bpy.props.CollectionProperty(type=CT_Group, name= "groups")
    active_group_index: bpy.props.IntProperty(
        name="Active group Index",
        default=-1
    )


_classes = [
    CT_Element_Bone,
    CT_SnapSource,
    CT_Group,
    ST_PropertyGroup
]


_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()
    bpy.types.Scene.capture_transform_tools_settings = bpy.props.PointerProperty(type=ST_PropertyGroup, name="Capture Tools Settings")

def unregister():
    del bpy.types.Scene.capture_transform_tools_settings
    _unregister()