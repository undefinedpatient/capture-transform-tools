import bpy
from mathutils import Vector, Matrix
from .types import SourceType, ApplyScope, CaptureType

def get_active_group_index(context: bpy.types.Context) -> int:
    return context.scene.capture_transform_tools_settings.active_group_index

def has_active_group(context:bpy.types.Context) -> bool:
    return get_active_group_index(context) != -1

def get_active_group(context:bpy.types.Context):
    if has_active_group(context):
        return context.scene.capture_transform_tools_settings.groups[get_active_group_index(context)]
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
    if not has_active_element(context):
        raise RuntimeError("No active element!")
    source = get_active_source(context)
    match source.type:
        case SourceType.OBJECT.name:
            return source.element_objects[get_active_element_index(context)]
        case SourceType.ARMATURE.name:
            return source.element_bones[get_active_element_index(context)]
        case _:
            raise RuntimeError("Unknown SourceType")

def get_element_list_from_active_source(source) -> list:
    match source.type:
        case SourceType.OBJECT.name:
            return [source.source_object]
        case SourceType.ARMATURE.name:
            return source.element_bones
        case _:
            raise RuntimeError("Unknown SourceType")


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
        if is_source_valid(source):
            capture_source(group, source)

def capture_source(group, source):
    match source.type:
        case SourceType.OBJECT.name:
            relative_matrix: Matrix = get_relative_matrix(group)
            source_object: bpy.types.Object = source.source_object
            source_matrix: Matrix = source_object.matrix_world
            offset_matrix: Matrix = (relative_matrix.inverted_safe() @ source_matrix)
            # print(offset_matrix)
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
    source_object: bpy.types.Object = source.source_object
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = source_object.evaluated_get(depsgraph)
    pose_bone: bpy.types.PoseBone = eval_obj.pose.bones[element.name]

    relative_matrix: Matrix = get_relative_matrix(group)
    armature_matrix: Matrix = pose_bone.matrix
    world_matrix: Matrix = eval_obj.matrix_world
    global_matrix: Matrix = world_matrix @ armature_matrix
    offset_matrix: Matrix = relative_matrix.inverted_safe() @ global_matrix

    element.transformation = [v for col in offset_matrix.transposed() for v in col]
    # print("Local: \n", armature_matrix)
    print("Global: \n", global_matrix)
    print("basis:\n", pose_bone.matrix_basis)
    # print("Offset: \n", offset_matrix)

def apply_group(group, should_insert_keyframe: bool = True):
    for source in group.sources:
        if is_source_valid(source):
            apply_source(group, source, should_insert_keyframe)

def apply_source(group, source, should_insert_keyframe: bool = True):
    match source.type:
        case SourceType.OBJECT.name:
            source_object: bpy.types.Object = source.source_object
            global_matrix: Matrix = source.transformation
            source_object.matrix_world = global_matrix

            bpy.context.view_layer.update()
            constraint_offset = global_matrix @ source_object.matrix_world.inverted_safe()
            source_object.matrix_world = constraint_offset @ get_relative_matrix(group) @ global_matrix
            
            bpy.context.view_layer.update()
            if should_insert_keyframe:
                source_object.keyframe_insert(
                    "location",
                    index=-1,
                    group="baked capture",
                    keytype="KEYFRAME"
                    )
                source_object.keyframe_insert(
                    "rotation_quaternion",
                    index=-1,
                    group="baked capture",
                    keytype="KEYFRAME"
                    )
                source_object.keyframe_insert(
                    "scale",
                    index=-1,
                    group="baked capture",
                    keytype="KEYFRAME"
                    )

        case SourceType.ARMATURE.name:
            for element in source.element_bones:
                apply_element_bone(group, source, element, should_insert_keyframe)
        case _:
            raise RuntimeError("Unknown SourceType")

def apply_element(group, source, element, should_insert_keyframe: bool = False):
    """
    Take in any element and call the corresponding apply element function.
    """
    match source.type:
        case SourceType.OBJECT.name:
            raise RuntimeError("OBJECT has no element")
        case SourceType.ARMATURE.name:
            apply_element_bone(group, source, element, should_insert_keyframe)

def apply_element_bone(group, source, element, should_insert_keyframe: bool = False):
    source_object: bpy.types.Object = source.source_object
    pose_bone: bpy.types.PoseBone = source_object.pose.bones[element.name]
    global_matrix: Matrix = element.transformation
    arm_matrix: Matrix = source_object.matrix_world.inverted_safe() @ global_matrix


    pose_bone.matrix = arm_matrix
    bpy.context.view_layer.update()
    constraint_offset = arm_matrix @ pose_bone.matrix.inverted_safe()
    pose_bone.matrix = constraint_offset @ get_relative_matrix(group) @ arm_matrix
    bpy.context.view_layer.update()
    # if pose_bone.parent == None:
    #     local_pose = pose_bone.bone.matrix_local.inverted_safe() @ arm_matrix
    #     local_constraint: Matrix = pose_bone.matrix_basis.inverted_safe() @ pose_bone.matrix
    #     pose_bone.matrix = local_constraint.inverted_safe() @ local_pose
    # else:
    #     # Get how much parent bone move relatively to target bone, if target bone has parent
    #     parent_rest: Matrix = pose_bone.parent.bone.matrix_local.copy()
    #     parent_pose: Matrix = pose_bone.parent.matrix.copy()
    #     parent_delta: Matrix =  parent_rest.inverted_safe() @ parent_pose
    #     print("parent_delta:\n", parent_delta)
    #     local_pose: Matrix = pose_bone.bone.matrix_local.inverted_safe() @ arm_matrix
    #     local_constraint: Matrix = pose_bone.matrix_basis.inverted_safe() @ pose_bone.matrix
    #     pose_bone.matrix = local_constraint.inverted_safe() @ parent_delta @ local_pose
    if should_insert_keyframe:
        pose_bone.keyframe_insert(
            "location",
            index=-1,
            group="baked capture",
            keytype="KEYFRAME"
            )
        pose_bone.keyframe_insert(
            "rotation_quaternion",
            index=-1,
            group="baked capture",
            keytype="KEYFRAME"
            )
        pose_bone.keyframe_insert(
            "scale",
            index=-1,
            group="baked capture",
            keytype="KEYFRAME"
            )

def get_relative_matrix(group) -> Matrix:
    match group.capture_type:
        case CaptureType.LOCATION.name:
            return Matrix.Translation(group.relative_location)
        case CaptureType.RELATIVE_OBJECT.name:
            return group.relative_object.matrix_world
        case CaptureType.RELATIVE_BONE.name:
            relative_object: bpy.types.Object = group.relative_object
            relative_bone: bpy.types.PoseBone = relative_object.pose.bones[group.relative_bone]
            return relative_bone.matrix
        case _:
            raise RuntimeError("Unknown SnapType")
        
#
#   Validation
#
def is_source_valid(source) -> bool:
    match source.type:
        case SourceType.OBJECT.name:
            return source.source_object != None
        case SourceType.ARMATURE.name:
            return source.source_object != None and source.source_object.type == "ARMATURE"
    return False

def is_bone_element_valid(element, parent_source) -> bool:
    return element.name in list(map(lambda bone: bone.name, parent_source.source_object.pose.bones))

def is_group_settings_valid(group) -> bool:
    match group.capture_type:
        case CaptureType.LOCATION.name:
            return True
        case CaptureType.RELATIVE_OBJECT.name:
            return group.relative_object != None
        case CaptureType.RELATIVE_BONE.name:
            if group.relative_object == None:
                return False
            if group.relative_object.type != "ARMATURE" or group.relative_bone == "":
                return False
            return True
    return False 