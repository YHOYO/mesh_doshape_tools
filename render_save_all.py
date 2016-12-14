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
 "name": "Renderizar y salvar todas las escenas",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > ToolShelf",  
 "description": "renderiza y salva todas las escenas",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} # "Mesh"


import bpy
def draw1(self, context):
    self.layout.label("un momento... renderizando")
def draw2(self, context):
    self.layout.label("PLEASE SAVE THE FILE FIRST")
            
        
class Render_Save_ScenesOperator(bpy.types.Operator):
    "Render_Save_Scenes"

    bl_idname = 'object.render_save_scenes'
    bl_label = 'Render and Save all steps'
    bl_description  = "allow render and save all scenes"
    bl_options = {'REGISTER', 'UNDO'}  
    
       

        
    def main(self, context):
        bpy.context.window_manager.popup_menu(draw1, title="PLEASE WAIT", icon='INFO')
        
        
              
        escenas = bpy.data.scenes
        print(len(escenas))
        
        try:
            archivo_full = bpy.data.filepath.split("\\")
            

            nombre_blend = archivo_full[len(archivo_full)-1]

            partir_nombre = nombre_blend.split(".")

            nombre_imagenes = partir_nombre[0]
        except:
            nombre_imagenes = "sin_nombre"
        
        for escena in escenas:                
            escenas[escena.name].render.filepath = str("//")+ str(nombre_imagenes) + "_"+  str(escena.name)
                                  
            bpy.ops.render.render(write_still=True, scene=escena.name)
        
        #abrir directorio donde se guarda
        archivo_full = bpy.data.filepath.split("\\")
        print(archivo_full)
        print(len(archivo_full))

        contador = 1 
        nombre = archivo_full[0]

        while contador != len(archivo_full)-1:
            nombre = str(nombre) + "\\" + str(archivo_full[contador])
            contador +=1

        print(nombre)
        bpy.ops.wm.path_open(filepath=nombre)

    
    @classmethod
    def poll(self, context):
        
        archivo_full = bpy.data.filepath.split(".")
            
        extension_file= archivo_full[len(archivo_full)-1]
        if extension_file == "blend":
                return all
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
        col.label(text="RENDER ALL?") 
        col.label(text="This could be take time") 
        col.label(text="Esto puede tomar tiempo")             
    

class Render_Save_ScenesOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    bl_label = "Renderizar y salvar escenas"
	
    @classmethod
    def poll(cls, context):
        return (context.mode)
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(Render_Save_ScenesOperator.bl_idname) #render and save all scenes
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
