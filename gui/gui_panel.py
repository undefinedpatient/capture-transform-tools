import bpy
from . import gui_list
from ..properties import SourceType, SnapType
class ST_PT_snap_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_label = "Snap Tools"
    bl_idname = "BS_PT_snap_tools"
    bl_category = "Snap Tools"
    bl_order = 1
    def draw_preset_section(self, context):
        props = context.scene.snap_tools_settings
        presets = props.presets
        active_index = props.active_preset_index
        active_preset = None if active_index == -1 else presets[active_index]

        preset_section = self.layout
        preset_section.label(icon="BOOKMARKS", text="Presets")
        row_presets = preset_section.row()
        # Left Column contains the source list
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
        # Right Column contains the actions
        col_presets_actions = row_presets.column()
        op_snap_preset_add = col_presets_actions.operator(operator="snap_tools.snap_preset_add", icon="ADD", text="")
        op_snap_preset_remove = col_presets_actions.operator(operator="snap_tools.snap_preset_remove", icon="REMOVE", text="")
        preset_section.separator(type="LINE")

    def draw_source_section(self, context):
        props = context.scene.snap_tools_settings
        presets = props.presets
        active_index = props.active_preset_index
        active_preset = None if active_index == -1 else presets[active_index]
        if active_preset:
            active_source_index = active_preset.active_source_index
            active_source = None if active_source_index == -1 else active_preset.sources[active_source_index]


            source_section = self.layout
            source_section.label(icon="OBJECT_DATA", text="Sources")
            row_sources = source_section.row()

            # Left Column contains the source list
            col_source_list = row_sources.column()
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
                col_source_list.prop(active_source, "source_object", text="")
            row_add_ops = col_source_list.row()
            op_add_active = row_add_ops.operator(operator="snap_tools.snap_source_add", text="Add Active")
            op_add_active.is_blank = False
            op_add_active.only_active = True
            op_add_selected = row_add_ops.operator(operator="snap_tools.snap_source_add", text="Add Selected")
            op_add_selected.is_blank = False
            op_add_selected.only_active = False
            col_source_list.operator(operator="snap_tools.capture", text="Capture")
            col_source_list.operator(operator="snap_tools.apply_snap_to_source", text="Apply")

            # Right Column contains +/-
            col_sources_actions = row_sources.column()
            op_snap_source_add = col_sources_actions.operator(operator="snap_tools.snap_source_add", icon="ADD", text="")
            op_snap_source_add.is_blank = True
            op_snap_source_remove = col_sources_actions.operator(operator="snap_tools.snap_source_remove", icon="REMOVE", text="")
            source_section.separator()
        else:
            return

    def draw_element_section(self, context):
        props = context.scene.snap_tools_settings
        presets = props.presets
        active_index = props.active_preset_index
        active_preset = None if active_index == -1 else presets[active_index]
        if active_preset:
            active_source_index = active_preset.active_source_index
            active_source = None if active_source_index == -1 else active_preset.sources[active_source_index]
            if active_source:
                layout = self.layout
                match active_source.type:
                    case SourceType.OBJECT.name:
                        pass
                    case SourceType.POSE_BONE.name:
                        layout.label(icon="ARMATURE_DATA", text="Elements")
                        row_elements = layout.row()
                        # Left Column contains the element list
                        col_element_list = row_elements.column()
                        col_element_list.template_list(
                            listtype_name="ST_UL_snap_sources",
                            list_id="element_list",
                            dataptr=active_source,
                            propname="element_bones",
                            active_dataptr=active_source,
                            active_propname="active_element_index",
                            rows=3
                        )
                        row_add_ops = col_element_list.row()
                        op_add_active = row_add_ops.operator(operator="snap_tools.snap_element_add", text="Add Active")
                        op_add_active.only_active = True
                        op_add_active.is_blank = False 
                        op_add_selected = row_add_ops.operator(operator="snap_tools.snap_element_add", text="Add Selected")
                        op_add_selected.only_active = False
                        op_add_selected.is_blank = False 
                        # Right
    
    def draw_settings(self, context):
        props = context.scene.snap_tools_settings
        presets = props.presets
        active_index = props.active_preset_index
        active_preset = None if active_index == -1 else presets[active_index]
        if active_preset:
            active_source_index = active_preset.active_source_index
            active_source = None if active_source_index == -1 else active_preset.sources[active_source_index]
            layout = self.layout
            if active_source:   
                layout.label(icon="PRESET",text="Settings")
                row_snap_type = layout.column_flow(columns=1)
                row_snap_type.props_enum(active_source, "snap_type")
                match active_source.snap_type:
                    case SnapType.LOCATION.name:
                        layout.prop(props, "relative_location", text="")
                    case SnapType.RELATIVE.name:
                        layout.prop(props, "relative_object", text="")
            else:
                layout.label(text="You need to pick a source")

    def draw(self, context):
        layout = self.layout
        self.draw_preset_section(context)
        self.draw_source_section(context)
        self.draw_element_section(context)
        self.draw_settings(context)



_classes = [
    ST_PT_snap_tools
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()