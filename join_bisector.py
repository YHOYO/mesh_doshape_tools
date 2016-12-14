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
 "name": "Join Bisector",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "Join two points and bisect all the mesh",  
 "warning": "",  
 "wiki_url": "http://wiki.blender.org/index.php/Extensions:ES/2.6/Py/Scripts/Modeling/Join_cut_extend",  
 "tracker_url": "",  
 "category": "Doshape"} 

import bpy
import bmesh
import mathutils
import math
from bpy_extras import view3d_utils
import time


 ################################################################################       
 ##########  clase del Join######  #####################################
 ################################################################################                
class JoinBisectorOperator(bpy.types.Operator):
    "une dos puntos y divide la malla"
    bl_idname = 'mesh.joinbisectorline'
    bl_label = 'Join Bisector line'
    bl_description  = "Join two points and bisect all the mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def main(self, context):
        oa = bpy.context.active_object
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        vert = [v for v in bm.verts if (v.select == True and v.hide == False)]
        
        contador = 0

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                #ubicar la camara en posicion
                bpy.ops.view3d.snap_cursor_to_selected()
                
                viewport = area.regions[4]
                
                for v in vert:
                     #coo in 3d space
                    co_3d = oa.matrix_world * v.co
                     #coo in the 3d view area (2d)
                    co_2d = view3d_utils.location_3d_to_region_2d(viewport, area.spaces[0].region_3d, co_3d)
                    
                     #coo in the blender window
                    co_2d_w = (co_2d[0]+viewport.x, co_2d[1]+viewport.y)
                     #coo in the system screen
                    co_2d_s = (co_2d_w[0]+bpy.context.window.x, co_2d_w[1]+bpy.context.window.y)
                              
                    if contador == 0:
                        x1 = co_2d[0]
                        y1 = co_2d[1]
                        contador +=1
                        
                    if contador == 1:
                        x2 = co_2d[0]
                        y2 = co_2d[1]
                        break
                        

                #mover cursor del sistema operativo a donde el v1
                
                #depth_location = vert[1].co + Vector((0.1,0.1,0.1))
                #v3 =  view3d_utils.region_2d_to_location_3d(viewport, area.spaces[0].region_3d, co_2d, depth_location)
                
                v3 =  view3d_utils.region_2d_to_vector_3d(viewport, area.spaces[0].region_3d, co_2d)
                
                v3 = v3+ vert[1].co
                
                normal =  mathutils.geometry.normal(vert[0].co,vert[1].co,v3)
                
                bpy.ops.mesh.select_all(action='SELECT')

                #bpy.ops.mesh.bisect(plane_co=vert[0].co, plane_no=normal)
                
                bpy.ops.mesh.bisect(
                    plane_co=vert[1].co,
                    plane_no=normal, 
                    use_fill=False, 
                    clear_inner=False, 
                    clear_outer=False, 
                    threshold=0.0001, 
                    xstart=x1, 
                    xend=x2,
                    ystart=y1, 
                    yend=y2, 
                    cursor=1002)
      

        bmesh.update_edit_mesh(me, True)
            
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}
        
                 
    

class JoinBisectorOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Join"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(JoinBisectorOperator.bl_idname) #line Join from two vertices
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()