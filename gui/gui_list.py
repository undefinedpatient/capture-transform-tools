import bpy
from ..utilities import *
class CT_UL_capture_elements(bpy.types.UIList):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        row_item = layout.row()
        parent_source = get_active_source(context)
        if not is_bone_element_valid(item, parent_source):
            row_item.alert = True
        element_name = "<empty>" if item.name == "" else item.name
        row_item.label(text=element_name,  icon="BONE_DATA")
        row_item.separator()

        # Is active bone under current source indicator.
        if context.active_pose_bone and context.active_pose_bone.name == item.name:
            row_item.label(icon="DOT")
        row_item.prop(data=item, property="locked", icon="LOCKED" if item.locked else "UNLOCKED", text='', emboss=False)

class CT_UL_capture_sources(bpy.types.UIList):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        row_item = layout.row()
        if not is_source_valid(item):
            row_item.alert = True
        source_name = "<empty>" if item.source_object == None else item.source_object.name
        if getattr(active_data, active_property)==index:
            row_item.label(text=source_name, icon="RADIOBUT_ON")
        else:
            row_item.label(text=source_name, icon="RADIOBUT_OFF")
        # Is active object under current source indicator.
        if context.active_object and item.source_object == context.active_object:
            row_item.label(icon="DOT")
        row_item.prop(data=item, property="locked", icon="LOCKED" if item.locked else "UNLOCKED", text='', emboss=False)

class CT_UL_capture_groups(bpy.types.UIList):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):

        row_item = layout.row()
        if getattr(active_data, active_property)==index:
            row_item.prop(data=item, property="name", icon="RADIOBUT_ON", text="", emboss=False)
        else:
            row_item.prop(data=item, property="name", icon="RADIOBUT_OFF", text="", emboss=False)

        # Is active object under current group indicator.
        if context.active_object and context.active_object in list(map(lambda s: s.source_object, item.sources)):
            row_item.label(icon="DOT")

        row_item.prop(data=item, property="locked", icon="LOCKED" if item.locked else "UNLOCKED", text='', emboss=False)
    

_classes = [
    CT_UL_capture_elements,
    CT_UL_capture_sources,
    CT_UL_capture_groups
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()