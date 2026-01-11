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
    
_classes = [
    ST_OT_snap,
    ST_OT_capture
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()