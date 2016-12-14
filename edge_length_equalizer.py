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
 "name": "equally length Bisector",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "equally length",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 

import bpy
import bmesh
import mathutils
import math


def igualarlargos(vertice1, vertice2, length):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    v1 = vertice1
    v2 = vertice2
    largo = length
    #distancia entre los dos vertices   

    dv1v2 = math.sqrt(math.fabs((((((v2.co.x)-(v1.co.x))**2))+((((v2.co.y)-(v1.co.y))**2))+((((v2.co.z)-(v1.co.z))**2)))))

    print("distancia entre vertices  : " + str(dv1v2))

    # asigno la distancia del nuevo vertice colinear respecto al vertice 1
    dv1v3 = largo


    #formula para cordenadas del nuevo vertice
    u = (dv1v3/dv1v2)

    cox = (1-u)*(v1.co.x)+ (u* v2.co.x)

    coy = (1-u)*(v1.co.y)+ (u* v2.co.y)

    coz = (1-u)*(v1.co.z)+ (u* v2.co.z)
    
    
    #cambio la cordenada del vertice 2


    v2.co = (cox,coy,coz)


    
    

 ################################################################################       
 ##########  clase del perpendicular######  #####################################
 ################################################################################                
class Edge_Equalizer_LengthOperator(bpy.types.Operator):
    "crea lineas a 90 grados respecto el vertice"
    bl_idname = "mesh.edgeequalizer"
    bl_label = 'Edge Equalizer'
    bl_description  = "taker all edges and set his lenght iqual to active edge"
    bl_options = {'REGISTER', 'UNDO'}
    
    chboxVert0 = bpy.props.BoolProperty(
        name="Vert 1",
        default= False
    )
    chboxVert1 = bpy.props.BoolProperty(
        name="Vert 2",
        default= False
    )


    def main(self, context, chboxVert0, chboxVert1):
        
        
        
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
              
         
        edges= [e for e in bm.edges if (e.select==True and not e.hide)]
        
        if not len(edges) > 2:
            msg = "select MINIMUM 2 vertices"
            self.report({"WARNING"}, msg)
            return {'CANCELLED'}  
        
        else:
            
            aristas = [a for a in bm.edges if (a.select and not a.hide)]


            active_edge = filter(lambda elem: isinstance(elem, bmesh.types.BMEdge), 
                    reversed(bm.select_history)).__next__()

            largo = active_edge.calc_length()    
            print(active_edge.calc_length())

            active_edge.select = False
            
            if chboxVert0:
                for a in aristas:
                    v1 = a.verts[0]
                    v2 = a.verts[1]
                    
                    igualarlargos(v1,v2,largo)              
       
            if chboxVert1:
                
                for a in aristas:
                    v1 = a.verts[0]
                    v2 = a.verts[1]
                    
                    igualarlargos(v2,v1,largo)
                
        
        
            
        # actualizo malla
        active_edge.select = True
        bmesh.update_edit_mesh(me, True)  
        
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxVert0, self.chboxVert1)
        #bisectoroperator(self)
        return {'FINISHED'}
        
                 
    

class Edge_Equalizer_LengthOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Edge  Equalizer"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(Edge_Equalizer_LengthOperator.bl_idname) #line perpendicular from two vertices
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()