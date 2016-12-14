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
 "name": "ganchos y bisagras",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "ganchos y bisagras ",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 


import bpy
import bmesh
import mathutils
import math





def vertices_conectados(self,context):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    
    
    print("#"*20)
    
    '''
    * revisamos todos los vertices en el plano,
    * luego  vemos solamente los vertices seleccionados
    * creamos una lista local donde almacenaremos los indices
    * por cada vertice seleccionado, verificamos  los bordes (e) que tiene conectados
    * de cada uno de esos bordes (e), vemos cuales vertices (a) lo componen
    * verificamos q el indice de ese vertice (a) no este ya en la lista y que sea diferente al indice del vertice seleccionado, en ese caso lo agregamos a la lista
    * luego agregamos al diccionario global _conectados como clave el indice del vertice seleccionado y como valores la lista con los vertices anteriormente evaluados:
    '''

    for vert in bm.verts:        
        if vert.select:
            self._verticesSeleccionados.append(vert.index)
            self._verticesInvolucrados.append(vert.index)
            #print(tuple(vert.co))
            lista = []
            
            for e in vert.link_edges:
                for a in e.verts:
                    if a.index not in lista and a.index != vert.index:
                        lista.append(a.index)
                        if a.index not in self._verticesInvolucrados:
                            self._verticesInvolucrados.append(a.index)
                        
            self._conectados[vert.index]=lista
    
    #print(self._conectados)
    #print("lista: ",lista)
    self._verticesInvolucrados.sort() #ordeno la lista de todos los vertices involucrados
    '''
    *  llamamos cada una de las claves (indices de vertices seleccionados) almacenados en el diccionario _conectados
    * guardamos cada coordenada de los vertices como clave y como valor el indice de ese vertice
      se hace asi para luego renombrar los vertices creados y facilitar la coneccion de los ganchos posteriormente
    
    for a in self._conectados:
        self._coordenadas_emptys[tuple(bm.verts[a].co)]=a
      
        #print(a)
        if tuple() not in self._coordenadas_emptys:
            self._coordenadas_emptys.append(tuple(bm.verts[a].co))
       
        
        #print(self._conectados[a])
        for e in self._conectados[a]:
            self._coordenadas_emptys[tuple(bm.verts[e].co)]=e

            if tuple(bm.verts[e].co)  not in self._coordenadas_emptys:
                self._coordenadas_emptys.append(tuple(bm.verts[e].co))
         
    
    #print(self._coordenadas_emptys)
    '''
    bmesh.update_edit_mesh(me, True)
    
def crear_empty(self,context):
    for localizacion in  self._coordenadas_emptys:
        bpy.ops.object.empty_add(type='PLAIN_AXES', 
                                 radius=0.01, 
                                 view_align=False, 
                                 location=localizacion, 
                                 rotation=(0.0, 0.0, 0.0), 
                                 layers=(False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

def renombrado_empty(self,context):
    
    '''
    * busco todos los posibles objetos que pueden ser seleccionados de tipo EMPTY
    * luego a ese empty le cambio el nombre por el string del index del vertice correspondiente que almacene en el diccionario _coordenadas_emptys
    '''
    contador = -1
    for objeto in bpy.context.selectable_objects:
        if objeto.type =="EMPTY":
            contador+=1
            index_vertice= self._verticesInvolucrados[contador]
            nombre = str(index_vertice)
            objeto.name= nombre
            objeto.scale=(0.01,0.01,0.01)
           #print(objeto.location)

def crear_ganchos(self,context): 
    
    for vertice_index in self._verticesInvolucrados:
        bpy.ops.mesh.select_all(action='DESELECT')
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        if hasattr(bm.verts, "ensure_lookup_table"): 
            bm.verts.ensure_lookup_table()
            # only if you need to:
            # bm.edges.ensure_lookup_table()   
            # bm.faces.ensure_lookup_table()
        
                
        bm.verts[vertice_index].select=True
        
        bpy.ops.object.hook_add_newob()
        
        bmesh.update_edit_mesh(me, True)
      
    
    #SELECCIONAMOS LOS VERTICES ORIGINALES    
    bpy.ops.mesh.select_all(action='DESELECT')
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
        
    if hasattr(bm.verts, "ensure_lookup_table"): 
        bm.verts.ensure_lookup_table()
            # only if you need to:
            # bm.edges.ensure_lookup_table()   
            # bm.faces.ensure_lookup_table()    
    for vertice_index in self._verticesSeleccionados:       
        bm.verts[vertice_index].select=True
        
    
    bmesh.update_edit_mesh(me, True)
        

def  renombrado_ganchos(self,context):

    '''
    tomamos cada modificador de tipo gancho ("hook") que tenga el objeto
    y le cambiamos el nombre por el objeto (el empty) al que esta conectado
    '''
    for modifier in self.objeto_activo.modifiers:
        if modifier.type == "HOOK":
            modifier.name = modifier.object.name
            #print (modifier.name)


        
def limitar_distancia(self, context):
    '''
    * deseleccionamos todo
    * buscamos en el diccinario _conectados, los verticesprincipales seleccionados
    * cada uno de ellos lo vamos seleccionando y haciendo activo cada vez
    * luego de estar seleccionado y activo, llamamos cada uno de los vertices alos cuales esta conectado y que estan el el diccionario _conectados.
    *creamos un nuevo nombre para  el resultado de restricción de distancia (constraint) que vamos a realizar, el nombre es el vertice principal junto all vertice que se va a limitar la distancia
    * creamos unna nueva restriccion de distancia ligada al vertice seleccionado
    *le asignamos como target cada uno de los vertices conectados por un edge (sub_vert)
    * activamos el limit mode y el use tranform limit
    * por ultimo deseleccionamos este vertice para seguir con el siguiente en el ciclo.
    '''
    bpy.ops.object.select_all(action='DESELECT')
    
        
    for vert in self._conectados:    
        print(vert)    
        bpy.context.scene.objects.active = bpy.data.objects[str(vert)]    
        bpy.context.active_object.select=True
        #print("objeto inicial: ", obj)
        #print(self._conectados[obj])
        for sub_vert in self._conectados[vert]:
            #print(sub_obj)
            nombre=str(vert)+"-"+str(sub_vert)
            bpy.ops.object.constraint_add(type='LIMIT_DISTANCE')            
            bpy.context.object.constraints["Limit Distance"].name  = nombre
            bpy.context.object.constraints[nombre].target = bpy.data.objects[str(sub_vert)]
            bpy.context.object.constraints[nombre].limit_mode = 'LIMITDIST_ONSURFACE'
            bpy.context.object.constraints[nombre].use_transform_limit = True

        bpy.context.active_object.select=False

    
class ganchosBisagrasOperator(bpy.types.Operator):
    "ganchos y visagras "
    bl_idname = 'mesh.ganchosybisagras'
    bl_label = 'ganchos y bisagras'
    bl_description  = "ganchos y bisagras"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def main(self, context):  
        ## creamos variables, listas y diccionarios globales
        self.objeto_activo =  bpy.context.active_object
        self._verticesSeleccionados=[] # guarda los vertices seleccionados originales
        self._verticesInvolucrados=[] #todos los vertices involucrados en la operacion
        self._coordenadas_emptys={} # listado de coordenadas para crear emptys
        self._conectados={} #diccionario que almacerara vertices principales y a  cuales vertices esta conectado
        
        
        
        bpy.ops.object.mode_set(mode='EDIT', toggle=False) #Ingreso a editmode. aunque ya estoy
        vertices_conectados(self,context) #verifico los vertices conectados y guardo las coordenadas para crear emptys
        crear_ganchos(self,context) #creamos los ganchos
        renombrado_empty(self,context) #renombramos los emptys para q concuerden con los indices de los vert   
        renombrado_ganchos(self,context)   #renombramos los ganchos 
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False) #salgo momentaneamente a modo objeto
        
        bpy.ops.object.select_all(action='DESELECT')
        
        limitar_distancia(self, context) #limitamos la distancia entre los ganchos
        
    
       
        bpy.context.scene.objects.active = bpy.data.objects[self.objeto_activo.name]    
        self.objeto_activo.select=True    
        #
        #bpy.ops.object.mode_set(mode='EDIT', toggle=False) #Ingreso nuevamente editmode. 
        
         
                        
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context)
        return {'FINISHED'}
    
    
class ganchosBisagrasOperatorPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Ganchos y Bisagras"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.operator(ganchosBisagrasOperator.bl_idname) 



    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()