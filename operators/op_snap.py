import bpy

class ST_OT_snap(bpy.types.Operator):
    bl_idname = "snap_tools.snap"
    bl_label = "Snap"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

class ST_OT_capture(bpy.types.Operator):
    bl_idname = "snap_tools.capture"
    bl_label = "Capture"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

class ST_OT_snap_preset_add(bpy.types.Operator):
    bl_idname = "snap_tools.snap_preset_add"
    bl_label = "Snap Preset Add"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.snap_tools_settings
        new_preset = props.presets.add()
        # If it is a newly added preset, set the active preset index to 0
        if len(props.presets) == 1:
            props.active_preset_index = 0
        return {"FINISHED"}

class ST_OT_snap_preset_remove(bpy.types.Operator):
    bl_idname = "snap_tools.snap_preset_remove"
    bl_label = "Snap Preset Remove"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.snap_tools_settings
        if len(props.presets) == 0:
            return {"FINISHED"}
        active_preset_index = props.active_preset_index
        if active_preset_index>=len(props.presets)-1:
            props.active_preset_index -= 1
        props.presets.remove(active_preset_index)
        return {"FINISHED"}

class ST_OT_snap_source_add_objects(bpy.types.Operator):
    bl_idname = "snap_tools.snap_source_add_objects"
    bl_label = "Snap Source Add Objects"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"

    only_active: bpy.props.BoolProperty(
        name="Only Active",
        default=False
    )

    def execute(self, context):
        props = context.scene.snap_tools_settings

        if len(props.presets) == 0:
            self.report(type={"INFO"}, message="No preset exist, created one.")
            bpy.ops.snap_tools.snap_preset_add()
        active_preset_index = props.active_preset_index
        if self.only_active:
            source = props.presets[active_preset_index].sources.add()
            source.name = context.active_object.name
            source.source_object = context.active_object

        else:
            for o in context.selected_objects:
                source = props.presets[active_preset_index].sources.add()
                source.name = o.name
                source.source_object = o

        return {"FINISHED"}

class ST_OT_snap_source_add(bpy.types.Operator):
    bl_idname = "snap_tools.snap_source_add"
    bl_label = "Snap Source Add"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.snap_tools_settings

        if len(props.presets) == 0:
            self.report(type={"INFO"}, message="No preset exist, created one.")
            bpy.ops.snap_tools.snap_preset_add()

        active_preset_index = props.active_preset_index
        props.presets[active_preset_index].sources.add()
        return {"FINISHED"}

class ST_OT_snap_source_remove(bpy.types.Operator):
    bl_idname = "snap_tools.snap_source_remove"
    bl_label = "Snap Source Remove"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.snap_tools_settings
        if len(props.presets) == 0 or len(props.presets[props.active_preset_index].sources) == 0:
            return {"FINISHED"}
        active_preset = props.presets[props.active_preset_index]
        active_source_index = active_preset.active_source_index

        if active_source_index>=len(active_preset.sources)-1:
            props.presets[props.active_preset_index].active_source_index -= 1

        active_preset.sources.remove(active_source_index)

        return {"FINISHED"}

class ST_OT_apply_snap_to_source(bpy.types.Operator):
    bl_idname = "snap_tools.apply_snap_to_source"
    bl_label = "Apply Snap to Source"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

class ST_OT_apply_snap_to_element(bpy.types.Operator):
    bl_idname = "snap_tools.apply_snap_to_element"
    bl_label = "Apply Snap to Element"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

_classes = [
    ST_OT_snap,
    ST_OT_capture,
    ST_OT_snap_preset_add,
    ST_OT_snap_preset_remove,
    ST_OT_snap_source_add,
    ST_OT_snap_source_add_objects,
    ST_OT_snap_source_remove,
    ST_OT_apply_snap_to_source,
    ST_OT_apply_snap_to_element,
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()