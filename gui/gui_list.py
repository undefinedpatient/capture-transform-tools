import bpy
from ..utilities import *
class CT_UL_snap_elements(bpy.types.UIList):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        layout.label(text=item.name,  icon="BONE_DATA")

class CT_UL_snap_sources(bpy.types.UIList):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        row_item = layout.row()
        if has_source_object(item) and not is_source_type_valid(item):
            row_item.alert = True
        if getattr(active_data, active_property)==index:
            row_item.prop(data=item, property="name", icon="RADIOBUT_ON", text="", emboss=False)
        else:
            row_item.prop(data=item, property="name", icon="RADIOBUT_OFF", text="", emboss=False)
        # row_item.prop(data=item, property="source_object")
        row_item.prop(data=item, property="type", text="", emboss=False, expand=False)

class CT_UL_snap_groups(bpy.types.UIList):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):

        row_item = layout.row()
        if getattr(active_data, active_property)==index:
            row_item.prop(data=item, property="name", icon="RADIOBUT_ON", text="", emboss=False)
        else:
            row_item.prop(data=item, property="name", icon="RADIOBUT_OFF", text="", emboss=False)
    

_classes = [
    CT_UL_snap_elements,
    CT_UL_snap_sources,
    CT_UL_snap_groups
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()