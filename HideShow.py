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
 "name": "hide - unhide inverse",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "hide unhide inverse ",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 

import bpy
import bmesh
import mathutils
import math
import sys

  

    
class HideShowOperator(bpy.types.Operator):
    "crea las marcas de origami"
    bl_idname = 'mesh.hideshow'
    bl_label = 'Mostrar u Ocultar inversos'
    bl_description  = "Muestra o oculta los inversos seleccionados"
    bl_options = {'REGISTER', 'UNDO'}
    
    chboxhide = bpy.props.BoolProperty(
        name="Hide",
        default= True
    )
    chboxshow = bpy.props.BoolProperty(
        name="Show",
        default= False
    )

   
    
    def main(self, context, chboxhide, chboxshow):   
        
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        try:
            v1 = [v for v in bm.verts if (v.select == True and v.hide == False)]
            
            e1 = [e for e in bm.edges if (e.select == True and e.hide == False)]
            
            f1 = [f for f in bm.faces if (f.select == True and f.hide == False)]
        
        
            if len(v1)>0 or len(e1) >0 or f1>0:
                if chboxhide:
                    bpy.ops.mesh.select_all(action='INVERT')
                    bpy.ops.mesh.hide(unselected=False)
                    bpy.ops.mesh.select_all(action='SELECT')
                    
                elif chboxshow:                         
                    bpy.ops.mesh.reveal()
        except:
            
            if chboxshow:                         
                bpy.ops.mesh.reveal()

                
              
                
            
            
        
        bmesh.update_edit_mesh(me, True)
    
     
        
        
        
        
                        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxhide, self.chboxshow)
        return {'FINISHED'}
    
    
class HideShowOperatorPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "muestra u oculta lo inversamente seleccionado"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.operator(HideShowOperator.bl_idname) 



    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()