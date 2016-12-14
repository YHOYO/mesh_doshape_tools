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
 "name": "equal angler Bisector",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "equally divided angle",  
 "warning": "",  
 "wiki_url": "http://wiki.blender.org/index.php/Extensions:ES/2.6/Py/Scripts/Modeling/Equal_Angles",  
 "tracker_url": "",  
 "category": "Doshape"} 
 
import bpy
import bmesh
import mathutils
import math
from bpy_extras import view3d_utils
import time
import sys


def anguloylargopuesto(vertice1,vertice2,vertice3):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    
    v1 = vertice1
    v2 = vertice2
    v3 = vertice3
    
    #distancia v1v2 
        
    l1 = math.sqrt(math.fabs((((((v2.co.x)-(v1.co.x))**2))+((((v2.co.y)-(v1.co.y))**2))+((((v2.co.z)-(v1.co.z))**2)))))
                
    print("distancia entre vertices v1_v2 : " + str(l1))
    
    #distancia v1v3 
        
    l2 = math.sqrt(math.fabs((((((v3.co.x)-(v1.co.x))**2))+((((v3.co.y)-(v1.co.y))**2))+((((v3.co.z)-(v1.co.z))**2)))))
                
    print("distancia entre vertices v1_v3 : " + str(l2))
    
    
    #distancia v2v3  # este es el lado opuesto
        
    l3 = math.sqrt(math.fabs((((((v3.co.x)-(v2.co.x))**2))+((((v3.co.y)-(v2.co.y))**2))+((((v3.co.z)-(v2.co.z))**2)))))
                
    print("distancia entre vertices v2_v3 : " + str(l3))
    
    
    #formula para calcular :     
    #angulo1 =  arccos((x2 + y2 - z2)/2xy)
    a1= (l1*l1)+(l2*l2)-(l3*l3)
    b1= (2*l1*l2)
    
    #print(a)
    #print(b)
    angulo1_radianes = math.acos(a1/b1)
    print("angulo1 en radianes: " + str(angulo1_radianes))
    pi = math.pi # constante de pi
    
    # convertimos los radianes a angulos
    angulo1_grados = (180 * angulo1_radianes) / pi
    print("angulo1 en grados: " + str(angulo1_grados))
    
    
    # actualizo malla
    
    bmesh.update_edit_mesh(me, True)

def colinear(vertice1,vertice2,vertice3):
        
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    #toma dos vertices
    v1,v2 = [v for v in bm.verts if (v.select==True and not v.hide)]

    #distancia entre los dos vertices   
        
    dv1v2 = math.sqrt(math.fabs((((((v2.co.x)-(v1.co.x))**2))+((((v2.co.y)-(v1.co.y))**2))+((((v2.co.z)-(v1.co.z))**2)))))
                
    print("distancia entre vertices  : " + str(dv1v2))

    # asigno la distancia del nuevo vertice colinear respecto al vertice 1
    dv1v3 = 8


    #formula para cordenadas del nuevo vertice
    u = (dv1v3/dv1v2)

    cox = (1-u)*(v1.co.x)+ (u* v2.co.x)

    coy = (1-u)*(v1.co.y)+ (u* v2.co.y)

    coz = (1-u)*(v1.co.z)+ (u* v2.co.z)

       
    #creacion nuevo vertice colinear    
    vnuevo = mathutils.Vector((tuple((cox,coy,coz))))
        
    v3 = bm.verts.new((cox,coy,coz))


    #creo un nuevo borde entre el vertice1 y el nuevo colinear

    borde = bm.edges.new((v1,v3))

    #selecciono todo

    bpy.ops.mesh.select_all(action='SELECT')

    #deseleccciono el vertice 2
    v2.select=False

    # actualizo malla

    bmesh.update_edit_mesh(me, True)
    

def razor2(vertice1,vertice2, vertice3,anglecorte, anglefijo):
    oa = bpy.context.active_object
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    pi = math.pi # constante de pi    
    v1 = vertice1
    v2 = vertice2
    v3 = vertice3
    
    angulocorte = anglecorte
    angulofijo = anglefijo
    angulocomplementario = pi -(angulocorte+angulofijo)
    print(angulocorte)
    print("angulo corte: " + str((180 * angulocorte) / pi))
    print("angulo fijo: " + str((180 * angulofijo) / pi))
    print("angulo complementario: " + str((180 * angulocomplementario) / pi))
    #distancia entre los dos vertices   
        
    dv2v3 = math.sqrt(math.fabs((((((v3.co.x)-(v2.co.x))**2))+((((v3.co.y)-(v2.co.y))**2))+((((v3.co.z)-(v2.co.z))**2)))))
                
    print("distancia entre vertices opuestos v2v3: " + str(dv2v3))
    dv1v3 = math.sqrt(math.fabs((((((v1.co.x)-(v3.co.x))**2))+((((v1.co.y)-(v3.co.y))**2))+((((v1.co.z)-(v3.co.z))**2)))))
    #dv1v3 = math.sqrt(math.fabs((((((v1.co.x)-(v2.co.x))**2))+((((v1.co.y)-(v2.co.y))**2))+((((v1.co.z)-(v2.co.z))**2)))))
    print("distancia entre vertices opuestos v1v3: " + str(dv1v3))
    #distancia nuevo vertice:
    # asigno la distancia del nuevo vertice colinear respecto al vertice 1
    
    dv1v2=  (dv1v3 * math.sin(angulocorte))/(math.sin(angulocomplementario))
    
    print("distancia entre vertices v1v2: " + str(dv1v2))


    #formula para cordenadas del nuevo vertice
    u = (dv1v2/dv2v3)

    cox = (1-u)*(v3.co.x)+ (u* v2.co.x)

    coy = (1-u)*(v3.co.y)+ (u* v2.co.y)

    coz = (1-u)*(v3.co.z)+ (u* v2.co.z)

       
    #creacion nuevo vertice colinear    
    vnuevo = mathutils.Vector((tuple((cox,coy,coz))))
        
    v3 = bm.verts.new((cox,coy,coz))
    
    
    veje = v1.co
    vdestino = v3.co
    
    listado = [v3]
    bmesh.ops.dissolve_verts(bm, verts = listado)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            viewport = area.regions[4]
    
            #coo in 3d space
            co_3d = oa.matrix_world * vdestino
            #coo in the 3d view area (2d)
            co_2d = view3d_utils.location_3d_to_region_2d(viewport, area.spaces[0].region_3d, co_3d)
                            
            v4 =  view3d_utils.region_2d_to_vector_3d(viewport, area.spaces[0].region_3d, co_2d)
                        
            v4 = v4+ vdestino
                        
            normal =  mathutils.geometry.normal(veje, vdestino,v4)
        
    #print("thenormal " + str(normal))


    plane_no = normal
    plane_co = veje
    #print('cordenadas plano:\n', plane_no, '\n', plane_co)
    dist = 0.0001

    # hidden geometry will not be affected.
    visible_geom = [g for g in bm.faces[:] + bm.verts[:] + bm.edges[:] if not g.hide]

    newdata = bmesh.ops.bisect_plane(
        bm,
        geom=visible_geom,
        dist=dist,
        plane_co=plane_co, 
        plane_no=plane_no,
        use_snap_center=False,
        clear_outer=False,
        clear_inner=False)

    #cortador(v2,v3)
    bmesh.update_edit_mesh(me, True) 

    
    
############    
def calcularangulos(vertice1, vertice2, vertice3,secciones,direccion):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    # calcula la direccion del corte
    direccion = direccion
    #aqui debemos duplicar los vertices 2 y 3 unicamente
    v1 = vertice1
    vv2 = vertice2
    vv3 = vertice3
    
    v2 = bm.verts.new((vv2.co))
    v3 = bm.verts.new((vv3.co))
    
    #luego los nuevos vertices los agregamos a la lista a eliminar luego
    listabasuravertices = [v2,v3]
    #deseleccinamos los vertices 2 y 3 originales y seleccionamos los nuevos
    vv2.select = False
    vv3.select = False
    v2.select =  True
    v3.select = True
        

    #se crean los nuevos bordes
    edge1 = bm.edges.new((v1,v2))
    edge2 = bm.edges.new((v1,v3))
    edge3 = bm.edges.new((v2,v3))
    #agregamos el edge3 a la lista a eliminar luego
    listabasuraedges = [edge3]
    
    # Se calculan los largos
    l1 = edge1.calc_length()
    l2 = edge2.calc_length()
    l3 = edge3.calc_length()
    
    print(l1,l2,l3)
    
    # borro el tercer borde creado (el apuesto al angulo)
    bmesh.ops.delete(bm, geom= listabasuraedges, context=2)
        

#formula para calcular :     
    #angulo1 =  arccos((x2 + y2 - z2)/2xy)
    a1= (l1*l1)+(l2*l2)-(l3*l3)
    b1= (2*l1*l2)
    
    #print(a)
    #print(b)
    angulo1_radianes = math.acos(a1/b1)
    print("angulo1 en radianes: " + str(angulo1_radianes))
    pi = math.pi # constante de pi
    
    # convertimos los radianes a angulos
    angulo1_grados = (180 * angulo1_radianes) / pi
    print("angulo1 en grados: " + str(angulo1_grados))
    
    ###########################################################
    #angulo2 =  arccos((y2 + z2 - x2)/2yz)
    a2= (l2*l2)+(l3*l3)-(l1*l1)
    b2= (2*l2*l3)
    
    #print(a)
    #print(b)
    angulo2_radianes = math.acos(a2/b2)
    print("angulo2 en radianes: " + str(angulo2_radianes))

        # convertimos los radianes a angulos
    angulo2_grados = (180 * angulo2_radianes) / pi
    print("angulo2 en grados: " + str(angulo2_grados))
    
            
    ###########################################################
    #angulo3 =  arccos((x2 + z2 - y2)/2xz)
    a3= (l1*l1)+(l3*l3)-(l2*l2)
    b3= (2*l1*l3)
    
    #print(a)
    #print(b)
    angulo3_radianes = math.acos(a3/b3)
    print("angulo3 en radianes: " + str(angulo3_radianes))

        # convertimos los radianes a angulos
    angulo3_grados = (180 * angulo3_radianes) / pi
    print("angulo3 en grados: " + str(angulo3_grados))
    
    ############envio angulo real para corte:
    
    anguloestatico = angulo2_radianes
    contador =  1
    anguloreal=(direccion*(angulo1_radianes/secciones))
    angulosausar = [anguloreal]
    while contador != secciones:       
        anguloreal1 = contador * angulosausar[0]
        angulosausar.append(anguloreal1)
        contador = contador+1
    
    del angulosausar[0]
    
    for anguloenvio in angulosausar:
        print("angulo real: " + str(angulo1_grados))
        print("angulos corte enviado: " + str((180 * anguloenvio) / pi))
        print("angulos estatico enviado000: " + str((180 * anguloestatico) / pi))
        print("vertices enviados: ",  v2.co, v1.co)   
        razor2(v1,v2,v3,anguloenvio, anguloestatico)
        #razor(v2,v1,anguloreal)
    
    # borro los vertices duplicados al inicio
    bmesh.ops.delete(bm, geom= listabasuravertices, context = 1)
    # selecciono los vertices 2 y 3 originales
    vv2.select = True
    vv3.select = True
    bmesh.update_edit_mesh(me, True)
####################### 
                    
class equalangleBisectorOperator(bpy.types.Operator):
    "divide en en angulo especificado"
    bl_idname = 'mesh.equalequalangleBisector'
    bl_label = 'Equal Angle Bisector'
    bl_description  = "allow  bisect in specific angle"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    
    chboxVert0 = bpy.props.BoolProperty(
        name="Vert A",
        default= True
    )
    chboxVert1 = bpy.props.BoolProperty(
        name="Vert B",
        default= False
    )
    chboxVert2 = bpy.props.BoolProperty(
        name="Vert C",
        default= False
    )

    cortes = bpy.props.IntProperty(  
        name="Segmentos",  
        default=2,  
        description="Number of segments (not dividing lines)",
        min=2
    )

    def main(self, context, chboxVert0, chboxVert1, chboxVert2, cortes):
        
        
        # variable angulo dependiendo los grados ingresados
        secciones = cortes
   
        direccion = 1
        
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
                
        vertices = [v for v in bm.verts if (v.select==True and not v.hide)]
                
        if len(vertices) != 3:
            print("seleccione solo 3 vertices")
            #return {'FINISHED'}
        else:
            vv1,vv2,vv3 = [v for v in bm.verts if (v.select==True and not v.hide)]
                       
            if chboxVert0:
                calcularangulos(vv1, vv2, vv3,secciones,direccion)
                

            if chboxVert1:
                calcularangulos(vv2, vv3, vv1,secciones,direccion)
            
            if chboxVert2:
                calcularangulos(vv3, vv1, vv2,secciones,direccion)
                        
        
        bmesh.update_edit_mesh(me, True)
    
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        oa = bpy.context.active_object
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                viewport = area.regions[4]
                v_m = area.spaces[0].region_3d.view_matrix  #orientation matrix
                
                vert = [v for v in bm.verts if (v.select == True and v.hide == False)]
                if len(vert) ==3:
                    self.main(context, self.chboxVert0, self.chboxVert1, self.chboxVert2, self.cortes)
                else:    
                    msg = "select  3  vertices"
                    self.report({"WARNING"}, msg)
                    return {'CANCELLED'}  


        return {'FINISHED'}
    
    

        
                 
    

class equalangleBisectorOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    #bl_context = "editmode"
    bl_label = " Equal Angle bisector"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        
        row.operator(equalangleBisectorOperator.bl_idname) 
        
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
