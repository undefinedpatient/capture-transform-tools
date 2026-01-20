import bpy
from mathutils import Vector, Matrix
from ..utilities import *

class CT_OT_apply(bpy.types.Operator):
    bl_idname = "capture_transform_tools.apply"
    bl_label = "Apply"
    bl_options = {"UNDO"}
    bl_description = "Empty"
    apply_scope: bpy.props.EnumProperty(
        items=[
            (ApplyScope.GROUP.name, "Preset", "Empty", "OUTLINER_COLLECTION", 0),
            (ApplyScope.SOURCE.name, "Source", "Empty", "OBJECT_DATA", 1),
            (ApplyScope.ELEMENT.name, "Element", "Empty", "STICKY_UVS_DISABLE", 2)
        ]
    )
    should_insert_keyframe: bpy.props.BoolProperty(
        name="Insert Keyframe",
        default=False
    )
    def execute(self, context):
        if not has_active_group(context):
            self.report(type={"WARNING"}, message="No group selected!")
            return {"CANCELLED"}
        active_group = get_active_group(context)
        if not is_group_settings_valid(active_group):
            self.report(type={"WARNING"}, message="Invalid Group Setting!")
            return {"CANCELLED"}
        match self.apply_scope:
            case ApplyScope.GROUP.name:
                if len(active_group.sources) == 0:
                    self.report(type={"INFO"}, message="Empty Group")
                    return {"CANCELLED"}
                apply_group(active_group, self.should_insert_keyframe)
            case ApplyScope.SOURCE.name:
                if not has_active_source(context):
                    self.report(type={"INFO"}, message="No source selected!")
                    return {"CANCELLED"}
                active_source = get_active_source(context)
                if not is_source_valid(active_source):
                    self.report(type={"WARNING"}, message="Invalid source!")
                    return {"CANCELLED"}
                apply_source(active_group, active_source, self.should_insert_keyframe)

            case ApplyScope.ELEMENT.name:
                if not has_active_element(context):
                    self.report(type={"WARNING"}, message="No element selected!")
                    return {"CANCELLED"}
                active_source = get_active_source(context)
                active_element = get_active_element(context)
                apply_element(active_group, active_source, active_element, self.should_insert_keyframe)
        return {"FINISHED"}

class CT_OT_capture(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture"
    bl_label = "Capture"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    capture_scope: bpy.props.EnumProperty(
        items=[
            (CaptureScope.GROUP.name, "Preset", "Empty", "OUTLINER_COLLECTION", 0),
            (CaptureScope.SOURCE.name, "Source", "Empty", "OBJECT_DATA", 1),
            (CaptureScope.ELEMENT.name, "Element", "Empty", "STICKY_UVS_DISABLE", 2)
        ]
    )

    def execute(self, context):
        if not has_active_group(context):
            return {"CANCELLED"}
        active_group = get_active_group(context)
        if not is_group_settings_valid(active_group):
            self.report(type={"WARNING"}, message="Invalid Group Setting!")
            return {"CANCELLED"}
        match self.capture_scope:
            case CaptureScope.GROUP.name:
                if len(active_group.sources) == 0:
                    self.report(type={"INFO"}, message="Empty Group")
                    return {"CANCELLED"}
                capture_group(active_group)

            case CaptureScope.SOURCE.name:
                if not has_active_source(context):
                    self.report(type={"INFO"}, message="No source selected!")
                active_source = get_active_source(context)
                if not is_source_valid(active_source):
                    self.report(type={"WARNING"}, message="Invalid source!")
                    return {"CANCELLED"}
                capture_source(active_group, active_source)

            case CaptureScope.ELEMENT.name:
                if not has_active_element(context):
                    return {"FINISHED"}
                active_source = get_active_source(context)
                active_element = get_active_element(context)
                capture_element(active_group, active_source, active_element)

        return {"FINISHED"}

class CT_OT_capture_group_add(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_group_add"
    bl_label = "Capture Group Add"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.capture_transform_tools_settings
        new_group = props.groups.add()
        new_group.name = get_unqiue_name_from_list("group", list(map(lambda g: g.name,props.groups)))
        # If it is a newly added group, set the active group index to 0
        if len(props.groups) == 1:
            props.active_group_index = 0
        return {"FINISHED"}

class CT_OT_capture_source_add(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_source_add"
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
        props = context.scene.capture_transform_tools_settings

        if len(props.groups) == 0:
            self.report(type={"INFO"}, message="No Group exist, created one.")
            bpy.ops.capture_transform_tools.capture_group_add()
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

        return {"FINISHED"}

class CT_OT_capture_element_add(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_element_add"
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
        props = context.scene.capture_transform_tools_settings
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
                    element = active_source.element_bones.add()
        return {"FINISHED"}

class CT_OT_capture_group_remove(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_group_remove"
    bl_label = "Capture group Remove"
    bl_options = {"UNDO"}
    bl_description = "Empty"

    remove_all: bpy.props.BoolProperty(
        name="Remove All",
        default=False
    )

    def execute(self, context):
        props = context.scene.capture_transform_tools_settings
        # When user clicked "Remove All Unlocked"
        if self.remove_all:
            for i in range(len(props.groups)-1, -1, -1):
                if props.groups[i].locked:
                    continue
                props.groups.remove(i)

            if len(props.groups) == 0:
                props.active_group_index = -1
            else:
                props.active_group_index = 0
            return {"FINISHED"}
        # When no active group selected
        if not has_active_group(context):
            return {"FINISHED"}
        active_group_index = props.active_group_index
        # When active group is locked
        if props.groups[active_group_index].locked:
            self.report(type={"INFO"}, message="Group is locked!")
            return {"FINISHED"}
        props.active_group_index -= 1
        props.groups.remove(active_group_index)
        return {"FINISHED"}
    
class CT_OT_capture_source_remove(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_source_remove"
    bl_label = "Capture Source Remove"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    remove_all: bpy.props.BoolProperty(
        name="Remove All",
        default=False
    )

    def execute(self, context):
        props = context.scene.capture_transform_tools_settings
        active_group = get_active_group(context)
        # When user clicked "Remove All Unlocked"
        if self.remove_all:
            for i in range(len(active_group.sources)-1, -1, -1):
                if active_group.sources[i].locked:
                    continue
                active_group.sources.remove(i)

            if len(active_group.sources) == 0:
                active_group.active_source_index = -1
            else:
                active_group.active_source_index = 0
            return {"FINISHED"}
        # When no active source exist
        if not has_active_source(context):
            return {"FINISHED"}
        # When active source is locked
        if get_active_source(context).locked:
            return {"FINISHED"}
        if len(props.groups) == 0 or len(props.groups[props.active_group_index].sources) == 0:
            return {"FINISHED"}
        active_source_index = active_group.active_source_index
        active_group.active_source_index -= 1
        active_group.sources.remove(active_source_index)

        return {"FINISHED"}

class CT_OT_capture_element_remove(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_element_remove"
    bl_label = "Capture Source Remove Elements"
    bl_options = {"UNDO"}
    bl_description = "Empty"
    
    remove_all: bpy.props.BoolProperty(
        name="Remove All",
        default=False
    )

    def execute(self, context):
        if not has_active_source(context):
            return {"FINISHED"}
        source = get_active_source(context)
        element_list = get_element_list_from_active_source(source)
        # When user clicked "Remove All Unlocked"
        if self.remove_all:
            for i in range(len(element_list)-1, -1, -1):
                if element_list[i].locked:
                    continue
                element_list.remove(i)

            if len(element_list) == 0:
                source.active_element_index = -1
            else:
                source.active_element_index = 0
            return {"FINISHED"}
        # When no active element exist
        if not has_active_element(context):
            return {"FINISHED"}

        active_element = get_active_element(context)
        match source.type:
            case SourceType.OBJECT.name:
                source.element_objects.remove(get_active_element_index(context))
            case SourceType.ARMATURE.name:
                source.element_bones.remove(get_active_element_index(context))
        source.active_element_index -= 1
        return {"FINISHED"}

class CT_OT_capture_group_lock(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_group_lock"
    bl_label = "Capture Group Lock"
    bl_options = {"UNDO"}
    bl_description = "Empty"

    actions: bpy.props.EnumProperty(
        items=[
            (LockAction.LOCK.name, "Lock", "Empty", "LOCKED", 0),
            (LockAction.UNLOCK.name, "Unlock", "Empty", "UNLOCKED", 1),
            (LockAction.INVERT.name, "Invert Lock", "Empty", "NONE", 2),
        ]
    )

    def execute(self, context):
        match self.actions:
            case LockAction.LOCK.name:
                for group in context.scene.capture_transform_tools_settings.groups:
                    group.locked = True
            case LockAction.UNLOCK.name:
                for group in context.scene.capture_transform_tools_settings.groups:
                    group.locked = False
            case LockAction.INVERT.name:
                for group in context.scene.capture_transform_tools_settings.groups:
                    group.locked = not group.locked
        return {"FINISHED"}

class CT_OT_capture_source_lock(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_source_lock"
    bl_label = "Capture Source Lock"
    bl_options = {"UNDO"}
    bl_description = "Empty"

    actions: bpy.props.EnumProperty(
        items=[
            (LockAction.LOCK.name, "Lock", "Empty", "LOCKED", 0),
            (LockAction.UNLOCK.name, "Unlock", "Empty", "UNLOCKED", 1),
            (LockAction.INVERT.name, "Invert Lock", "Empty", "NONE", 2),
        ]
    )

    def execute(self, context):
        active_group = get_active_group(context)
        match self.actions:
            case LockAction.LOCK.name:
                for source in active_group.sources:
                    source.locked = True
            case LockAction.UNLOCK.name:
                for source in active_group.sources:
                    source.locked = False
            case LockAction.INVERT.name:
                for source in active_group.sources:
                    source.locked = not source.locked

        return {"FINISHED"}

class CT_OT_capture_element_lock(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_element_lock"
    bl_label = "Capture element Lock"
    bl_options = {"UNDO"}
    bl_description = "Empty"

    actions: bpy.props.EnumProperty(
        items=[
            (LockAction.LOCK.name, "Lock", "Empty", "LOCKED", 0),
            (LockAction.UNLOCK.name, "Unlock", "Empty", "UNLOCKED", 1),
            (LockAction.INVERT.name, "Invert Lock", "Empty", "NONE", 2),
        ]
    )

    def execute(self, context):
        active_source = get_active_source(context)
        element_list = get_element_list_from_active_source(active_source)
        match self.actions:
            case LockAction.LOCK.name:
                for element in element_list:
                    element.locked = True
            case LockAction.UNLOCK.name:
                for element in element_list:
                    element.locked = False
            case LockAction.INVERT.name:
                for element in element_list:
                    element.locked = not element.locked

        return {"FINISHED"}

class CT_OT_remove_duplicated_elements(bpy.types.Operator):
    bl_idname = "capture_transform_tools.remove_duplicated_elements"
    bl_label = "Remove Duplicated Elements"
    bl_options = {"UNDO"}
    bl_description = "Empty"

    def execute(self, context):
        source = get_active_source(context)
        element_list = get_element_list_from_active_source(source)
        i: int = len(element_list)-1
        while i > 0:
            checkee = element_list[i]
            j: int = i - 1
            while j > -1:
                if element_list[j].name == checkee.name:
                    element_list.remove(j)
                j = j - 1
            i = i - 1

        return {"FINISHED"}

_classes = [
    CT_OT_apply,
    CT_OT_capture,
    CT_OT_capture_group_add,
    CT_OT_capture_source_add,
    CT_OT_capture_element_add,
    CT_OT_capture_group_remove,
    CT_OT_capture_source_remove,
    CT_OT_capture_element_remove,
    CT_OT_capture_group_lock,
    CT_OT_capture_source_lock,
    CT_OT_capture_element_lock,
    CT_OT_remove_duplicated_elements
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()