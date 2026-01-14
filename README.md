# Snap Tools (0.0.1)
This addon aims to extend beyond Blender `copy Global Transform` funtionality. Allowing user to store it in groups!

# Status
This addon is still under development, and will have lots of bugs.

# Installation
You can simply download this as zip file, and pull the zip file into your Blender application to install it.

# Guidance
### Group
- Consider it as "group of objects/sources", each group will have its own independent settings, which are shared among the sources.
### Source
- This is the basic member unit in a group, each of them points to a single `Object`.
- Currently support `Object` and `Armature` types.
### Element
- Only when the source type is `Armature`, should be showing a list of bones to be captured.
- Ignored if the source type is `Object`, since the object itself is the element to be captured.
