import bpy, bmesh

'''
BEGIN GPL LICENSE BLOCK

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

END GPL LICENCE BLOCK
'''

bl_info = {  
 "name": "Selected Vertex By Plane Side",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > Select",  
 "description": "Selected Vertex By Plane Side",  
 "warning": "",  
 "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/selected_vertex_by_plane_side",  
 "tracker_url": "https://github.com/YHOYO/mesh_doshape_tools/blob/master/select%20vertex%20by%20plane%20side.py",
 "category": "Doshape"} 

import bpy
import bmesh
import mathutils
import math
from bpy_extras import view3d_utils


addon_keymaps = []
def shortcut(activar):   
    if activar:
         # handle the keymap
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new(SelectedVertexByPlaneSideOperator.bl_idname, 'Q', 'ANY', any=False, shift=False, ctrl=False, alt=True, oskey=False, key_modifier='NONE', head=False)
        
        addon_keymaps.append((km, kmi))
    else:
            # handle the keymap
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        
        addon_keymaps.clear()

        
class SelectedVertexByPlaneSideOperator(bpy.types.Operator):
    "Selected Vertex By Plane Side"
    bl_idname = 'mesh.selected_vertex_by_plane_side'
    bl_label = 'Select vertex by Plane side'
    bl_description  = "allow select vertex in any side of plane"
    bl_options = {'REGISTER', 'UNDO'}
    
    chboxiniciales = bpy.props.BoolProperty(
        name="Selected",
        default= True
    )
    chboxcoplanares = bpy.props.BoolProperty(
        name="Coplanar",
        default= True
    )
    chboxladoa= bpy.props.BoolProperty(
        name="Lado / Side A",
        default= False
    )
        
    chboxladob = bpy.props.BoolProperty(
        name="Lado / Side B",
        default= False
    )


    def main(self, context, chboxiniciales, chboxcoplanares, chboxladoa, chboxladob):
        
        #print("#"*50)
        #me cambio a modo vertices
        #modo_actual = tuple(bpy.context.scene.tool_settings.mesh_select_mode)   
        #bpy.context.scene.tool_settings.mesh_select_mode=(True,False,False)
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        oa = bpy.context.active_object
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        mat = obj.matrix_world
        
        vert_1 = [v for v in bm.verts if (v.select == True and v.hide == False)]            
        #vert_2 = [v for v in bm.verts if (v.select == False and v.hide == False)]
        if len(vert_1)<2:
                self.report({'ERROR'}, 'no plane detected')
        else:
            v1 = mat*vert_1[0].co
            v2 = mat*vert_1[1].co
            try:
                v3 = mat*vert_1[2].co
            except:
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        override = bpy.context.copy()
                        viewport = area.regions[4]
                
                        #coo in 3d space
                        co_3d = mat* v1
                        #coo in the 3d view area (2d)
                        co_2d = view3d_utils.location_3d_to_region_2d(viewport, area.spaces[0].region_3d, co_3d)      
                
                        v3 =  view3d_utils.region_2d_to_vector_3d(viewport, area.spaces[0].region_3d, co_2d)
                        v3 = v3+ v1

            plane_no = mathutils.geometry.normal([v1, v2, v3])

            self._coplanares = []
            
            for v in vert_1:
                v.select=False

            for v in bm.verts:
                pt = mat*v.co
                d = mathutils.geometry.distance_point_to_plane(pt, v1, plane_no)
                z= round(d, 4)
                
                
                if z ==0.0:
                    self._coplanares.append(v)
                elif z>0 and chboxladoa:
                    v.select=True
                elif z<0 and chboxladob:
                    v.select=True
                elif z==None:
                    print(v.index)

            
            for v in self._coplanares:
                if chboxcoplanares:
                    v.select=True    
                else:
                    v.select=False
            
            for v in vert_1:
                if chboxiniciales:
                    v.select=True
                else:
                    v.select=False    
        bmesh.update_edit_mesh(me, True) 

        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxiniciales, self.chboxcoplanares, self.chboxladoa, self.chboxladob)
        return {'FINISHED'}
    
    
def menu_draw(self, context):
        self.layout.operator(SelectedVertexByPlaneSideOperator.bl_idname)

        


                 
'''    
class SelectedVertexByPlaneSideOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Fold line"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(SelectedVertexByPlaneSideOperator.bl_idname) #line Triangle from two vertices
        
'''     
    

def register():
    bpy.utils.register_module(__name__)
    
    bpy.types.VIEW3D_MT_select_edit_mesh.prepend(menu_draw)
    shortcut(True)



    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_draw)
    shortcut(False)

if __name__ == "__main__":
    register()
