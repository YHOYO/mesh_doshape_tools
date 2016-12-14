bl_info = {
    "name": "Set Pivot Point (View 3D) Menu",
    "author": "CoDEmanX",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Spacebar Menu (or bind it to a hotkey)",
    "description": "A menu to change the Pivot Point of the 3D View, bindable to a hotkey.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Doshape"}
	
	
import bpy

pivot_prop = bpy.types.SpaceView3D.bl_rna.properties['pivot_point']
pivot_items = [(item.identifier, item.name, item.description) for item in pivot_prop.enum_items]

class VIEW3D_OT_pivot_point_set(bpy.types.Operator):
    __doc__ = pivot_prop.description
    bl_idname = "view3d.pivot_point_set"
    bl_label = "Set Pivot Point (View 3D)"

    type = bpy.props.EnumProperty(items=pivot_items)

    @classmethod
    def poll(cls, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                return True
            
        return False

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].pivot_point = self.type
                break
        return {'FINISHED'}


class VIEW3D_MT_pivot_point_set(bpy.types.Menu):
    bl_label = pivot_prop.name
    bl_idname = "VIEW3D_MT_pivot_point_set"

    def draw(self, context):
        layout = self.layout
        enum = bpy.types.SpaceView3D.bl_rna.properties['pivot_point'].enum_items
        
        for item in reversed(enum):
            layout.operator("view3d.pivot_point_set", text=item.name, icon=item.icon).type = item.identifier

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=VIEW3D_MT_pivot_point_set.bl_idname)