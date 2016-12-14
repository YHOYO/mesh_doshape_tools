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
 "name": "origami lines",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "origami lines",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 

import bpy
import bmesh
import mathutils
import math
import sys
           
class MontanaOperator(bpy.types.Operator):
    "crea las marcas de origami"
    bl_idname = 'mesh.mountainfreestyle'
    bl_label = 'Montaña'
    bl_description  = "Crea las lineas  Montaña de origami."
    bl_options = {'REGISTER', 'UNDO'}
    
 
    
    def main(self, context):

        ######################
        objetoactivo =  bpy.context.active_object

        bpy.ops.object.mode_set(mode = 'EDIT')

        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        lista_edges=[]
        edges = [e for e in bm.edges if (e.select==True and not e.hide)]
        for edge in edges:
            lista_edges.append(edge)
		
        for edge in lista_edges:
            edge.select = True
            bpy.ops.mesh.mark_freestyle_edge(clear=False)
            
	    
        bpy.ops.mesh.select_all(action='SELECT')
        
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        
        bpy.ops.mesh.separate(type='SELECTED')
        bmesh.update_edit_mesh(me, True)

        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        objetoactivo.select = False

        objetos_seleccionados = bpy.context.selected_objects


        for objeto in objetos_seleccionados:
            if objeto != objetoactivo:
                bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
                objeto.select = False
            

        objetos_seleccionados[0].select=False
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False 
        bpy.context.scene.layers[2] = False 

        objetoactivo.select=True

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        bpy.ops.object.mode_set(mode = 'EDIT')

        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bpy.ops.mesh.select_all(action='SELECT')
        for edge in bm.edges:
            edge.select = True
            bpy.ops.mesh.mark_freestyle_edge(clear=True)
            
        bmesh.update_edit_mesh(me, True)
    
        
        
        bpy.context.scene.layers[1] = True  
        bpy.context.scene.layers[2] = True   
        
        #"Render"
        bpy.ops.render.render()    

     
                
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}

 ################################################################################                
class delMontanaOperator(bpy.types.Operator):
    "borralas marcas de origami"
    bl_idname = 'mesh.delmountainfreestyle'
    bl_label = 'D_Montaña'
    bl_description  = "borralas lineas  Montaña de origami."
    bl_options = {'REGISTER', 'UNDO'}
    
    def main(self, context):

        activeobject =  bpy.context.active_object
        #all layers active
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = True
        # change to object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
        # deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # layer 0 and 2 inactive and layer 1 active
        bpy.context.scene.layers[0] = False
        bpy.context.scene.layers[2] = False
        #bpy.context.scene.layers[1] = True

        # select all in active layer and delete all
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        #change to layer active 0
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = True
		
		#"Render"
        bpy.ops.render.render()
        
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}


 ################################################################################                
            
class delCreaseOperator(bpy.types.Operator):
    "borra las marcas de origami"
    bl_idname = 'mesh.delcreasefreestyle'
    bl_label = 'D_Crease'
    bl_description  = "borra las lineas  crease de origami."
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def main(self, context):

        activeobject =  bpy.context.active_object
        #all layers active
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = True
        # change to object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
        # deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # layer 0 and 2 inactive and layer 1 active
        bpy.context.scene.layers[0] = False
        bpy.context.scene.layers[1] = False
        #bpy.context.scene.layers[2] = True

        # select all in active layer and delete all
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        #change to layer active 0
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[0] = True
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = True
		
		#"Render"
        bpy.ops.render.render()
        
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}
    
            
class CreaseOperator(bpy.types.Operator):
    "crea las marcas de origami"
    bl_idname = 'mesh.creasefreestyle'
    bl_label = 'Crease'
    bl_description  = "Crea las lineas  crease de origami."
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def main(self, context):

        ######################
        objetoactivo =  bpy.context.active_object

        bpy.ops.object.mode_set(mode = 'EDIT')

        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        lista_edges=[]
        edges = [e for e in bm.edges if (e.select==True and not e.hide)]
        for edge in edges:
            lista_edges.append(edge)
		
        for edge in lista_edges:
            edge.select = True
            bpy.ops.mesh.mark_freestyle_edge(clear=False)
            
	    
        bpy.ops.mesh.select_all(action='SELECT')
        
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        
        bpy.ops.mesh.separate(type='SELECTED')
        bmesh.update_edit_mesh(me, True)

        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        objetoactivo.select = False

        objetos_seleccionados = bpy.context.selected_objects


        for objeto in objetos_seleccionados:
            if objeto != objetoactivo:
                bpy.ops.object.move_to_layer(layers=(False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
                objeto.select = False
            

        objetos_seleccionados[0].select=False
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False 
        bpy.context.scene.layers[2] = False 

        objetoactivo.select=True

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        bpy.ops.object.mode_set(mode = 'EDIT')

        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        bpy.ops.mesh.select_all(action='SELECT')
        for edge in bm.edges:
            edge.select = True
            bpy.ops.mesh.mark_freestyle_edge(clear=True)
            
        bmesh.update_edit_mesh(me, True)
    
        
        
        bpy.context.scene.layers[1] = True  
        bpy.context.scene.layers[2] = True   
        
        #"Render"
        bpy.ops.render.render()   
        
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}
    

class LineasOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = "Origami Lines"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.label(text="Asignar")
        props = row.operator("mesh.mark_freestyle_edge", text = "Valle") 
        props.clear= False    
        row.operator(MontanaOperator.bl_idname) 
        row.operator(CreaseOperator.bl_idname)  
        
        layout = self.layout 
        row = layout.row(align=True)
        row.label(text="Borrar")
        props = row.operator("mesh.mark_freestyle_edge", text = "D_Valle") 
        props.clear= True   
        row.operator(delMontanaOperator.bl_idname) 
        row.operator(delCreaseOperator.bl_idname)  

    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()