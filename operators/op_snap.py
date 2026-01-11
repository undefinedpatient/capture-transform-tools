import bpy

class ST_OT_snap(bpy.types.Operator):
    bl_idname = "snap_tool.snap"
    bl_label = "Snap"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

class ST_OT_capture(bpy.types.Operator):
    bl_idname = "snap_tool.capture"
    bl_label = "Capture"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

class ST_OT_snap_group_add(bpy.types.Operator):
    bl_idname = "snap_tool.snap_group_add"
    bl_label = "Snap Group Add"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.snap_tools_settings
        new_preset = props.presets.add()
        return {"FINISHED"}
class ST_OT_snap_group_remove(bpy.types.Operator):
    bl_idname = "snap_tool.snap_group_remove"
    bl_label = "Snap Group Remove"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        props = context.scene.snap_tools_settings
        active_preset_index = props.active_preset_index
        props.presets.remove(active_preset_index)
        return {"FINISHED"}

_classes = [
    ST_OT_snap,
    ST_OT_capture,
    ST_OT_snap_group_add,
    ST_OT_snap_group_remove
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()