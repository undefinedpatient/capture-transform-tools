import bpy

from .types import SourceType

def get_active_group_index(context: bpy.types.Context) -> int:
    return context.scene.snap_tools_settings.active_group_index

def has_active_group(context:bpy.types.Context) -> bool:
    return get_active_group_index(context) != -1

def get_active_group(context:bpy.types.Context):
    if has_active_group(context):
        return context.scene.snap_tools_settings.groups[get_active_group_index(context)]
    else:
        raise RuntimeError("No active group!")
    
def get_active_source_index(context: bpy.types.Context) -> int:
    group = get_active_group(context)
    return group.active_source_index

def has_active_source(context: bpy.types.Context) -> bool:
    if not has_active_group(context):
        return False
    return get_active_source_index(context) != -1

def get_active_source(context: bpy.types.Context):
    if has_active_source(context):
        return get_active_group(context).sources[get_active_source_index(context)]
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
            case SourceType.ARMATURE.name:
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
        case SourceType.ARMATURE.name:
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
        case SourceType.ARMATURE.name:
            if len(source.element_bones) <= source.active_element_index:
                source.active_element_index = len(source.element_bones) - 1
        case _:
            raise RuntimeError("Unknown SourceType!")
    source.type = target_type


def get_unqiue_name_from_list(name: str, list: list[str]) -> str:
    new_name: str = name
    occurance: int = 0
    while new_name in list:
        occurance += 1
        suffix = "." + str(occurance).rjust(3, '0')
        new_name = name + suffix
    return new_name
