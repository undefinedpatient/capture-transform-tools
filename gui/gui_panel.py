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
            # List
        col_preset_list = row_presets.column()
        col_preset_list.template_list(
            listtype_name="ST_UL_snap_presets",
            list_id="preset_list",
            dataptr=props,
            propname="presets",
            active_dataptr=props, 
            active_propname="active_preset_index",
            rows=1
        )
            # Column: List of actions
        col_presets_actions = row_presets.column()
        op_snap_preset_add = col_presets_actions.operator(operator="snap_tools.snap_preset_add", icon="ADD", text="")
        op_snap_preset_remove = col_presets_actions.operator(operator="snap_tools.snap_preset_remove", icon="REMOVE", text="")
        preset_section.separator(type="LINE")

        #
        #   Sources Section
        #
        source_section = preset_section
        source_section.label(icon="OBJECT_DATA", text="Sources")
        row_sources = source_section.row()
            # List
        col_source_list = row_sources.column()
            # In case the preset list is empty, simple return a empty dummy list.
        if len(props.presets) == 0:
            col_source_list.template_list(
                listtype_name="ST_UL_snap_sources",
                list_id="source_list",
                dataptr=props,
                propname="presets",
                active_dataptr=props,
                active_propname="active_preset_index",
                rows=3  
            )
        else:
            col_source_list.template_list(
                listtype_name="ST_UL_snap_sources",
                list_id="source_list",
                dataptr=props.presets[props.active_preset_index],
                propname="sources",
                active_dataptr=props.presets[props.active_preset_index],
                active_propname="active_source_index",
                rows=3  
            )
        col_source_list.operator(operator="snap_tools.apply_snap_to_source", text="Apply")
            # Column: List of actions
        col_sources_actions = row_sources.column()
        op_snap_source_add = col_sources_actions.operator(operator="snap_tools.snap_source_add", icon="ADD", text="")
        op_snap_source_remove = col_sources_actions.operator(operator="snap_tools.snap_source_remove", icon="REMOVE", text="")
        source_section.separator(type="LINE")
        #
        #   Edit Section
        #
        edit_section = layout
        edit_section.label(icon="PRESET",text="Settings")
        edit_section.label(text="Relative Location")
        edit_section.prop(props, "relative_location", text="")
        edit_section.label(text="Relative Object")
        edit_section.prop(props, "relative_object", text="")
        layout.operator(operator="snap_tools.snap")

_classes = [
    ST_PT_snap_tools
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()