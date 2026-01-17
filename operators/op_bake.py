import bpy


class CT_OT_capture_group_bake(bpy.types.Operator):
    bl_idname = "capture_transform_tools.capture_group_bake"
    bl_label = "Capture Group Bake"
    bl_options = {"UNDO"}
    bl_description = "Empty"
    def execute(self, context):
        return {"FINISHED"}

classes = [
    CT_OT_capture_group_bake
]

_register, _unregister = bpy.utils.register_classes_factory(classes)


def register():
    _register()

def unregister():
    _unregister()