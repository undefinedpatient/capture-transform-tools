import bpy
from mathutils import Vector, Matrix
from .types import SourceType, ApplyScope, SnapType

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
#
#
#

def capture_group(group):
    for source in group.sources:
        capture_source(group, source)

def capture_source(group, source):
    match source.type:
        case SourceType.OBJECT.name:
            relative_matrix: Matrix = get_relative_matrix(group)
            source_object: bpy.types.Object = source.source_object
            source_matrix: Matrix = source_object.matrix_world
            offset_matrix: Matrix = (source_matrix @ relative_matrix.inverted_safe())
            source.transformation = [v for col in offset_matrix.transposed() for v in col]
        case SourceType.ARMATURE.name:
            for element in source.element_bones:
                capture_element_bone(group, source, element)
        case _:
            raise RuntimeError("Unknown SourceType")
        
def capture_element(group, source, element):
    """
    Take in any element and call the corresponding capture element function.
    """
    match source.type:
        case SourceType.OBJECT.name:
            raise RuntimeError("OBJECT has no element")
        case SourceType.ARMATURE.name:
            capture_element_bone(group, source, element)

def capture_element_bone(group, source, element):
    """
    Specific implementation for bone element.
    """
    bones = source.source_object.pose.bones
    bone: bpy.types.PoseBone = bones[element.name]
    relative_matrix: Matrix = get_relative_matrix(group)
    source_matrix: Matrix = bone.matrix_basis @ source.source_object.matrix_world
    offset_matrix: Matrix = (source_matrix @ relative_matrix.inverted_safe())
    element.transformation = [v for col in offset_matrix.transposed() for v in col]
    # print("Local: \n", bone.matrix_local)
    # print("World: \n", source_matrix)
    # print("Offset: \n", offset_matrix)

def apply_group(group):
    for source in group.sources:
        apply_source(group, source)

def apply_source(group, source):
    match source.type:
        case SourceType.OBJECT.name:
            source_object: bpy.types.Object = source.source_object
            matrix = source_object.matrix_world @ get_relative_matrix(group)
            source_object.matrix_world = matrix
        case SourceType.ARMATURE.name:
            for element in source.element_bones:
                apply_element_bone(group, source, element)
        case _:
            raise RuntimeError("Unknown SourceType")

def apply_element(group, source, element):
    """
    Take in any element and call the corresponding apply element function.
    """
    match source.type:
        case SourceType.OBJECT.name:
            raise RuntimeError("OBJECT has no element")
        case SourceType.ARMATURE.name:
            apply_element_bone(group, source, element)

def apply_element_bone(group, source, element):
    source_object: bpy.types.Object = source.source_object
    bone: bpy.types.PoseBone = source_object.pose.bones[element.name]
    relative_matrix: Matrix = get_relative_matrix(group)
    matrix = element.transformation @ relative_matrix
    bone.matrix_basis = matrix



#
#
#
def get_relative_matrix(group) -> Matrix:
    match group.snap_type:
        case SnapType.LOCATION.name:
            return Matrix.Translation(group.relative_location)
        case SnapType.RELATIVE.name:
            return group.relative_object.matrix_world
        case _:
            raise RuntimeError("Unknown SnapType")