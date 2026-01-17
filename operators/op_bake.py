import bpy
from ..utilities import *

class CT_OT_bake(bpy.types.Operator):
    bl_idname = "capture_transform_tools.bake"
    bl_label = "Capture Group Bake"
    bl_options = {"UNDO"}
    bl_description = "Empty"

    

    bake_scope: bpy.props.EnumProperty(
        name="Bake Scope",
        items=[
            (BakeScope.GROUP.name, "Preset", "Empty", "OUTLINER_COLLECTION", 0),
            (BakeScope.SOURCE.name, "Source", "Empty", "OBJECT_DATA", 1),
            (BakeScope.ELEMENT.name, "Element", "Empty", "STICKY_UVS_DISABLE", 2)
        ]
    )


    lock_location: bpy.props.BoolVectorProperty(
        name="Lock Location",
        default=(False, False, False),
        subtype="XYZ"
    )

    frame_start: bpy.props.IntProperty(
        name="Frame Start",
        default=0
    )
    frame_end: bpy.props.IntProperty(
        name="Frame End",
        default=42
    )
    must_include_last_frame: bpy.props.BoolProperty(
        name="Must Include Last Frame",
        default=False
    )
    step: bpy.props.IntProperty(
        name="Step",
        default=3
    )

    def execute(self, context):
        match self.bake_scope:
            case BakeScope.ELEMENT.name:
                if not has_active_element(context):
                    self.report(type={"WARNING"}, message="No Active Element!")
                element = get_active_element(context)
                source = get_active_source(context)
                source_object: bpy.types.Object = source.source_object
                group = get_active_group(context)
                pose_bone: bpy.types.PoseBone = source_object.pose.bones[element.name]
                for frame in range(self.frame_start, self.frame_end, self.step):
                    context.scene.frame_set(frame)
                    apply_element_bone(group, source, element)
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
                if self.must_include_last_frame:
                    context.scene.frame_set(self.frame_end)
                    apply_element_bone(group, source, element)
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
                    


        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "frame_start")
        layout.prop(self, "frame_end")
        layout.prop(self, "step")
        layout.prop(self, "must_include_last_frame")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self,
            title="Bake",
            width=200
            )

classes = [
    CT_OT_bake,
]

_register, _unregister = bpy.utils.register_classes_factory(classes)


def register():
    _register()

def unregister():
    _unregister()