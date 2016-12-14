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
 "name": "Modificadores y Emptys",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "Modificadores y emptys ",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 


import bpy

    
class EliminarModificadoresyEmptysOperator(bpy.types.Operator):
    "Eliminar todos los modificadores del objeto"
    bl_idname = 'ops.eliminarmodificadoresyemptys'
    bl_label = 'Eliminar Modificadores y Emptys'
    bl_description  = "eliminar todos los modificadores  y Emptys del objeto"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def main(self, context):  
        ## creamos variables, listas y diccionarios globales
        self.objeto_activo =  bpy.context.active_object

               
        for m in self.objeto_activo.modifiers: 
            bpy.ops.object.modifier_remove(modifier=m.name)
       
        
        for objeto in bpy.context.selectable_objects:
            if objeto.type =="EMPTY":
                    objeto.select = True
            else:
                    objeto.select=False
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False) 
        bpy.ops.object.delete(use_global=False)

                        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}
    
class AplicaryEliminarModificadoresyEmptysOperator(bpy.types.Operator):
    "Aplica y Eliminar todos los modificadores del objeto"
    bl_idname = 'ops.aplicaryeliminarmodificadoresyemptys'
    bl_label = 'Aplicar Modificadores y Emptys'
    bl_description  = "Aplica y elimina todos los modificadores  y Emptys del objeto"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def main(self, context):  
        ## creamos variables, listas y diccionarios globales
        self.objeto_activo =  bpy.context.active_object

               
        for m in self.objeto_activo.modifiers: 
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=m.name)

       
        
        for objeto in bpy.context.selectable_objects:
            if objeto.type =="EMPTY":
                    objeto.select = True
            else:
                    objeto.select=False
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False) 
        bpy.ops.object.delete(use_global=False)

                        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}
        
class EliminarModificadoresyEmptysOperatorPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Eliminar Modificadores yEmptys"
    
    @classmethod
    def poll(cls, context):
        return (context.mode)
    
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.operator(EliminarModificadoresyEmptysOperator.bl_idname) 
        row = layout.row(align=True)
        row.operator(AplicaryEliminarModificadoresyEmptysOperator.bl_idname) 



    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()