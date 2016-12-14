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
 "name": "Mover vertices seleccionados",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "mover vertices",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 


import bpy
import bmesh
import mathutils
import math


class MoverVerticesOperator(bpy.types.Operator):
    "Mover vertices"

    bl_idname = 'mesh.moververtices'
    bl_label = 'Mover Vertices'
    bl_description  = "allow move selected vertices"
    bl_options = {'REGISTER', 'UNDO'}  
       
    
    chboxaxisx = bpy.props.BoolProperty(
        name="Axis X",
        default= False
    )
    chboxaxisy  = bpy.props.BoolProperty(
        name="Axis Y",
        default= False
    )
    
    chboxaxisz  = bpy.props.BoolProperty(
        name="Axis z",
        default= True
    )
    
    distance = bpy.props.FloatProperty(  
        name="Distance",  
        default=0.0005,  
        description="Distance to explote",
        min=-100.00,
        max = 100.00
    )

    def main(self, context, chboxaxisx, chboxaxisy,chboxaxisz, distance):
        
        distancia = distance
        
        
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        if chboxaxisx:
            x = distancia
        else:
            x = 0.0
        
        if chboxaxisy:
            y = distancia
        else:
            y = 0.0
            
        if chboxaxisz:
            z = distancia
        else:
            z = 0.0    
        
        vertices = [v for v in bm.verts if (v.select and not v.hide)]
        
        
        bmesh.ops.translate(
                            bm,
                            verts=vertices,
                            vec=(x, y, z))

            ### separar caras###
       

        bmesh.update_edit_mesh(me, True)
        
        #"Render"
        bpy.ops.render.render()  
        
                  
    
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxaxisx, self.chboxaxisy,self.chboxaxisz, self.distance)
        #bisectoroperator(self)
        return {'FINISHED'}
    
                 
    

class MoverVerticesOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Mueve vertices"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(MoverVerticesOperator.bl_idname) #line Triangle from two vertices
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
