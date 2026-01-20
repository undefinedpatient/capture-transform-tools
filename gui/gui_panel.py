import bpy
from ..utilities import *


class CT_MT_group_manage(bpy.types.Menu):
    bl_idname = "CT_MT_group_manage"
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.enabled = has_active_group(context)
        op_delete_unlocked = layout.operator("capture_transform_tools.capture_group_remove", icon="NONE", text="Delete All Unlocked Groups")
        op_delete_unlocked.remove_all = True

        op_group_lock = layout.operator("capture_transform_tools.capture_group_lock", icon="LOCKED", text="Lock All")
        op_group_lock.actions = LockAction.LOCK.name

        op_group_unlock = layout.operator("capture_transform_tools.capture_group_lock", icon="UNLOCKED", text="Unlock All")
        op_group_unlock.actions = LockAction.UNLOCK.name

        op_group_lock_invert = layout.operator("capture_transform_tools.capture_group_lock", icon="NONE", text="Lock Invert All")
        op_group_lock_invert.actions = LockAction.INVERT.name

class CT_MT_source_manage(bpy.types.Menu):
    bl_idname = "CT_MT_source_manage"
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.enabled =\
            has_active_source(context) and not get_active_group(context).locked
        op_delete_unlocked = layout.operator("capture_transform_tools.capture_source_remove", icon="NONE", text="Delete All Unlocked sources")
        op_delete_unlocked.remove_all = True

        op_source_lock = layout.operator("capture_transform_tools.capture_source_lock", icon="LOCKED", text="Lock All")
        op_source_lock.actions = LockAction.LOCK.name

        op_source_unlock = layout.operator("capture_transform_tools.capture_source_lock", icon="UNLOCKED", text="Unlock All")
        op_source_unlock.actions = LockAction.UNLOCK.name

        op_source_lock_invert = layout.operator("capture_transform_tools.capture_source_lock", icon="NONE", text="Lock Invert All")
        op_source_lock_invert.actions = LockAction.INVERT.name

class CT_MT_element_manage(bpy.types.Menu):
    bl_idname = "CT_MT_element_manage"
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.enabled = has_active_element(context) and not get_active_source(context).locked and not get_active_group(context).locked
        op_remove_duplicated = layout.operator("capture_transform_tools.remove_duplicated_elements")
        layout.separator(type="LINE")
        op_delete_unlocked = layout.operator("capture_transform_tools.capture_element_remove", icon="NONE", text="Delete All Unlocked elements")
        op_delete_unlocked.remove_all = True

        op_element_lock = layout.operator("capture_transform_tools.capture_element_lock", icon="LOCKED", text="Lock All")
        op_element_lock.actions = LockAction.LOCK.name

        op_element_unlock = layout.operator("capture_transform_tools.capture_element_lock", icon="UNLOCKED", text="Unlock All")
        op_element_unlock.actions = LockAction.UNLOCK.name

        op_element_lock_invert = layout.operator("capture_transform_tools.capture_element_lock", icon="NONE", text="Lock Invert All")
        op_element_lock_invert.actions = LockAction.INVERT.name


class CT_PT_capture_transform_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_label = "Capture Transform"
    bl_idname = "CT_PT_transform_capture_tools"
    bl_category = "Capture Transform"
    bl_order = 1
    def draw_group_section(self, context):
        props = context.scene.capture_transform_tools_settings

        group_section = self.layout
        group_section.label(icon="OUTLINER_COLLECTION", text="Group")
        row_groups = group_section.row()
        # Left Column contains the source list
        col_group_list = row_groups.column()
        col_group_list.template_list(
            listtype_name="CT_UL_capture_groups",
            list_id="group_list",
            dataptr=props,
            propname="groups",
            active_dataptr=props, 
            active_propname="active_group_index",
            rows=1
        )
        row_op_capture = col_group_list.row()
        row_op_apply_bake = col_group_list.row()
        op_capture = row_op_capture.operator(operator="capture_transform_tools.capture", icon="COPYDOWN", text="Capture")
        op_capture.capture_scope = CaptureScope.GROUP.name
        row_op_capture.enabled = has_active_group(context) and not get_active_group(context).locked
        row_op_apply_bake.enabled = has_active_group(context) 
        op_apply = row_op_apply_bake.operator(operator="capture_transform_tools.apply", icon="PASTEDOWN", text="Apply")
        op_apply.apply_scope = ApplyScope.GROUP.name
        op_apply.should_insert_keyframe = False
        op_bake = row_op_apply_bake.operator(operator="capture_transform_tools.bake", icon="CON_ACTION", text="Bake")
        op_bake.bake_scope = BakeScope.GROUP.name
        # Right Column contains the actions
        col_group_actions = row_groups.column()
        row_group_add = col_group_actions.row()
        row_group_remove = col_group_actions.row()
        op_group_add = row_group_add.operator(operator="capture_transform_tools.capture_group_add", icon="ADD", text="")

        op_group_remove = row_group_remove.operator(operator="capture_transform_tools.capture_group_remove", icon="REMOVE", text="")
        op_group_remove.remove_all = False
        row_group_remove.enabled = has_active_group(context) and not get_active_group(context).locked

        col_group_actions.menu("CT_MT_group_manage", icon="DOWNARROW_HLT", text="")

        group_section.separator(type="LINE")

    def draw_source_section(self, context):
        props = context.scene.capture_transform_tools_settings
        if has_active_group(context):
            active_group = get_active_group(context)
            source_section = self.layout
            source_section.label(icon="OBJECT_DATA", text="Source")
            row_sources = source_section.row()

            # Left Column contains the source list
            col_source_list = row_sources.column()
            col_source_list.template_list(
                listtype_name="CT_UL_capture_sources",
                list_id="source_list",
                dataptr=active_group,
                propname="sources",
                active_dataptr=active_group,
                active_propname="active_source_index",
                rows=2
            )
            if has_active_source(context):
                active_source = get_active_source(context)
                # Enum: Source Type OBJECT|ARMATURE
                row_source_type = col_source_list.row()
                row_source_type.prop(active_source, "type", expand=True)
                
                #
                row_source_object = col_source_list.row()
                if not is_source_valid(active_source):
                    row_source_object.alert = True
                row_source_object.prop_search(
                    data=active_source, 
                    property="source_object", 
                    search_data=context.scene,
                    search_property="objects",
                    text=""
                )
                row_source_type.enabled = not active_source.locked and not get_active_group(context).locked
                row_source_object.enabled = not active_source.locked and not get_active_group(context).locked
            row_add_ops = col_source_list.row()
            op_add_active = row_add_ops.operator(operator="capture_transform_tools.capture_source_add", text="Add Active")
            op_add_active.is_blank = False
            op_add_active.only_active = True
            op_add_selected = row_add_ops.operator(operator="capture_transform_tools.capture_source_add", text="Add Selected")
            op_add_selected.is_blank = False
            op_add_selected.only_active = False

            #
            # Enable
            row_add_ops.enabled = not get_active_group(context).locked
            #
            #


            row_op_capture = col_source_list.row()
            row_op_apply_bake = col_source_list.row()
            op_capture = row_op_capture.operator(operator="capture_transform_tools.capture", icon="COPYDOWN", text="Capture")
            op_capture.capture_scope = CaptureScope.SOURCE.name
            op_apply = row_op_apply_bake.operator(operator="capture_transform_tools.apply", icon="PASTEDOWN", text="Apply")
            op_apply.apply_scope = ApplyScope.SOURCE.name
            op_apply.should_insert_keyframe = False
            op_bake = row_op_apply_bake.operator(operator="capture_transform_tools.bake", icon="CON_ACTION", text="Bake")
            op_bake.bake_scope = BakeScope.SOURCE.name
            row_op_capture.enabled =\
                has_active_source(context) and not get_active_source(context).locked and\
                not get_active_group(context).locked
            row_op_apply_bake.enabled = has_active_source(context)


            # Right Column contains +/-
            col_source_actions = row_sources.column()
            row_source_add = col_source_actions.row()
            row_source_remove = col_source_actions.row()
            op_source_add = row_source_add.operator(operator="capture_transform_tools.capture_source_add", icon="ADD", text="")
            op_source_add.is_blank = True
            op_capture_source_remove = row_source_remove.operator(operator="capture_transform_tools.capture_source_remove", icon="REMOVE", text="")
            row_source_remove.enabled = has_active_source(context) and not get_active_source(context).locked

            col_source_actions.menu("CT_MT_source_manage", icon="DOWNARROW_HLT", text="") 

            col_source_actions.enabled = not get_active_group(context).locked

            source_section.separator()
        else:
            return

    def draw_element_section(self, context):
        props = context.scene.capture_transform_tools_settings
        if has_active_source(context):
            active_source = get_active_source(context)
            layout = self.layout
            row_element = layout.row()
            # The Panel only enabled when active object is the same as source object
            row_element.enabled = active_source.source_object == context.active_object
            if not is_source_valid(active_source):
                return
            match active_source.type:
                case SourceType.OBJECT.name:
                    pass
                case SourceType.ARMATURE.name:
                    layout.label(icon="GROUP_BONE", text="Elements")
                    row_element = layout.row()
                    # Left Column contains the element list
                    col_element_list = row_element.column()
                    col_element_list.template_list(
                        listtype_name="CT_UL_capture_elements",
                        list_id="element_list",
                        dataptr=active_source,
                        propname="element_bones",
                        active_dataptr=active_source,
                        active_propname="active_element_index",
                        rows=3
                    )
                    if has_active_element(context):
                        element = get_active_element(context)
                        row_element_target = col_element_list.row()
                        row_element_target.prop_search(
                            data=element,
                            property="name",
                            search_data=active_source.source_object.data,
                            search_property="bones",
                            text=""
                        )
                        row_element_target.enabled = not get_active_element(context).locked and not get_active_source(context).locked and not get_active_group(context).locked
                    row_add_ops = col_element_list.row()
                    col_add_active = row_add_ops.column()
                    col_add_selected = row_add_ops.column()
                    op_add_active = col_add_active.operator(operator="capture_transform_tools.capture_element_add", text="Add Active")
                    op_add_active.only_active = True
                    op_add_active.is_blank = False 
                    op_add_selected = col_add_selected.operator(operator="capture_transform_tools.capture_element_add", text="Add Selected")
                    op_add_selected.only_active = False
                    op_add_selected.is_blank = False

                    #
                    # Enable
                    row_add_ops.enabled = not get_active_group(context).locked and not get_active_source(context).locked
                    #
                    #

                    row_op_capture = col_element_list.row()
                    row_op_apply_bake = col_element_list.row()
                    op_capture = row_op_capture.operator(operator="capture_transform_tools.capture", icon="COPYDOWN", text="Capture")
                    op_capture.capture_scope = CaptureScope.ELEMENT.name
                    op_apply = row_op_apply_bake.operator(operator="capture_transform_tools.apply", icon="PASTEDOWN", text="Apply")
                    op_apply.apply_scope = ApplyScope.ELEMENT.name
                    op_apply.should_insert_keyframe = False
                    op_bake = row_op_apply_bake.operator(operator="capture_transform_tools.bake", icon="CON_ACTION", text="Bake")
                    op_bake.bake_scope = BakeScope.ELEMENT.name
                    row_op_capture.enabled =\
                        has_active_element(context) and not get_active_element(context).locked and\
                        not get_active_source(context).locked and not get_active_group(context).locked

                    # Right Column contains +/-
                    col_element_actions = row_element.column()
                    row_element_add = col_element_actions.row()
                    row_element_remove = col_element_actions.row()
                    op_capture_element_add = row_element_add.operator(operator="capture_transform_tools.capture_element_add", icon="ADD", text="")
                    op_capture_element_add.is_blank = True
                    op_capture_element_remove = row_element_remove.operator(operator="capture_transform_tools.capture_element_remove", icon="REMOVE", text="")

                    col_element_actions.menu("CT_MT_element_manage", icon="DOWNARROW_HLT", text="")

                    col_element_actions.enabled = not get_active_source(context).locked and not get_active_group(context).locked
                    row_element_remove.enabled = has_active_element(context) and not get_active_element(context).locked

    def draw_settings(self, context):
        props = context.scene.capture_transform_tools_settings
        layout = self.layout
        group_settings = layout.column()
        group_settings.separator(type="LINE")
        group_settings.label(icon="SETTINGS",text="Group Settings")
        if has_active_group(context):
            group_settings.enabled = not get_active_group(context).locked
            active_group = get_active_group(context)
            row_capture_type = group_settings.column_flow(columns=1)
            row_capture_type.props_enum(active_group, "capture_type")
            match active_group.capture_type:
                case CaptureType.LOCATION.name:
                    group_settings.prop(active_group, "relative_location", text="")
                case CaptureType.RELATIVE_OBJECT.name:
                    group_settings.prop(active_group, "relative_object", text="")
                case CaptureType.RELATIVE_BONE.name:
                    group_settings.prop(active_group, "relative_object", text="")
                    if active_group.relative_object:
                        if active_group.relative_object.type != "ARMATURE":
                            group_settings.label(text="Object Type Mismatch")
                        else:
                            group_settings.prop_search(
                                data=active_group, 
                                property="relative_bone", 
                                search_data=active_group.relative_object.data,
                                search_property="bones",
                                text=""
                            )
        else:
            group_settings.label(text="Create a group first.")

    def draw(self, context):
        layout = self.layout
        self.draw_group_section(context)
        self.draw_source_section(context)
        self.draw_element_section(context)
        self.draw_settings(context)
        layout.enabled = context.mode == "POSE" or context.mode=="OBJECT"



_classes = [
    CT_MT_group_manage,
    CT_MT_source_manage,
    CT_MT_element_manage,
    CT_PT_capture_transform_tools
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()