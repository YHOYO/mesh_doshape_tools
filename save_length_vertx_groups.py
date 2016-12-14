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
 "name": "salvar largos de grupos de vertices",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > ToolShelf",  
 "description": "salva los largos de grupos de vertices",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} # "Mesh"


import bpy
import bmesh
import mathutils
import math

def draw1(self, context):
    self.layout.label("un momento... calculando y salvando")

        
class Save_Largos_Operator(bpy.types.Operator):
    "save lenghts of vertex groups"

    bl_idname = 'mesh.save_txt_lenghts'
    bl_label = 'save lenght vertex group'
    bl_description  = "allow save leght of vertex groups"
    bl_options = {'REGISTER', 'UNDO'}  
    
       

        
    def main(self, context):
        
        #abrir directorio donde se guarda
        archivo_full = bpy.data.filepath.split("\\")
        #print(archivo_full)
        #print(len(archivo_full))
        contador = 1 
        directorio = archivo_full[0]

        while contador != len(archivo_full)-1:
            directorio = str(directorio) + "\\" + str(archivo_full[contador])
            contador +=1

        #directorio actual
        print(directorio)

        #Nombre del archivo

        nombre = "length.txt"
              
        #se abre un directorio y se guarda la informacion
        file1 = open((directorio + '\\' + nombre), 'w', encoding = "utf-8")

        # se calculan los largos de cada uno de los grupos de vertices
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        obj.vertex_groups
        for ob in obj.vertex_groups:
            bpy.ops.object.vertex_group_set_active(group=str(ob.name))
            bpy.ops.object.vertex_group_select()

            edges= [e for e in bm.edges if (e.select==True and not e.hide)]

            total = 0
            for edge in edges:
                total = (total + edge.calc_length())

            print(ob.name, " ", total)
            dato = (str(ob.name)+" "+ str( total))
            #se escribe en el archivo
            file1.write(str(dato) + "\n")
            
            
            bpy.ops.object.vertex_group_deselect()

        #se cierra el archivo para escritura
        file1.close()    
        #se abre e imprime la información del archivo por consola    
        file1 = open((directorio + '\\' + nombre),  'r', encoding = "utf-8")
        print(file1.read())
        file1.close()

        bmesh.update_edit_mesh(me, True)  
       
       
        #abre el directorio donde se guardo
        bpy.ops.wm.path_open(filepath=directorio)

    
    @classmethod
    def poll(self, context):
        obj = context.active_object
            
        archivo_full = bpy.data.filepath.split(".")
            
        extension_file= archivo_full[len(archivo_full)-1]
        if extension_file == "blend" and len(bpy.context.object.vertex_groups)>0:
                return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])
        else:
                return None
        
    def execute(self, context):
        try:
            archivo_full = bpy.data.filepath.split(".")
            
            extension_file= archivo_full[len(archivo_full)-1]
            if extension_file == "blend":
                self.main(context)
                return {'FINISHED'}
            else:
                bpy.context.window_manager.popup_menu(draw2, title="PLEASE SAVE", icon='CANCEL')
                return {'CANCELLED'}
                
            
        except:
            nombre_imagenes = "CANCELADO"
            bpy.context.window_manager.popup_menu(draw2, title="PLEASE SAVE", icon='CANCEL')
            return {'CANCELLED'}
               
        
        
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Save Vertex Groups Lengths") 
        col.label(text="do you want to save this file?") 
        col.label(text="¿Desea guardar el archivo? ")             
    

class Save_Largos_OperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"


    #bl_context = "editmode"
    bl_label = " Save Vertex group lenght"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(Save_Largos_Operator.bl_idname) 
        
        
    
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
