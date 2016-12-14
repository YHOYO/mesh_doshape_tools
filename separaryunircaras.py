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
 "name": "separar / unir caras",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "separar y unir caras ",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 


import bpy
import bmesh
import mathutils
import math

def separarcaras():

    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

        ### separar caras###
    listabordes = []

    for borde in bm.edges:
        listabordes.append(borde)
        
    bmesh.ops.split_edges(bm, edges=listabordes)

    bpy.ops.mesh.select_all(action='SELECT')

    bmesh.update_edit_mesh(me, True)
  

    
class SeparaUneOperator(bpy.types.Operator):
    "separa o une las caras de la malla "
    bl_idname = 'mesh.separa_une_caras'
    bl_label = 'Separa o Une Caras'
    bl_description  = "Separa o une las caras de las mallas"
    bl_options = {'REGISTER', 'UNDO'}
    
    chboxsepara = bpy.props.BoolProperty(
        name="Separa",
        default= True
    )
    chboxune = bpy.props.BoolProperty(
        name="Une",
        default= False
    )

   
    
    def main(self, context, chboxsepara, chboxune):   
        
        
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        if chboxsepara:
            

                ### separar caras###
            listabordes = []

            for borde in bm.edges:
                listabordes.append(borde)
                
            bmesh.ops.split_edges(bm, edges=listabordes)

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')


        elif chboxune:
            
            bpy.ops.mesh.select_all(action='SELECT')
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.1)
            bpy.ops.mesh.select_all(action='SELECT')
        
        bmesh.update_edit_mesh(me, True)
        
        
    
     
        
        
        
        
                        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxsepara, self.chboxune)
        return {'FINISHED'}
    
    
class SeparauneOperatorPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Separa o Une las caras seleccionadas"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.operator(SeparaUneOperator.bl_idname) 



    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()