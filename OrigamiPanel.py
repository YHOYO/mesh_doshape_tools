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
 "name": "Origami",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "Origami Panel",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Doshape"} 

import bpy
import webbrowser

def opendoshapeurl(self):
    print("PANEL ORIGAMI CARGADO CON EXITO")
    webbrowser.open('http://doshape.com/')

def donar(self):
    print("gracias por donar")
    webbrowser.open('http://doshape.com/xojo/donativos/')
####################################################################################### 
 ########################### Seleccionar / Deseleccionar ###############################
 ############################### en todas las pantallas ###############################
 #######################################################################################       

class opendoshapeurloperator(bpy.types.Operator):
    """execute script """
    bl_idname = "mesh.opendoshapeurl"
    bl_label = "Open D_O Shape web site"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        opendoshapeurl(self)
        donar(self)
        return {'FINISHED'}       
 

class opendoshapeurlPanel(bpy.types.Panel):
    bl_category = "Origami"
    bl_label = "Abrir Website"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
       
    def draw(self, context):
        
        layout = self.layout
        row = layout.row(align=True)
        row.operator(opendoshapeurloperator.bl_idname)  
		
		
class SeleccionarPanel(bpy.types.Panel):
    bl_category = "Origami"
    bl_label = "Seleccionar / Deseleccionar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    

 
    def draw(self, context):

        layout = self.layout         
        col = layout.column(align=True)

        row = col.row(align=True)
       
        row.operator("mesh.select_all", text="All / Todo")    
        row.operator("view3d.select_border",text="Area", icon='BORDER_RECT')
        row = col.row(align=True) 
        row.operator("view3d.select_circle",text="Circulo")
        row.operator("mesh.select_linked", text="Objecto") 
        col.operator("view3d.ruler", text="Medir/Measure", icon='NDOF_TRANS')
    
        row = layout.row()
        row.label(text="Cambiar tipo")
        row = layout.row()       
        
        split = layout.split()
        col = split.column(align=True)  
        
        col.operator("mesh.select_mode", text="Vertices/Vertex", icon='VERTEXSEL').type = 'VERT'
        col.operator("mesh.select_mode", text="Borde/Edge", icon='EDGESEL').type = 'EDGE'
        col.operator("mesh.select_mode", text="Cara/Face", icon='FACESEL').type = 'FACE'
        
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True) 
        row = layout.row()
        row.label(text="Ocultar / Mostrar")
        row = layout.row() 
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)
        
        
        props = row.operator("wm.context_toggle_enum", text="Transparente / Solido")
        props.data_path="space_data.viewport_shade"
        props.value_1="SOLID"
        props.value_2="WIREFRAME"
        row = layout.row() 
        row.operator("mesh.hide", text="Ocultar/Hide", icon='GHOST_ENABLED')
        row.operator("mesh.reveal", text="ver/unhide", icon='RESTRICT_VIEW_OFF')
        row.operator("mesh.hideshow",text="V/O INV")
 
 
 ####################################################################################### 
 ################################### Agregar Objetos ###################################
 #######################################################################################   

    
class ObjetosPanel(bpy.types.Panel):

    bl_category =  "Origami"#"Objetos"
    bl_label = "Objetos y Symbolos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
 
    
  
    def draw(self, context):
        layout = self.layout  
          
        row = layout.row()
        row.label(text="Agregar Objetos / Add Objets")
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)   
        row.operator("mesh.primitive_plane_add", text="Plano", icon='MESH_PLANE')
        props = row.operator("mesh.primitive_circle_add", text="Ngon", icon='MESH_CIRCLE')
        props.vertices = 3
        props.radius = 1
        props.fill_type = 'NGON'
        layout = self.layout  
          
        row = layout.row()
        row.label(text="Simbolos")
        layout.operator("mesh.add_origami_symbol", text="Origami Symbols");
        
        

 ####################################################################################### 
 ##################################### Funciones #######################################
 #######################################################################################        

class FuncionesPanel(bpy.types.Panel):

    bl_category =  "Origami"#"Funciones"
    bl_label = "Funciones"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout    
        
        row = layout.row()
        split = layout.split()
        col = split.column(align=True) 
        
        row.label(text="Funciones / Funtions")
        row = layout.row()
        split = layout.split()
        col = split.column(align=True)
        row.operator("screen.screen_full_area", text="full zone", icon='FULLSCREEN')
        row.operator("screen.region_quadview", text="cuatri zone", icon='SPLITSCREEN')
        
        row = layout.row()
        row.operator('mesh.save_txt_lenghts', text="save lenght vertex group")
        
        
        split = layout.split()
        col = split.column(align=True)       
        col.operator("object.editmode_toggle", text="Edición / Edit", icon='EDITMODE_HLT')  
        col.operator("sculpt.sculptmode_toggle", text="Paint", icon='BRUSH_DATA')       
        col.operator("sculpt.sculptmode_toggle", text="Modelado/Sculpt", icon='SCULPTMODE_HLT')
               
        split = layout.split()
        row = col.row(align=True)
        props = row.operator("wm.context_set_enum", text="VER CP", icon='GREASEPENCIL')
        props.data_path="area.type"
        props.value="IMAGE_EDITOR"
        
       



####################################################################################### 
 ################################### Doblar  ############################################
 #######################################################################################       

class DoblarPanel0(bpy.types.Panel):

    bl_category =  "Origami"#"Doblar"
    bl_label = "Fold  0 / Doblar 0"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout         

        
        
        # Doblar 
        
      
        row = layout.row()
        row.label(text="Ganchos y bisagras")
        row = layout.row()
        
        # si no carga activar el addon pivote.py
        #row = col.row(align=True)
        row.operator("mesh.ganchosybisagras", text= "ganchos y Bisagras", icon='HOOK')
        
        row = layout.row()
        row.operator("ops.aplicaryeliminarmodificadoresyemptys", text= "Aplicar", icon='MOD_PHYSICS')
        
        row = layout.row()
        row.operator("ops.aplicaryeliminarmodificadoresyemptys", text= "Cancelar!", icon='CANCEL')
        
        col = layout.column(align=True)
        
        
        
        
 ####################################################################################### 
 ################################### Doblar # si no carga activar el addon pivote.py ############################################
 #######################################################################################       

class DoblarPanel1(bpy.types.Panel):

    bl_category =  "Origami"#"Doblar"
    bl_label = "Fold 1 / Doblar 1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout         

        
        
        # Doblar 
        
      
        row = layout.row()
        row.label(text="Doblar")
        row = layout.row()
        
        # si no carga activar el addon pivote.py
        #row = col.row(align=True)
        row.operator("mesh.separa_conecta_caras", text= "separar/conectar caras")
        row.operator("mesh.moververtices", text="Mover", icon='MAN_TRANS')  
        
        row = layout.row()
        props = row.operator("view3d.pivot_point_set", text="Pivote Elemento Activo", icon='STYLUS_PRESSURE')
        props.type="ACTIVE_ELEMENT"
        
        row = layout.row()
        props = row.operator("transform.rotate", text="Left Slow", icon='STYLUS_PRESSURE')
        props.value = 0.392699
        props.constraint_axis=(True, False, True)
        props.constraint_orientation = "NORMAL"
        
        props = row.operator("transform.rotate", text="Right Slow", icon='STYLUS_PRESSURE')
        props.value = -0.392699

        props.constraint_axis=(True, False, True)
        props.constraint_orientation = "NORMAL"
        
        
        row = layout.row()
        props = row.operator("transform.rotate", text="Left Total", icon='STYLUS_PRESSURE')
        props.value = 3.141599
        props.constraint_axis=(True, False, True)
        props.constraint_orientation = "NORMAL"
        
        props = row.operator("transform.rotate", text="Right Total", icon='STYLUS_PRESSURE')
        props.value = -3.141599
        props.constraint_axis=(True, False, True)
        props.constraint_orientation = "NORMAL"
       
        col = layout.column(align=True)
        

        
        
        
####################################################################################### 
 ################################### Doblar b # si no carga activar el addon pivote.py ############################################
 #######################################################################################       

class DoblarPanel2(bpy.types.Panel):

    bl_category =  "Origami"#"Doblar"
    bl_label = "Fold 2/ Doblar 2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout         

        # si no carga activar el addon pivote.py
       
        # Doblar 
        
      
        row = layout.row()
        row.label(text="Doblar")
        row = layout.row()
            
        
        props = row.operator("view3d.pivot_point_set", text="Cursor como Pivote", icon='ROTACTIVE')
        props.type="CURSOR"
        
        row = layout.row()
        props = row.operator("view3d.snap_cursor_to_selected", text="Unir Cursor a lo seleccionado")
        
        row = layout.row()
        props = row.operator("transform.rotate", text="Doblar")
        props.value = 0.399680652
        props.constraint_orientation="VIEW"
        
        row = layout.row()
        
####################################################################################### 
 ################################### Doblar b ############################################
 #######################################################################################       

class MundoPanel(bpy.types.Panel):

    bl_category =  "Origami"#"Doblar"
    bl_label = "Mundo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout         

        
        ob = context.object
        row = layout.row()
        row.column().prop(ob, "rotation_euler", text="Rotación general")
        
        
        row = layout.row()
        row.label(text="Orbita")
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)

        props = row.operator("view3d.view_orbit", text="Left")
        props.type = "ORBITLEFT"
        props = row.operator("view3d.view_orbit", text="Right")
        split = layout.split()
        row = col.row(align=True)
        props.type = "ORBITRIGHT"
        props = row.operator("view3d.view_orbit", text="UP")
        props.type = "ORBITUP" 
        props = row.operator("view3d.view_orbit", text="Down")
        props.type = "ORBITDOWN"
####################################################################################### 
 ################################### Unfold ##########################################
 #######################################################################################
        
class UnfolPanel(bpy.types.Panel):

    bl_category =  "Origami"#"aqui el panel"
    bl_label = "Unfold"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout 
        col = layout.column()
        col.operator("mesh.uv_3d_proyection", text="Unfold", icon='RECOVER_AUTO')       
 
        
 ####################################################################################### 
 ################################### Pliegues ##########################################
 #######################################################################################
        

class MarcasPanel(bpy.types.Panel):

    bl_category =  "Origami"#"Marcas"
    bl_label = "Marcas"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout 
                
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True) 
        row = layout.row()
        row.label(text="Funciones Rapidass")
        row = layout.row() 
        props = row.operator("object.modifier_add", text="Mirror", icon="MOD_MIRROR" )
        props.type='MIRROR'
        
        row.operator("mesh.hideshow",text="Ocultar Mostrar Inverso")
        row = layout.row()
        row.operator("mesh.joinexplote", text = "explorar/unir caras")
        row.operator("view3d.index_visualiser", text="Visualize indices")
        
        row = layout.row()
        props =row.operator("view3d.viewnumpad", text = "ver cara")
        props.type = "TOP"
        props.align_active = True
        
        
        
        row = layout.row()
        row.label(text="Dibujar Linea")
        row = layout.row() 
        props = row.operator("mesh.knife_tool", text="Total")
        props.use_occlude_geometry = False
        props.only_selected = False
        props = row.operator("mesh.knife_tool", text="Seleccionado")
        props.use_occlude_geometry = False
        
        
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True) 
        #row = layout.row()
        row.label(text="Dividir")
        row = col.row(align=True)
        props = row.operator("mesh.subdivide", text="Todo", icon='MESH_GRID') 
        props.number_cuts = 1
        props.quadtri = True
        props.quadcorner = 'FAN'   
        
        row.operator("mesh.loopcut_slide",text="Medios")
        
        
        row = col.row(align=True)
        
        row.operator('mesh.joinbisectorline', text = "cortar con 2")        
        row.operator("mesh.vert_connect", text="Conectar 2", icon='GREASEPENCIL')
        
        row1 = col.row(align=True)
        row1.operator('mesh.perpbisectorcircumcenter', text = "circuncentro")
        
        props = row1.operator("mesh.inset", text="inset")
        props.use_boundary = True
        props.use_even_offset = True
        
        
        row2 = col.row(align=True)
        row2.operator('mesh.perpbisectorline', text = "90 grados")
        row2.operator('mesh.trianglebisector', text = "Oreja Conejo")
        
               
        row3 = col.row(align=True)
        row3.operator('mesh.perpbisectororthocenter', text  ="ortocentro")
        row3.operator("mesh.quads_convert_to_tris", text="Diagonal") 
        
        row4 = col.row(align=True)
        row4.operator('mesh.equalanglebisector', text  ="Equal Angle")
        row4.operator("mesh.anglebisector", text="cortan en angulo")

        row6 = col.row(align=True)
        row6.operator('object.mesh_edge_length_set', text  ="set length")
        row6.operator("mesh.edge_angle_set", text=" set angle")
        
        
        row7 = col.row(align=True)
        row7.operator('mesh.edgeequalizer', text  ="edge equalizer")
        #row7.operator("mesh.edge_angle_set", text=" set angle")
        
		
	
        
				
		
		
        



        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True) 
        
        row = layout.row()
        row.label(text="Borrar")
         
        
        row = layout.row() 
        props = row.operator("mesh.merge", text="combinar", icon='AUTOMERGE_ON') 
        props.type = "CENTER"
        props.uvs = True
        
        
        props = row.operator("mesh.rip", text="separar", icon='FULLSCREEN_ENTER') 
        props.use_fill = False
        props.proportional = "PROJECTED"
        
        row = layout.row()    
        props = row.operator("mesh.dissolve_edges", text="Lineas") 
        props.use_verts= False
        props.use_face_split= True
        
        props = row.operator("mesh.dissolve_verts", text="Puntos") 
        props.use_face_split= False
        
        
            
        
        
        row = layout.row()
        props = row.operator("mesh.dissolve_edges", text="Lineas y Puntos") 
        props = row.operator("mesh.delete", text="Todo") 
        props.type= "VERT"

        
        
        

        
 ####################################################################################### 
 ################################### Lineas ############################################
 #######################################################################################
        
class LineasPanel(bpy.types.Panel):

    bl_category =  "Origami"#" O Lineas"
    bl_label = "Lineas"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        
        layout = self.layout 
        row = layout.row(align=True)
        row.label(text="Asignar")
        props = row.operator("mesh.mark_freestyle_edge", text = "Valle") 
        props.clear= False    
        row.operator("mesh.mountainfreestyle", text = "Montaña" ) 
        row.operator("mesh.creasefreestyle", text = "Crease")  
        
        layout = self.layout 
        row = layout.row(align=True)
        row.label(text="Borrar")
        props = row.operator("mesh.mark_freestyle_edge", text = "D_Valle") 
        props.clear= True   
        row.operator("mesh.delmountainfreestyle", text = "D_Montaña" ) 
        row.operator("mesh.delcreasefreestyle", text = "D_Crease")  

      
        
        
        layout = self.layout         
        
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True) 
        row = col.row(align=True)
        row.label(text="Tipo")
        
     
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row()
        col.template_list("RENDERLAYER_UL_renderlayers", "", rd, "layers", rd.layers, "active_index", rows=2)

        col = row.column(align=True)
        
        row = layout.row()
        rl = rd.layers.active
        if rl:
            row.prop(rl, "name")
        row.prop(rd, "use_single_layer", text="", icon_only=True)
        
        
        split = layout.split()
        col = split.column(align=True)
        row = layout.row(align=True)
        
              
        col.operator("mesh.mark_freestyle_edge", text="Asignar / Denegar ", icon='BRUSH_DATA')
        rd = context.scene.render
        rl = rd.layers.active
        freestyle = rl.freestyle_settings
        lineset = freestyle.linesets.active

        layout.active = rl.use_freestyle

        row = layout.row()
        rows = 5 if lineset else 2
        row.template_list("RENDERLAYER_UL_linesets", "", freestyle, "linesets", freestyle.linesets, "active_index", rows=rows)

        sub = row.column(align=True)
        sub.operator("scene.freestyle_lineset_add", icon='ZOOMIN', text="")
        sub.operator("scene.freestyle_lineset_remove", icon='ZOOMOUT', text="")
        sub.menu("RENDER_MT_lineset_specials", icon='DOWNARROW_HLT', text="")
        if lineset:
            sub.separator()
            sub.separator()
            sub.operator("scene.freestyle_lineset_move", icon='TRIA_UP', text="").direction = 'UP'
            sub.operator("scene.freestyle_lineset_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
            
         
                          
 ####################################################################################### 
 ################################### Render  ##########################################
 #######################################################################################
        

class RenderPanel(bpy.types.Panel):

    bl_category =  "Origami"#"Render"
    bl_label = "Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout         
        
        
                      
        split = layout.split()
        col = split.column(align=True)
        row = layout.row(align=True)
        col.label(text="Imagen")
        col.operator("view3d.camera_to_view", text="Alinear camara", icon='RESTRICT_RENDER_OFF')
        
               
        row1 = col.row(align=True)
        row1.operator("render.opengl", text="Rapida", icon='RESTRICT_VIEW_OFF')
        row1.operator("render.render", text="Real", icon='RENDER_STILL')
        
        row2 = col.row(align=True)
        row2.operator("object.render_save_scenes", text="Render_Save_all", icon='RENDER_STILL')
        
        split = layout.split()
        col = split.column(align=True)      
        col.operator("scene.new", text="Nuevo Paso / Next Step", icon='FORWARD').type = 'FULL_COPY'
        

        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True) 
        row = layout.row()
        row.label(text="Color de caras")
        row = layout.row() 
        
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.normals_make_consistent", text="Recalculate")
        row.operator("mesh.flip_normals", text="cambiar")
          
        

 ####################################################################################### 
 ################################### Modificar ##########################################
 #######################################################################################    
    

          
class MaterialPanel(bpy.types.Panel):    

    bl_category =  "Origami"#"Render"
    bl_label = "Diffuse"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_GAME'}

    @classmethod
    def poll(cls, context):
        mat = context.material
        engine = context.scene.render.engine
        return check_material(mat) and (mat.type in {'SURFACE', 'WIRE'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = active_node_mat(context.material)

        split = layout.split()

        col = split.column()
        col.prop(mat, "diffuse_color", text="")
        sub = col.column()
        sub.active = (not mat.use_shadeless)
        sub.prop(mat, "diffuse_intensity", text="Intensity")

        col = split.column()
        col.active = (not mat.use_shadeless)
        col.prop(mat, "diffuse_shader", text="")
        col.prop(mat, "use_diffuse_ramp", text="Ramp")

        col = layout.column()
        col.active = (not mat.use_shadeless)
        if mat.diffuse_shader == 'OREN_NAYAR':
            col.prop(mat, "roughness")
        elif mat.diffuse_shader == 'MINNAERT':
            col.prop(mat, "darkness")
        elif mat.diffuse_shader == 'TOON':
            row = col.row()
            row.prop(mat, "diffuse_toon_size", text="Size")
            row.prop(mat, "diffuse_toon_smooth", text="Smooth")
        elif mat.diffuse_shader == 'FRESNEL':
            row = col.row()
            row.prop(mat, "diffuse_fresnel", text="Fresnel")
            row.prop(mat, "diffuse_fresnel_factor", text="Factor")

        if mat.use_diffuse_ramp:
            col = layout.column()
            col.active = (not mat.use_shadeless)
            col.separator()
            col.template_color_ramp(mat, "diffuse_ramp", expand=True)
            col.separator()

            row = col.row()
            row.prop(mat, "diffuse_ramp_input", text="Input")
            row.prop(mat, "diffuse_ramp_blend", text="Blend")

            col.prop(mat, "diffuse_ramp_factor", text="Factor")



        
class MaterialesPanel(bpy.types.Panel):

    bl_category =  "Origami"#"Render"
    bl_label = "Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    

 
    def draw(self, context):
        layout = self.layout 
        
        
    
class ParamodificarPanel(bpy.types.Panel):

    bl_category =  "Origami"#"aqui el panel"
    bl_label = "Para modificar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    

 
    def draw(self, context):
        layout = self.layout 
#
#	Registration
#   All panels and operators must be registered with Blender; otherwise
#   they do not show up. The simplest way to register everything in the
#   file is with a call to bpy.utils.register_module(__name__).
#

def register():
    bpy.utils.register_module(__name__)
  


def unregister():
    
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()

