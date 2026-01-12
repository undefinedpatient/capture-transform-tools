import bpy
from ..properties import SourceType

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
                raise RuntimeError("Unknown Source Type")
    else:
        raise RuntimeError("No active element!")
    



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
            raise RuntimeError("Unknown source type!")
    source.type = target_type