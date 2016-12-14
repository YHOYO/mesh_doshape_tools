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
 "name": "uv 3d proyection",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "convierte el 3D a las cordenadas UV ",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 


import bpy
import bmesh
import mathutils
import math

    
class Uv_3d_proyection_Operator(bpy.types.Operator):
    "separa o une las caras de la malla "
    bl_idname = 'mesh.uv_3d_proyection'
    bl_label = 'proyecta el UV en 3D'
    bl_description  = "proyecta el UV en 3D"
    bl_options = {'REGISTER', 'UNDO'}
    
    chboxall = bpy.props.BoolProperty(
        name="All",
        default= True
    )


   
    
    def main(self, context, chboxall):   
        
        ob = bpy.context.active_object
        bpy.ops.object.mode_set(mode='OBJECT')
        list = []
        for area in bpy.context.screen.areas:
            
            if area.type == 'IMAGE_EDITOR':   #find the UVeditor
                cursor = area.spaces.active.cursor_location   # get cursor location
                if  area.spaces.active.image :     
                    #print("el area: ", area.spaces.active.image.name )   
                    x = area.spaces.active.image.size[0]
                    y = area.spaces.active.image.size[1]
                else:
                    x = y = 256
                
                try:
                    
                    if area.spaces.active.image.name!= "Render Result" and area.spaces.active.image.name!= "Viewer Node":
                        
                        for v in ob.data.vertices : 
                            for p in ob.data.loops :
                                if chboxall:
                                    if v.index == p.vertex_index:
                                        #v.select = True
                                        x = ob.data.uv_layers.active.data[p.index].uv[0]
                                        y = ob.data.uv_layers.active.data[p.index].uv[1]
                                        
                                        print(v.index, " 3d co: ", v.co, " UV co: ", x,",",y)
                                        v.co = (x,y,0)
                                        print("vertice selected: ", v.index, " cor: ",x, y)
                                        list.append((x,y,0))
                                    
                                else:
                                    if v.index == p.vertex_index  and v.select:
                                        #v.select = True
                                        x = ob.data.uv_layers.active.data[p.index].uv[0]
                                        y = ob.data.uv_layers.active.data[p.index].uv[1]
                                        
                                        print(v.index, " 3d co: ", v.co, " UV co: ", x,",",y)
                                        v.co = (x,y,0)
                                        print("vertice selected: ", v.index, " cor: ",x, y)
                                        list.append((x,y,0))
       
                except:
                    return {'CANCELED'}
                           
              
        bpy.ops.object.mode_set(mode='EDIT')          
       
        
        
        
                        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxall)
        return {'FINISHED'}
    
    
class Uv_3d_proyection_OperatorPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Separa o Une las caras seleccionadas"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.operator(Uv_3d_proyection_Operator.bl_idname) 



    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()