from Modules.Scenes.Layouts.LayoutManager import LayoutManagerClass
from Modules.Scenes.Objects.ObjectManager import ObjectManagerClass

class SceneManagerClass():

    def __init__(self, bpy, r, f_obj_import, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'SCE']
        self._d = _d
        self.bpy = bpy
        self.r = r

        self.layout_manager = LayoutManagerClass(bpy, r, DEBUG, _d)
        self.object_manager = ObjectManagerClass(bpy, r, f_obj_import, DEBUG, _d)
        super(SceneManagerClass,self).__init__()



    def BuildScene(self, complexity, _LAYOUT = '', obj = ''):
        # Choose a layout
        chosen_layout = self.layout_manager.Get_Layout(complexity, _LAYOUT)
        self.debug(self._d, 'BuildMesh()', 'Chosen Layout', chosen_layout.Name())

        # Get object list from layout
        oblist = chosen_layout.Get_Object_List(complexity)
        self.debug(self._d, 'BuildMesh()', 'Object List', 'COMPLETE')

        # Populate object list with geometry
        oblist = self.object_manager.Get_Objects(complexity, oblist)
        self.debug(self._d, 'BuildMesh()', 'Getting Mesh', 'COMPLETE')

        # Place geometry in scene
        chosen_layout.Place_Objects(oblist)
        self.debug(self._d, 'BuildMesh()', 'Placing Objects', 'COMPLETE')

        return oblist
