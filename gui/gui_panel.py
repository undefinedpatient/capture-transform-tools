import bpy
from ..utilities import *
class ST_PT_snap_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_label = "Snap Tools"
    bl_idname = "BS_PT_snap_tools"
    bl_category = "Snap Tools"
    bl_order = 1
    def draw_group_section(self, context):
        props = context.scene.snap_tools_settings

        group_section = self.layout
        group_section.label(icon="OUTLINER_COLLECTION", text="Group")
        row_groups = group_section.row()
        # Left Column contains the source list
        col_group_list = row_groups.column()
        col_group_list.template_list(
            listtype_name="ST_UL_snap_groups",
            list_id="group_list",
            dataptr=props,
            propname="groups",
            active_dataptr=props, 
            active_propname="active_group_index",
            rows=1
        )
        # Right Column contains the actions
        col_group_actions = row_groups.column()
        row_group_add = col_group_actions.row()
        row_group_remove = col_group_actions.row()
        op_group_add = row_group_add.operator(operator="snap_tools.snap_group_add", icon="ADD", text="")
        op_group_remove = row_group_remove.operator(operator="snap_tools.snap_group_remove", icon="REMOVE", text="")
        row_group_remove.enabled = has_active_group(context)

        group_section.separator(type="LINE")

    def draw_source_section(self, context):
        props = context.scene.snap_tools_settings
        if has_active_group(context):
            active_group = get_active_group(context)
            source_section = self.layout
            source_section.label(icon="OBJECT_DATA", text="Source")
            row_sources = source_section.row()

            # Left Column contains the source list
            col_source_list = row_sources.column()
            col_source_list.template_list(
                listtype_name="ST_UL_snap_sources",
                list_id="source_list",
                dataptr=active_group,
                propname="sources",
                active_dataptr=active_group,
                active_propname="active_source_index",
                rows=2
            )
            if has_active_source(context):
                active_source = get_active_source(context)
                match active_source.type:
                    case SourceType.ARMATURE.name:
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
            # The Panel only enabled when active object is the same as source object
            row_element.enabled = active_source.source_object == context.active_object

            if not has_source_object(active_source) or not is_source_type_valid(active_source):
                return
            match active_source.type:
                case SourceType.OBJECT.name:
                    pass
                case SourceType.ARMATURE.name:
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
                    col_add_active = row_add_ops.column()
                    col_add_selected = row_add_ops.column()
                    op_add_active = col_add_active.operator(operator="snap_tools.snap_element_add", text="Add Active")
                    op_add_active.only_active = True
                    op_add_active.is_blank = False 
                    op_add_selected = col_add_selected.operator(operator="snap_tools.snap_element_add", text="Add Selected")
                    op_add_selected.only_active = False
                    op_add_selected.is_blank = False 
                    # col_add_selected.enabled = active_source.source_object == context.active_object


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
        layout.label(icon="SETTINGS",text="Source Settings")
        if has_active_source(context):
            active_source = get_active_source(context)
            row_snap_type = layout.column_flow(columns=1)
            row_snap_type.props_enum(active_source, "snap_type")
            match active_source.snap_type:
                case SnapType.LOCATION.name:
                    layout.prop(active_source, "relative_location", text="")
                case SnapType.RELATIVE.name:
                    layout.prop(active_source, "relative_object", text="")
        else:
            layout.label(text="You need to pick a source")

    def draw(self, context):
        layout = self.layout
        self.draw_group_section(context)
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