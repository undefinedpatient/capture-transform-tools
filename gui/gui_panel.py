import bpy
from . import gui_list
from ..properties import SourceType, SnapType
class ST_PT_snap_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_label = "Snap Tools"
    bl_idname = "BS_PT_snap_tools"
    bl_category = "Snap Tools"
    def draw(self, context):
        props = context.scene.snap_tools_settings
        # Keep the index in range
        active_preset = props.presets[props.active_preset_index] if props.active_preset_index > -1 else None
        active_source = active_preset.sources[active_preset.active_source_index] if active_preset and active_preset.active_source_index > -1 and len(active_preset.sources) > 0 else None
        
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
        if not active_preset:
            # Dummy List
            
            col_source_list.template_list(
                listtype_name="ST_UL_snap_sources",
                list_id="source_list",
                dataptr=props,
                propname="presets",
                active_dataptr=props,
                active_propname="active_preset_index",
                rows=2  
            )
        else:
            col_source_list.template_list(
                listtype_name="ST_UL_snap_sources",
                list_id="source_list",
                dataptr=active_preset,
                propname="sources",
                active_dataptr=active_preset,
                active_propname="active_source_index",
                rows=2
            )
        
        
        
        if active_source:
            element_section = col_source_list
            if active_source.source_object:
                match active_source.type:
                    case SourceType.OBJECT.name:
                        pass
                    case SourceType.POSE_BONE.name:
                        row_elements = element_section.row()
                        # List
                        col_element_list = row_elements.column()
                        col_element_list.template_list(
                            listtype_name="ST_UL_snap_elements",
                            list_id="element_list",
                            dataptr=active_preset,
                            propname="sources",
                            active_dataptr=active_preset,
                            active_propname="active_source_index",
                            rows=2
                        )
            col_source_list.prop(active_source, "source_object", text="")

        row_add_ops = col_source_list.row()
        op_add_active = row_add_ops.operator(operator="snap_tools.snap_source_add_objects", text="Add Active")
        op_add_active.only_active = True
        op_add_selected = row_add_ops.operator(operator="snap_tools.snap_source_add_objects", text="Add Selected")
        op_add_selected.only_active = False
        col_source_list.operator(operator="snap_tools.capture", text="Capture")
        col_source_list.operator(operator="snap_tools.apply_snap_to_source", text="Apply")

            # Column: List of actions
        col_sources_actions = row_sources.column()
        op_snap_source_add = col_sources_actions.operator(operator="snap_tools.snap_source_add", icon="ADD", text="")
        op_snap_source_remove = col_sources_actions.operator(operator="snap_tools.snap_source_remove", icon="REMOVE", text="")
        source_section.separator(type="LINE")



        #
        #   Edit Section
        #
        if active_source:   
            edit_section = layout
            edit_section.label(icon="PRESET",text="Settings")
            row_snap_type = edit_section.column_flow(columns=1)
            row_snap_type.props_enum(active_source, "snap_type")
            match active_source.snap_type:
                case SnapType.LOCATION.name:
                    edit_section.prop(props, "relative_location", text="")
                case SnapType.RELATIVE.name:
                    edit_section.prop(props, "relative_object", text="")
        else:
            layout.label(text="You need to pick a source")
_classes = [
    ST_PT_snap_tools
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()