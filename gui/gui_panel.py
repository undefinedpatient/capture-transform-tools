import bpy
from ..utilities import *
class ST_PT_snap_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_label = "Snap Tools"
    bl_idname = "BS_PT_snap_tools"
    bl_category = "Snap Tools"
    bl_order = 1
    def draw_preset_section(self, context):
        props = context.scene.snap_tools_settings

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
        col_preset_actions = row_presets.column()
        row_preset_add = col_preset_actions.row()
        row_preset_remove = col_preset_actions.row()
        op_preset_add = row_preset_add.operator(operator="snap_tools.snap_preset_add", icon="ADD", text="")
        op_preset_remove = row_preset_remove.operator(operator="snap_tools.snap_preset_remove", icon="REMOVE", text="")
        row_preset_remove.enabled = has_active_preset(context)

        preset_section.separator(type="LINE")

    def draw_source_section(self, context):
        props = context.scene.snap_tools_settings
        if has_active_preset(context):
            active_preset = get_active_preset(context)
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
            if has_active_source(context):
                active_source = get_active_source(context)
                row_source_object = col_source_list.row()
                if has_source_object(active_source) and not is_source_type_valid(active_source):
                    row_source_object.alert = True
                row_source_object.prop(active_source, "source_object", text="")
            row_add_ops = col_source_list.row()
            op_add_active = row_add_ops.operator(operator="snap_tools.snap_source_add", text="Add Active")
            op_add_active.is_blank = False
            op_add_active.only_active = True
            op_add_selected = row_add_ops.operator(operator="snap_tools.snap_source_add", text="Add Selected")
            op_add_selected.is_blank = False
            op_add_selected.only_active = False
            row_op_capture = col_source_list.row()
            row_op_apply = col_source_list.row()
            row_op_capture.operator(operator="snap_tools.capture", text="Capture")
            row_op_apply.operator(operator="snap_tools.apply_snap_to_source", text="Apply")
            row_op_capture.enabled = has_active_source(context) and has_source_object(active_source) and is_source_type_valid(active_source)
            row_op_apply.enabled = has_active_source(context) and has_source_object(active_source) and is_source_type_valid(active_source)

            # Right Column contains +/-
            col_source_actions = row_sources.column()
            row_source_add = col_source_actions.row()
            row_source_remove = col_source_actions.row()
            op_source_add = row_source_add.operator(operator="snap_tools.snap_source_add", icon="ADD", text="")
            op_source_add.is_blank = True
            op_snap_source_remove = row_source_remove.operator(operator="snap_tools.snap_source_remove", icon="REMOVE", text="")
            row_source_remove.enabled = has_active_source(context)
            source_section.separator()
        else:
            return

    def draw_element_section(self, context):
        props = context.scene.snap_tools_settings
        if has_active_source(context):
            active_source = get_active_source(context)
            layout = self.layout
            row_element = layout.row()
            if not has_source_object(active_source) or not is_source_type_valid(active_source):
                return
            match active_source.type:
                case SourceType.OBJECT.name:
                    pass
                case SourceType.POSE_BONE.name:
                    layout.label(icon="ARMATURE_DATA", text="Elements")
                    row_element = layout.row()
                    # Left Column contains the element list
                    col_element_list = row_element.column()
                    col_element_list.template_list(
                        listtype_name="ST_UL_snap_elements",
                        list_id="element_list",
                        dataptr=active_source,
                        propname="element_bones",
                        active_dataptr=active_source,
                        active_propname="active_element_index",
                        rows=3
                    )
                    if has_active_element(context):
                        element = get_active_element(context)
                        col_element_list.prop_search(
                            data=element,
                            property="name",
                            search_data=active_source.source_object.data,
                            search_property="bones",
                            text="Bone"
                        )
                    row_add_ops = col_element_list.row()
                    op_add_active = row_add_ops.operator(operator="snap_tools.snap_element_add", text="Add Active")
                    op_add_active.only_active = True
                    op_add_active.is_blank = False 
                    op_add_selected = row_add_ops.operator(operator="snap_tools.snap_element_add", text="Add Selected")
                    op_add_selected.only_active = False
                    op_add_selected.is_blank = False 

                    # Right Column contains +/-
                    col_element_actions = row_element.column()
                    row_element_add = col_element_actions.row()
                    row_element_remove = col_element_actions.row()
                    op_snap_element_add = row_element_add.operator(operator="snap_tools.snap_element_add", icon="ADD", text="")
                    op_snap_element_add.is_blank = True
                    op_snap_element_remove = row_element_remove.operator(operator="snap_tools.snap_element_remove", icon="REMOVE", text="")
                    row_element_remove.enabled = has_active_element(context)

    def draw_settings(self, context):
        props = context.scene.snap_tools_settings
        layout = self.layout
        layout.separator(type="LINE")
        layout.label(icon="PRESET",text="Source Settings")
        if has_active_source(context):
            active_preset = get_active_preset(context)
            active_source = get_active_source(context)
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