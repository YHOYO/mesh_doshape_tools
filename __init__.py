bl_info = {
    "name": "Doshape Mesh tools",
    "author": "yhoyo (Diego Quevedo)",
    "version": (2, 0, 1),
    "blender": (2, 7, 8),
    "category": "Doshape",
    "location": "View3D > EditMode > ToolShelf",
    "wiki_url": "",
    "tracker_url": ""
}


if "bpy" in locals():
    import imp
    imp.reload(angle_bisector)
    imp.reload(CoDEmanX_pivote)
    imp.reload(edge_length_equalizer)
    imp.reload(equal_angles)
    imp.reload(ganchosybisagras)
    imp.reload(HideShow)
    imp.reload(join_bisector)
    imp.reload(join_explote)
    imp.reload(lines_origami_freestyle)
    imp.reload(modificadoresyemptys)
    imp.reload(mover)
    imp.reload(NirenYang_mesh_edges_length_angle_yi)
    imp.reload(origami_symbols)
    imp.reload(OrigamiPanel)
    imp.reload(perpendicular_bisector)
    imp.reload(perpendicular_circum_center)
    imp.reload(perpendicular_orthocenter)
    imp.reload(render_save_all)
    imp.reload(save_length_vertx_groups)
    imp.reload(separaryunircaras)
    imp.reload(triangle_bisector)
    imp.reload(unfold)
    imp.reload(view3d_idx_view2)


else:
    from. import angle_bisector,CoDEmanX_pivote,edge_length_equalizer,equal_angles,ganchosybisagras,HideShow,join_bisector,join_explote,lines_origami_freestyle ,modificadoresyemptys,mover,NirenYang_mesh_edges_length_angle_yi,origami_symbols,OrigamiPanel,perpendicular_bisector  ,perpendicular_circum_center ,perpendicular_orthocenter,render_save_all ,save_length_vertx_groups,separaryunircaras,triangle_bisector,unfold,view3d_idx_view2

import bpy

def register():
    angle_bisector.register()
    CoDEmanX_pivote.register()
    edge_length_equalizer.register()
    equal_angles.register()
    ganchosybisagras.register()
    HideShow.register()
    join_bisector.register()
    join_explote.register()
    lines_origami_freestyle.register()
    modificadoresyemptys.register()
    mover.register()
    NirenYang_mesh_edges_length_angle_yi.register()
    origami_symbols.register()
    OrigamiPanel.register()
    perpendicular_bisector.register()
    perpendicular_circum_center.register()
    perpendicular_orthocenter.register()
    render_save_all.register()
    save_length_vertx_groups.register()
    separaryunircaras.register()
    triangle_bisector.register()
    unfold.register()
    view3d_idx_view2.register()



def unregister():
    angle_bisector.register()
    CoDEmanX_pivote.register()
    edge_length_equalizer.register()
    equal_angles.register()
    ganchosybisagras.unregister()
    HideShow.unregister()
    join_bisector.unregister()
    join_explote.unregister()
    lines_origami_freestyle.unregister()
    modificadoresyemptys.unregister()
    mover.unregister()
    NirenYang_mesh_edges_length_angle_yi.unregister()
    origami_symbols.unregister()
    OrigamiPanel.unregister()
    perpendicular_bisector.unregister()
    perpendicular_circum_center.unregister()
    perpendicular_orthocenter.unregister()
    render_save_all.unregister()
    save_length_vertx_groups.unregister()
    separaryunircaras.unregister()
    triangle_bisector.unregister()
    unfold.unregister()
    view3d_idx_view2.unregister()


if __name__ == "__main__":
    register()