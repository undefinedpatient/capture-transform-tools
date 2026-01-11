import bpy
from . import gui_list
class ST_PT_snap_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_label = "Snap Tools"
    bl_idname = "BS_PT_snap_tools"
    bl_category = "Snap Tools"
    def draw(self, context):
        props = context.scene.snap_tools_settings

        layout = self.layout
    
        #
        #   Presets Section
        #
        preset_section = layout
        preset_section.label(icon="BOOKMARKS", text="Presets")

        row_presets = preset_section.row()
        row_presets.template_list(listtype_name="ST_UL_snap_presets", list_id="present_list", dataptr=props, propname="presets", active_dataptr=props, active_propname="active_preset_index")
        # Column: List of actions
        col_presets_actions = row_presets.column()
        op_snap_group_add = col_presets_actions.operator(operator="snap_tool.snap_group_add", icon="ADD", text="")
        op_snap_group_remove = col_presets_actions.operator(operator="snap_tool.snap_group_remove", icon="REMOVE", text="")
        preset_section.separator(type="LINE")
        #
        #   Sources Section
        #
        source_section = preset_section
        source_section.label(icon="OBJECT_DATA", text="Sources")
        source_section.separator(type="LINE")
        #
        #   Edit Section
        #
        edit_section = layout
        edit_section.label(icon="PRESET",text="Settings")


        edit_section.prop(props, "relative_object", text="")

_classes = [
    ST_PT_snap_tools
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()