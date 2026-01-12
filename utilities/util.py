import bpy

from .types import SourceType

def get_active_preset_index(context: bpy.types.Context) -> int:
    return context.scene.snap_tools_settings.active_preset_index

def has_active_preset(context:bpy.types.Context) -> bool:
    return get_active_preset_index(context) != -1

def get_active_preset(context:bpy.types.Context):
    if has_active_preset(context):
        return context.scene.snap_tools_settings.presets[get_active_preset_index(context)]
    else:
        raise RuntimeError("No active preset!")
    
def get_active_source_index(context: bpy.types.Context) -> int:
    preset = get_active_preset(context)
    return preset.active_source_index

def has_active_source(context: bpy.types.Context) -> bool:
    if not has_active_preset(context):
        return False
    return get_active_source_index(context) != -1

def get_active_source(context: bpy.types.Context):
    if has_active_source(context):
        return get_active_preset(context).sources[get_active_source_index(context)]
    else:
        raise RuntimeError("No active source!")

def get_active_element_index(context:bpy.types.Context) -> int:
    return get_active_source(context).active_element_index

def has_active_element(context: bpy.types.Context) -> bool:
    if not has_active_source(context):
        return False
    return get_active_element_index(context) != -1

def get_active_element(context: bpy.types.Context):
    if has_active_element(context):
        source = get_active_source(context)
        match source.type:
            case SourceType.OBJECT.name:
                return source.element_objects[get_active_element_index(context)]
            case SourceType.POSE_BONE.name:
                return source.element_bones[get_active_element_index(context)]
            case _:
                raise RuntimeError("Unknown SourceType")
    else:
        raise RuntimeError("No active element!")
    

def has_source_object(source)->bool:
    return source.source_object != None
def is_source_type_valid(source) -> bool:
    """
    In case user select "POSE_BONE" for non-armature object, have to check it
    """
    match source.type:
        case SourceType.OBJECT.name:
            return True
        case SourceType.POSE_BONE.name:
            return source.source_object.type == "ARMATURE"
        case _:
            raise RuntimeError("Unknow SourceType")

def switch_source_type(source, target_type: SourceType):
    match target_type:
        # Switch to OBJECT
        case SourceType.OBJECT.name:
            if len(source.element_objects) <= source.active_element_index:
                source.active_element_index = len(source.element_objects) - 1
        # Switch to POSE_BONE
        case SourceType.POSE_BONE.name:
            if len(source.element_bones) <= source.active_element_index:
                source.active_element_index = len(source.element_bones) - 1
        case _:
            raise RuntimeError("Unknown SourceType!")
    source.type = target_type