# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Snap Tools",
    "author": "Patient",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

_needs_reload = "gui" in locals()

from  . import gui, operators, properties
if _needs_reload:
    import importlib
    importlib.reload(operators)
    importlib.reload(gui)
    importlib.reload(properties)

def register():
    operators.register()
    gui.register()
    properties.register()


def unregister():
    properties.unregister()
    gui.unregister()
    operators.unregister()
