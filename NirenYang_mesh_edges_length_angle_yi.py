bl_info = {
	'name': "set length and angle",
	'description': "length and angle",
	'author': "NirenYang [BlenderCN]",
	'version': (0, 0, 2),
	'blender': (2, 7, 0, 5),
	'location': '[Toolbar][Tools][Mesh Tools][edges set]: set Length(Shit+Alt+E) | set Angle(Ctrl+Shit+Alt+E)',
	'warning': "",
	'category': 'Doshape',
	"wiki_url": "http://blenderartists.org/forum/showthread.php?335568-A-tinny-addon-for-directly-set-edge-length",
	"tracker_url": "https://developer.blender.org/maniphest/task/edit/39999/",
}


#引入blender核心
import bpy, bmesh, math, mathutils

#基本类型
from bpy.props import BoolProperty, FloatProperty, EnumProperty

#定义操作
class LengthSet(bpy.types.Operator):
	#操作名称(2.70.5 原本是mesh.edge，但现在工具栏是OT，要加入这个位置还只能是object，也许以后会修改)
	bl_idname = "object.mesh_edge_length_set"
	#标签
	bl_label = "length_set"
	#说明
	bl_description = "change active edge length (Shit+Alt+E)"
	#返回
	bl_options = {'REGISTER', 'UNDO'}
	
	#目标长度
	target_length = FloatProperty(name = 'length', default = 0.0)
	
	#缩放中心
	switch_point = BoolProperty(
		name="switch point",
		default=False,
		description="switch point")
		
	count = 0
	me = vts_sequence = None
	
	@classmethod
	def poll(cls, context):
		return (context.edit_object)

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)	
		
	#运行
	def execute(self, context):
		# if self.target_length == 0:
			# return {'FINISHED'}	
			
		self.count += 1
		if self.count == 1:
			# 初始化
			ob = context.edit_object

			# 准备
			self.me = ob.data
			
			self.switch_point = False
			
			bm = bmesh.from_edit_mesh(self.me)
			# 选择顺序 重新判断长度是为了识别模式切换
			if len(bm.select_history) > 1 and isinstance(bm.select_history[-1], bmesh.types.BMVert):
				self.vts_sequence = [i.index for i in [bm.select_history[j] for j in (-2,-1)]]
			elif len(bm.select_history) > 0 and isinstance(bm.select_history[-1], bmesh.types.BMEdge):
				self.vts_sequence = [i.index for i in bm.select_history[-1].verts]
			else:
				self.report({'ERROR'}, '0,1 edge OR 2 points; 1,don\'t support Face mode; 2,Changing select mode will Lost select-history')
				return {'CANCELLED'}
			
			# 当前长度
			if abs(self.target_length) < 0.000000000001:
				if self.switch_point:
					tmp_vts_sequence = [self.vts_sequence[-1], self.vts_sequence[-2]]
				else:
					tmp_vts_sequence = self.vts_sequence
				vector = bm.verts[tmp_vts_sequence[-2]].co - bm.verts[tmp_vts_sequence[-1]].co
				self.target_length = vector.length
			self.execute(context)
		else:
			bm = bmesh.from_edit_mesh(self.me)
			
			if self.switch_point:
				tmp_vts_sequence = [self.vts_sequence[-1], self.vts_sequence[-2]]
			else:
				tmp_vts_sequence = self.vts_sequence
			
			vector = bm.verts[tmp_vts_sequence[-2]].co - bm.verts[tmp_vts_sequence[-1]].co
			vector.length = abs(self.target_length)
			if self.target_length > 0:
				bm.verts[tmp_vts_sequence[-1]].co = bm.verts[tmp_vts_sequence[-2]].co - vector
			elif self.target_length < 0:
				bm.verts[tmp_vts_sequence[-1]].co = bm.verts[tmp_vts_sequence[-2]].co + vector
			# 刷新视窗数据
			bmesh.update_edit_mesh(self.me, True)
		return {'FINISHED'}

# def AngleDir(fwd, targetDir, up):
	# """-1左, 1右, 0 前后"""
	# perp = fwd.cross(targetDir)
	# dir = perp.dot(up)
	# # return dir
	# if dir > 0:
		# return 1
	# elif dir < 0:
		# return -1
	# else:
		# return 0

class AngleSet(bpy.types.Operator):
	#操作名称
	bl_idname = "mesh.edge_angle_set"
	#标签
	bl_label = "angle_set"
	#说明
	bl_description = "change connecting 2 edges angle (Ctrl+Shit+Alt+E)"
	#返回
	bl_options = {'REGISTER', 'UNDO'}
	
	#角度
	target_angle = FloatProperty( name = 'angle', default = 0.0)	
	# defined_up = EnumProperty(items = [("object", "object", ""),
										# ("world", "world", ""),
										# ("view", "view", ""),
										# ("normal", "normal", "")],
								# default = 'normal',
								# name = "defined up",
								# description ="defined up axis for differentiate left/right")
	
	count = 0
	me = None
	rotate_id = rotate_point = rotate_center = rotate_normal = originLength = None
	
	@classmethod
	def poll(cls, context):
		return (context.edit_object)
		
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)		
		
	def execute(self, context):
		self.count += 1
		if self.count == 1:
			ob = context.edit_object

			self.me = ob.data
			bm = bmesh.from_edit_mesh(self.me)

			# 选择顺序
			if len(bm.select_history) > 1 and isinstance(bm.select_history[-1], bmesh.types.BMEdge):
				edge_sequence = [bm.select_history[-1], bm.select_history[-2]]
				# 三个点 左中右
				points3 = [None, None, None]
				for i in bm.select_history[-1].verts:
					if i in bm.select_history[-2].verts:
						points3[1] = i.index
					else:
						points3[0] = i.index
				for i in bm.select_history[-2].verts:
					if i not in bm.select_history[-1].verts:
						points3[2] = i.index
				# print('当前三点:', points3)
			elif len(bm.select_history) > 2 and isinstance(bm.select_history[-1], bmesh.types.BMVert):
				points3 = [i.index for i in bm.select_history]
				points3.reverse()
			else:
				self.report( {'WARNING'}, '0,2 edges OR 3 points; 1,don\'t support Face mode; 2,Changing select mode will Lost select-history' )
				return {'CANCELLED'}
			
			# 坐标
			points3co = [bm.verts[i].co.copy() for i in points3]
			
			self.rotate_id	 = points3[0]
			self.rotate_center = points3co[1]
			self.rotate_point  = points3co[2]
			
			v1, v2 = (points3co[0] - points3co[1]), (points3co[2] - points3co[1])
			if self.target_angle % 360 == 0:
				self.target_angle = math.degrees(v1.angle(v2))
				# 简单就好 simple is good
			self.rotate_normal = v1.cross(v2)
			
			## 改变长度，因为两边的长度可能不一样
			self.originLength = v1.length
			
			self.execute(context)
		else:
			_angle = self.target_angle % 360
			#_angle == 0时，不能再运算，不然只能ctrl z归位
			if _angle == 0:
				_angle = 0.000000000001
			# 错误操作会导致 self.rotate_normal 为0，不管怎么样，大多数人不会那么做，pass
			rotate_matrix = mathutils.Matrix.Rotation(math.radians(_angle), 4, self.rotate_normal)
			
			r_edge = (self.rotate_point - self.rotate_center)
			r_edge.length = self.originLength
			rp = rotate_matrix * r_edge + self.rotate_center
			
			bm = bmesh.from_edit_mesh(self.me)
			bm.verts[self.rotate_id].co = rp
		
			# 刷新视窗数据
			bmesh.update_edit_mesh(self.me, True)
		return {'FINISHED'}
		
#定义面板
def menu_func(self, context):
	#位置
	self.layout.operator_context = 'INVOKE_DEFAULT'
	#按键
	self.layout.label(text="edges set:")	# and Angle
	row = self.layout.row(align=True)
	row.operator(AngleSet.bl_idname, "set angle")
	row.operator(LengthSet.bl_idname, "set length")
	#分割
	#self.layout.separator()
		

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
