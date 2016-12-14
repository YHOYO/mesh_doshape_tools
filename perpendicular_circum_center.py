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
 "name": "Circumcenter bisector",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": " the circumcenter is the point where the perpendicular bisectors of a triangle intersect. ",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 
 
import bpy
import bmesh
import mathutils
import math

################################################################################ 
########  funcion para el corte del Circumcentro ##########
################################################################################ 

def corte(bm, v1, v2, v3):
	mid_vec = v1.lerp(v2, 0.5)
	plane_no = v1 - mid_vec
	plane_co = mid_vec
	dist = 0.0001

	# hidden geometry will not be affected.
	visible_geom = [g for g in bm.faces[:]
	+ bm.verts[:] + bm.edges[:] if not g.hide]

	try:
		bmesh.ops.bisect_plane(
	bm,
	geom=visible_geom,
	dist=dist,
	plane_co=plane_co, plane_no=plane_no,
	use_snap_center=False,
	clear_outer=False,
	clear_inner=False)

		bmesh.update_edit_mesh(me, True)
		
	except:  
		print("salto excepcion") 

            
################################################################################ 
##########  clase del Circumcentro ##########################################      
################################################################################ 
class PerpendicularCircumOperator(bpy.types.Operator):
    "divide a 90 grados"
    bl_idname = 'mesh.perpbisectorcircumcenter'
    bl_label = 'Perpendicular Bisector circumcenter  (medium point)'
    bl_description  = " the circumcenter is the point where the perpendicular bisectors of a triangle intersect. ."
    bl_options = {'REGISTER', 'UNDO'}
    
    def main(self, context):
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
                
        edges = [e for e in bm.edges if (e.select and not e.hide)]         
        vertices = [v for v in bm.verts if (v.select and not v.hide)]

        listavertices=[]
        if len(edges) !=0:
            
            print("bordes seleccionados: " +  str(len(edges)))
            for edge in edges:
                listavertices.append(edge.verts[0])
                listavertices.append(edge.verts[1])
                edge.select=False
                print(listavertices)
            
            contador =  len(listavertices)
            print(contador)
            while contador != 1:
                v1 =  listavertices[contador-1].co
                v2 =  listavertices[contador-2].co
                v3 = (0,0,0)
                print(v1,v2)
                corte(bm, v1, v2, v3) 
                contador = contador - 1

        elif len(edges) ==0 and len(vertices) == 2:
            v1,v2 =[v.co for v in bm.verts if (v.select and not v.hide)]
            v3 = (0,0,0)
            
            print("seleccionados 2 vertices")
            corte(bm, v1, v2, v3)   
        else:
            print("seleccione minimo 1 borde o 2 vertices")
            

            
        bmesh.update_edit_mesh(me, True) 
    
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        #bisectoroperator(self)
        return {'FINISHED'}
                 
    

class PerpendicularCircumOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Circum Perpendicular"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(PerpendicularCircumOperator.bl_idname) # lines as Circumcenter in triangle
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()