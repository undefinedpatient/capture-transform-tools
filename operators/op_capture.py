import bpy
from mathutils import Vector, Matrix
from ..utilities import *

class CT_OT_snap(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap"
    bl_label = "Snap"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    apply_scope: bpy.props.EnumProperty(
        items=[
            (ApplyScope.PRESET.name, "Preset", "Empty", "OUTLINER_COLLECTION", 0),
            (ApplyScope.SOURCE.name, "Source", "Empty", "OBJECT_DATA", 1),
            (ApplyScope.ELEMENT.name, "Element", "Empty", "STICKY_UVS_DISABLE", 2)
        ]
    )
    def execute(self, context):
        if not has_active_group(context):
            return {"FINISHED"}
        active_group = get_active_group(context)
        match self.apply_scope:
            case ApplyScope.PRESET.name:
                apply_group(active_group)
            case ApplyScope.SOURCE.name:
                if not has_active_source(context):
                    return {"FINISHED"}
                active_source = get_active_source(context)
                apply_source(active_group, active_source)
            case ApplyScope.ELEMENT.name:
                if not has_active_element(context):
                    return {"FINISHED"}
                active_source = get_active_source(context)
                active_element = get_active_element(context)
                apply_element(active_group, active_source, active_element)
        return {"FINISHED"}

class CT_OT_capture(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.capture"
    bl_label = "Capture"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    capture_scope: bpy.props.EnumProperty(
        items=[
            (CaptureScope.PRESET.name, "Preset", "Empty", "OUTLINER_COLLECTION", 0),
            (CaptureScope.SOURCE.name, "Source", "Empty", "OBJECT_DATA", 1),
            (CaptureScope.ELEMENT.name, "Element", "Empty", "STICKY_UVS_DISABLE", 2)
        ]
    )

    def execute(self, context):
        if not has_active_group(context):
            return {"FINISHED"}
        active_group = get_active_group(context)
        match self.capture_scope:
            case CaptureScope.PRESET.name:
                capture_group(active_group)
            case CaptureScope.SOURCE.name:
                if not has_active_source(context):
                    return {"FINISHED"}
                active_source = get_active_source(context)
                capture_source(active_group, active_source)
            case CaptureScope.ELEMENT.name:
                if not has_active_element(context):
                    return {"FINISHED"}
                active_source = get_active_source(context)
                active_element = get_active_element(context)
                capture_element(active_group, active_source, active_element)
        return {"FINISHED"}

class CT_OT_snap_group_add(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap_group_add"
    bl_label = "Capture Group Add"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.capture_global_transform_tools_settings
        new_group = props.groups.add()
        new_group.name = get_unqiue_name_from_list("group", list(map(lambda g: g.name,props.groups)))
        # If it is a newly added group, set the active group index to 0
        if len(props.groups) == 1:
            props.active_group_index = 0
        return {"FINISHED"}

class CT_OT_snap_source_add(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap_source_add"
    bl_label = "Capture Source Add"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    is_blank: bpy.props.BoolProperty(
        name="Is Blank",
        default=True
    )
    only_active: bpy.props.BoolProperty(
        name="Only Active",
        default=False
    )

    def execute(self, context):
        props = context.scene.capture_global_transform_tools_settings

        if len(props.groups) == 0:
            self.report(type={"INFO"}, message="No Group exist, created one.")
            bpy.ops.capture_global_transform_tools.snap_group_add()
        active_group_index = props.active_group_index
        active_group = props.groups[active_group_index]

        # If previously the source list is empty, set selection to 0
        if active_group.active_source_index == -1:
            active_group.active_source_index = 0

        if not self.is_blank:
            if len(context.selected_objects) == 0:
                self.report(type={"WARNING"}, message="No selected object!")
                active_group.active_source_index = -1
                return {"FINISHED"}
            # Adding object(s) to the group
            if self.only_active:
                source = active_group.sources.add()
                source.name = context.active_object.name
                source.source_object = context.active_object
            else:
                for o in context.selected_objects:
                    source = active_group.sources.add()
                    source.name = o.name
                    source.source_object = o
        else:
            # Empty as source here
            source = active_group.sources.add()
            source.name = get_unqiue_name_from_list("source", list(map(lambda s: s.name, active_group.sources)))

        return {"FINISHED"}

class CT_OT_snap_element_add(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap_element_add"
    bl_label = "Capture Source Add Elements"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    is_blank: bpy.props.BoolProperty(
        name="Is Blank",
        default=True
    )
    only_active: bpy.props.BoolProperty(
        name="Only Active",
        default=False
    )
    # User should not be abled to select the type of element, so take it from scene
    def execute(self, context):
        props = context.scene.capture_global_transform_tools_settings
        active_group = props.groups[props.active_group_index]
        active_source = active_group.sources[active_group.active_source_index]
        source_object: bpy.types.Object = active_source.source_object
        match active_source.type:
            case SourceType.ARMATURE.name:
                if not self.is_blank:
                    if context.mode == "POSE":
                        if self.only_active:
                            bone = context.active_pose_bone
                            if bone:
                                element = active_source.element_bones.add()
                                element.name = bone.name
                        else:
                            all_selected_bones = set()
                            bones_in_source_object = set()
                            for bone in source_object.pose.bones:
                                bones_in_source_object.add(bone)
                            for bone in source_object.pose.bones:
                                if bone.select:
                                    all_selected_bones.add(bone)
                            
                            bones_to_add = all_selected_bones.intersection(bones_in_source_object)
                            for bone in bones_to_add:
                                element = active_source.element_bones.add()
                                element.name = bone.name

                    else:
                        self.report({"INFO"}, message="Adding bones only works in Pose mode.")
                else:
                    active_source.element_bones.add()

        return {"FINISHED"}

class CT_OT_snap_group_remove(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap_group_remove"
    bl_label = "Capture group Remove"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.capture_global_transform_tools_settings
        if not has_active_group(context):
            return {"FINISHED"}
        active_group_index = props.active_group_index
        props.active_group_index -= 1
        props.groups.remove(active_group_index)
        return {"FINISHED"}
    
class CT_OT_snap_source_remove(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap_source_remove"
    bl_label = "Capture Source Remove"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.capture_global_transform_tools_settings
        if not has_active_source(context):
            return {"FINISHED"}
        if len(props.groups) == 0 or len(props.groups[props.active_group_index].sources) == 0:
            return {"FINISHED"}
        active_group = props.groups[props.active_group_index]
        active_source_index = active_group.active_source_index

        props.groups[props.active_group_index].active_source_index -= 1

        active_group.sources.remove(active_source_index)

        return {"FINISHED"}

class CT_OT_snap_element_remove(bpy.types.Operator):
    bl_idname = "capture_global_transform_tools.snap_element_remove"
    bl_label = "Capture Source Remove Elements"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    def execute(self, context):
        if not has_active_element(context):
            return {"FINISHED"}
        source = get_active_source(context)
        match source.type:
            case SourceType.OBJECT.name:
                source.element_objects.remove(get_active_element_index(context))
            case SourceType.ARMATURE.name:
                source.element_bones.remove(get_active_element_index(context))
        source.active_element_index -= 1
        return {"FINISHED"}

_classes = [
    CT_OT_snap,
    CT_OT_capture,
    CT_OT_snap_group_add,
    CT_OT_snap_source_add,
    CT_OT_snap_element_add,
    CT_OT_snap_group_remove,
    CT_OT_snap_source_remove,
    CT_OT_snap_element_remove
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()