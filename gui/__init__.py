from . import gui_panel, gui_list

def register():
    gui_panel.register()
    gui_list.register()

def unregister():
    gui_list.unregister()
    gui_panel.unregister()