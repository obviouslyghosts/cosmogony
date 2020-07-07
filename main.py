import os, sys
import bpy
from random import randint

bpy.context.preferences.view.show_tooltips_python = True
_d = [True,'--', 'MAIN' ]

scene_data = {  'seed': randint(0,1000000),
                'scene_complexity' : 50000000, #[1,100],
                'res' : [1920,1920, 100],
                'engine':'BLENDER_EEVEE', #'CYCLES',
                'auto_save':False}#,
                #'post_history':folders.f_post_history}


os.system("cls")
project = 'F:\\Projects\\cosmogony\\'

#print( scene_data['seed'] )
#project = os.path.abspath(os.curdir)
print( project )
if project not in sys.path: sys.path.append( project )

import Utilities.Debug
import Utilities.FolderStructure
import Modules.Ops
import Utilities.SeededRandom
import Modules.Cameras.CameraManager
import Modules.Scenes.SceneManager
import Modules.Shaders.ShaderManager

d = Utilities.Debug.DebugClass().debug
folders = Utilities.FolderStructure.FolderStructureClass( os, project, d, _d )
r = Utilities.SeededRandom.SeededRandomClass( scene_data['seed'] )
gen_ops = Modules.Ops.OpsClass( bpy, d, _d )
cam_man = Modules.Cameras.CameraManager.CameraManagerClass(bpy, r, d, _d)
sce_man = Modules.Scenes.SceneManager.SceneManagerClass(bpy, r, folders.f_obj, d, _d)
shd_man = Modules.Shaders.ShaderManager.ShaderManagerClass(bpy, r, d, _d)

def DrawScene():
    gen_ops.ClearScene()
    cam_man.AddCam( scene_data['scene_complexity'] )
    oblist = sce_man.BuildScene( scene_data['scene_complexity'] )
    # add materials
    rgb = shd_man.ApplyShaders(scene_data['scene_complexity'], oblist)
    # draw materials
    # add lights


gen_ops.SetupRender(engine=scene_data['engine'], resolution=scene_data['res'])
DrawScene()
