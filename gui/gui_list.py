import bpy

class ST_UL_snap_elements(bpy.types.UIList):
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        layout.prop(data=item, property="name", icon="BONE_DATA", text="", emboss=False)

class ST_UL_snap_sources(bpy.types.UIList):
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        row_item = layout.row()

        if getattr(active_data, active_property)==index:
            row_item.prop(data=item, property="name", icon="RADIOBUT_ON", text="", emboss=False)
        else:
            row_item.prop(data=item, property="name", icon="RADIOBUT_OFF", text="", emboss=False)
        row_item.prop(data=item, property="type", text="", emboss=False)

class ST_UL_snap_presets(bpy.types.UIList):
    layout_type="DEFAULT"
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        row_item = layout.row()
        if getattr(active_data, active_property)==index:
            row_item.prop(data=item, property="name", icon="RADIOBUT_ON", text="", emboss=False)
        else:
            row_item.prop(data=item, property="name", icon="RADIOBUT_OFF", text="", emboss=False)

_classes = [
    ST_UL_snap_elements,
    ST_UL_snap_sources,
    ST_UL_snap_presets
]

_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()

def unregister():
    _unregister()