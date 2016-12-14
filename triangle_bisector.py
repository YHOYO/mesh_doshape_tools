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
 "name": "Triangle Bisector",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "split all  the triangular faces selected in their bisectors",  
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

####################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  
def calcularpuntobisectrices(cara,lado1,lado2,lado3,vertice1,vertice2,vertice3, arista1, arista2,arista3, vvertice1,vvertice2,vvertice3,chboxVert0, chboxVert1, chboxVert2):
    l1 = lado1
    l2 = lado2
    l3 = lado3
    v1 = vertice1
    v2 = vertice2
    v3 = vertice3
    a1 = arista1
    a2 = arista2
    a3 = arista3
    vv1 = vvertice1  #especifica el indice de los vertices
    vv2 = vvertice2
    vv3 = vvertice3
    face = cara
    seleccion1 = chboxVert0
    seleccion2 = chboxVert1
    seleccion3= chboxVert2
    
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    ###########################################################
    # punto BISECTRIZ 1
    
    #calcular razon de bisectriz
    razon_bisectriz1 = (l3/l1)
            
    print("razon 1: " + str(razon_bisectriz1))

    nuevovertice_x1 = (v3.x + ((razon_bisectriz1)*(v2.x)))/(1+razon_bisectriz1)
    nuevovertice_y1 = (v3.y + ((razon_bisectriz1)*(v2.y)))/(1+razon_bisectriz1)
    nuevovertice_z1 = (v3.z + ((razon_bisectriz1)*(v2.z)))/(1+razon_bisectriz1)
            
    #print("nuevo verticex" + str(nuevovertice_x1))
    #print("nuevo verticey" + str(nuevovertice_y1))
    #print("nuevo verticez" + str(nuevovertice_z1))

     
    coordenanuevaarista1 = mathutils.Vector((nuevovertice_x1,nuevovertice_y1,nuevovertice_z1))
    
    aristanueva1 = bmesh.utils.edge_split(a2, a2.verts[0], 0.5 ) 
    
    verticenuevo1 = [v for v in face.verts if (v.select==False and not v.hide)]
    for vertice1 in verticenuevo1:
        vv4 = vertice1
        vv4.co = coordenanuevaarista1
        vv4.select = True
      
   ##########################################################
    # punto BISECTRIZ 2
    
    #calcular razon de bisectriz
    razon_bisectriz2 = (l1/l2)
            
    print("razon 2: " + str(razon_bisectriz2))

    nuevovertice_x2 = (v1.x + ((razon_bisectriz2)*(v3.x)))/(1+razon_bisectriz2)
    nuevovertice_y2 = (v1.y + ((razon_bisectriz2)*(v3.y)))/(1+razon_bisectriz2)
    nuevovertice_z2 = (v1.z + ((razon_bisectriz2)*(v3.z)))/(1+razon_bisectriz2)

    coordenanuevaarista2 = mathutils.Vector((nuevovertice_x2,nuevovertice_y2,nuevovertice_z2))
    
    aristanueva2 = bmesh.utils.edge_split(a3, a3.verts[0], 0.5 ) 
    
    verticenuevo2 = [v for v in face.verts if (v.select==False and not v.hide)]
    for vertice2 in verticenuevo2:
        vv5 = vertice2
        vv5.co = coordenanuevaarista2
        vv5.select = True
    
    

    ###########################################################
    # punto BISECTRIZ 3
    
    #calcular razon de bisectriz
    razon_bisectriz3 = (l2/l3)
            
    print("razon 3: " + str(razon_bisectriz3))

    nuevovertice_x3 = (v2.x + ((razon_bisectriz3)*(v1.x)))/(1+razon_bisectriz3)
    nuevovertice_y3 = (v2.y + ((razon_bisectriz3)*(v1.y)))/(1+razon_bisectriz3)
    nuevovertice_z3 = (v2.z + ((razon_bisectriz3)*(v1.z)))/(1+razon_bisectriz3)

    coordenanuevaarista3 = mathutils.Vector((nuevovertice_x3,nuevovertice_y3,nuevovertice_z3))
    
    aristanueva3 = bmesh.utils.edge_split(a1, a1.verts[0], 0.5 ) 
    
    verticenuevo3 = [v for v in face.verts if (v.select==False and not v.hide)]
    for vertice3 in verticenuevo3:
        vv6 = vertice3
        vv6.co = coordenanuevaarista3
        vv6.select = True
    
    # all bisectriz
    if seleccion1 and  seleccion2 == False and seleccion3 ==False:
        
        bmesh.ops.connect_vert_pair(bm, verts=[vv1, vv4])
        bmesh.ops.connect_vert_pair(bm, verts=[vv2, vv5]) 
        bmesh.ops.connect_vert_pair(bm, verts=[vv3, vv6])
        
        verticenuevo4 = [v for v in face.verts if (v.select==False and not v.hide)]
        for vertice in verticenuevo4:
            incentro = vertice
            print("cordenadas incentro: " + str(incentro.co))
            #incentro.select = True   #se crea bucle infinito al dejarlo activo    
    
    #only bisect points        
    elif seleccion2 and  seleccion1 == False and seleccion3 == False:
         
        bmesh.ops.connect_vert_pair(bm, verts=[vv1, vv4])
        bmesh.ops.connect_vert_pair(bm, verts=[vv2, vv5]) 
        bmesh.ops.connect_vert_pair(bm, verts=[vv3, vv6])
        
        verticenuevo4 = [v for v in face.verts if (v.select==False and not v.hide)]
        for vertice in verticenuevo4:
            incentro = vertice
            print("cordenadas incentro: " + str(incentro.co))
            #incentro.select = True   #se crea bucle infinito al dejarlo activo    
            bmesh.utils.vert_dissolve(vertice)
    #        
    elif  seleccion3 and  seleccion2 == False and seleccion1 == False:
        
        bmesh.ops.connect_vert_pair(bm, verts=[vv1, vv4])
        bmesh.ops.connect_vert_pair(bm, verts=[vv2, vv5]) 
        bmesh.ops.connect_vert_pair(bm, verts=[vv3, vv6])
        
        verticenuevo4 = [v for v in face.verts if (v.select==False and not v.hide)]
        for vertice in verticenuevo4:
            incentro = vertice
            print("cordenadas incentro: " + str(incentro.co))
            #incentro.select = True   #se crea bucle infinito al dejarlo activo    
        
        bmesh.utils.vert_dissolve(vv4)
        bmesh.utils.vert_dissolve(vv5)
        bmesh.utils.vert_dissolve(vv6)
        
    else:
         msg = "select ONLY 1 option"
################################################################################
######  triangle bisector##########################################  
################################################################################ 

class TriangleBisectorOperator(bpy.types.Operator):
    "triangle bisector"
    bl_idname = 'mesh.trianglebisector'
    bl_label = 'Triangle Bisector'
    bl_description  = "allow create the triangle bisector points"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    
    
    chboxVert0 = bpy.props.BoolProperty(
        name="Full",
        default= True
    )
    chboxVert1 = bpy.props.BoolProperty(
        name="Only reference Verts",
        default= False
    )
    chboxVert2 = bpy.props.BoolProperty(
        name="Incenter",
        default= False
    )

    def main(self, context, chboxVert0, chboxVert1, chboxVert2):
        finalizar_uniendocaras = True
        
        #almacena caras
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        listacaras = []
        
        for face in bm.faces:
            if face.select and len(face.verts) ==3:
                listacaras.append(face)
        #bmesh.update_edit_mesh(me, True)        
		
        
        
        #################### separa caras
        separarcaras()
        ##########################   
        #obj = bpy.context.object
        #me = obj.data
        #bm = bmesh.from_edit_mesh(me)
        
        
        #vuelve a seleccionar caras
        for face in listacaras:
            face.select = True
        

        ##########################   
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)


        ### aplicar división 

        for face in listacaras:
            if face.select:
                print("cara seleccionada")
                centro_cara = mathutils.Vector(face.calc_center_median_weighted())
                
                if len(face.verts) == 3:
                    print("es un triangulo")
                    vertices = [v for v in face.verts ]
                    print(len(vertices))
                    vv1,vv2,vv3 = [v for v in vertices]
                    print(vv1,vv2,vv3)
                    v1,v2,v3 = [v.co for v in vertices]
                    print("cordenada vertice  " + str(v1))
                    print("cordenada vertice  " + str(v2))
                    print("cordenada vertice  " + str(v3))
                    
                    #agrupamos todas las aristas seleccionadas y no ocultas de la cara                             
                    aristas = [a for a in face.edges if (a.select and not a.hide)]
                    #las asignamos a variables independientes
                    a1,a2,a3 =[a for a in aristas]
                    #creamos los largos de cada una de las aristas
                    l1,l2,l3 =[a.calc_length() for a in aristas]
                    print(l1,'\n',l2,'\n',l3)
                    
                    #distancia entre vertices segun sus cordinadas           
                    c= ((((v1[0])-(v2[0])*(v1[0])-(v2[0]))),(((v1[1])-(v2[1])*(v1[1])-(v2[1]))),(((v1[2])-(v2[2])*(v1[2])-(v2[2]))))
                    print(c)

                    distancia1 = math.sqrt(math.fabs(c[0])) + math.sqrt(math.fabs(c[1])) +math.sqrt(math.fabs(c[2])) 
                    
                    print(distancia1)
                    
                   
                    #divide uno de los bordes.
                    #mid_vec1 = v3.lerp(v2, razon_bisectriz1)
                    #bmesh.utils.edge_split(a2, a2.verts[0], 0.5)

           #####################################   
                    #llamo a la funcion que calcula los angulos:
                    #calcularangulos(l1,l2,l3)  #funcionando
                    #calcularbisectrices(l1,l2,l3,v1,v2,v3) #falta por comprobar

                    if chboxVert0:
                        vertice1 = True
                        calcularpuntobisectrices(face,l2,l3,l1,v2,v3,v1,a2,a3,a1,vv2,vv3,vv1,chboxVert0, chboxVert1, chboxVert2)
                    if chboxVert1:
                        calcularpuntobisectrices(face,l1,l2,l3,v1,v2,v3,a1,a2,a3,vv1,vv2,vv3,chboxVert0, chboxVert1, chboxVert2)
                    if chboxVert2:
                        calcularpuntobisectrices(face,l3,l1,l2,v3,v1,v2,a3,a1,a2,vv3,vv1,vv2,chboxVert0, chboxVert1, chboxVert2)
                    



                                
                else:
                    print("DEBE SER UN TRIANGULO")
            else:
                print("cara no seleccionada")
                
                    


        ## actualizar toda la malla
            bmesh.update_edit_mesh(me, True)
            
        if finalizar_uniendocaras:
            bpy.ops.mesh.select_all(action='SELECT')    
            bpy.ops.mesh.remove_doubles()  
            bpy.ops.mesh.select_all(action='DESELECT')
            return {'FINISHED'}  
        
           
    
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context, self.chboxVert0, self.chboxVert1, self.chboxVert2)
        #bisectoroperator(self)
        return {'FINISHED'}
    
                 
    

class TriangleBisectorOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Triangle bisector"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(TriangleBisectorOperator.bl_idname) #line Triangle from two vertices
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
