from . import op_capture, op_bake

def register():
    op_capture.register()
    op_bake.register()

def unregister():
    op_bake.unregister()
    op_capture.unregister()

