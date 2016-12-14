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
 "name": "join_explote",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "join or explote faces",  
 "warning": "",  
 "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/triangle_bisector",  
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



class JoinExploteOperator(bpy.types.Operator):
    "triangle bisector"
    bl_idname = 'mesh.joinexplote'
    bl_label = 'Join / Explote'
    bl_description  = "allow join or explote faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    chboxexplote = bpy.props.BoolProperty(
        name="Explote",
        default= True
    )
    chboxjoin = bpy.props.BoolProperty(
        name="Join",
        default= False
    )
    
    
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
        default=0.05,  
        description="Distance to explote",
        min=-100.00,
        max = 100.00
    )

    def main(self, context, chboxexplote, chboxjoin, chboxaxisx, chboxaxisy,chboxaxisz, distance):
        
                   
        
        if chboxexplote:
            
            distancia = distance/10
                        
             #almacena caras
            obj = bpy.context.object
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            
            obj = bpy.context.object
            
            cara_activa = bm.faces.active
            
            
            listacaras = [v for v in bm.faces if (v.select and not v.hide)]
            
            listacarasdes = [v for v in bm.faces if (v.select == False and not v.hide)]
            
            contador = len(listacaras)
            #print(len(listacaras))
            
            if distancia != 0: 
                separarcaras()
                
            while contador != 0:
                contador -=1
                cara = listacaras[contador]
                posicion = contador * distancia
                if cara == cara_activa:
                    print("cara eje")
                
                for vertice in cara.verts:
                        if chboxaxisx:
                            vertice.co.x =  vertice.co.x + posicion
                        if chboxaxisy:
                            vertice.co.y =  vertice.co.y + posicion
                        if chboxaxisz:
                            vertice.co.z =  vertice.co.z + posicion         
                    
            for cara in listacaras:
                cara.select = False
             
            if len(listacaras) != (len(bm.faces)):
                bpy.ops.mesh.select_all(action='INVERT')
            else:
                bpy.ops.mesh.select_all(action='SELECT')
                
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
            cara_activa.select=True
            bmesh.update_edit_mesh(me, True)   

        ######### unir caras
        
        elif chboxjoin:                  
        
            
                        #almacena caras
            obj = bpy.context.object
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            listacaras = []

            if len(bm.faces)>1:
                for face in bm.faces:
                    if face.select:
                        listacaras.append(face)
                #bmesh.update_edit_mesh(me, True)
            		


            distanciax= bm.faces.active.verts[0].co.x
            distanciay= bm.faces.active.verts[0].co.y
            distanciaz= bm.faces.active.verts[0].co.z
            contador = len(listacaras)
            #print(len(listacaras))

            listavertices = [bm.faces.active.verts[0]]

            for cara in listacaras:
                for vertice in cara.verts:
                    listavertices.append(vertice)
                    if chboxaxisx:
                        vertice.co.x = distanciax
                    if chboxaxisy:
                        vertice.co.y = distanciay
                    if chboxaxisz:
                        vertice.co.z = distanciaz



            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)


            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            for vertice in bm.verts:
                if vertice.co.x == distanciax:
                    vertice.select = True
                elif vertice.co.y == distanciay:
                    vertice.select = True
                elif vertice.co.z == distanciaz:
                    vertice.select = True


            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

                  
                    
            bmesh.update_edit_mesh(me, True)   
           
          
                  
    
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxexplote, self.chboxjoin, self.chboxaxisx, self.chboxaxisy,self.chboxaxisz, self.distance)
        #bisectoroperator(self)
        return {'FINISHED'}
    
                 
    

class JoinExploteOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Join or Explote Faces"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(JoinExploteOperator.bl_idname) #line Triangle from two vertices
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
