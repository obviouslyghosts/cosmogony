import os
import fnmatch
from math import radians
#

class M_ObjImportClass():

    def __init__(self, bpy, r, DEBUG, _d, _FPATH = ''):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'OBJ']
        self._d = _d
        self.r = r
        self.bpy = bpy

        self.dirpath = _FPATH
        self.fname = ''
        self.name = 'OBJ'
        self.count = 1
        self.vert_count = 8
        super(M_ObjImportClass, self).__init__()

##    def GetObjectCount(self):
##        return len(fnmatch.filter(os.listdir(self.dirpath), '*.obj'))

    def __vert_count(self):
        a = fnmatch.filter(os.listdir(self.dirpath), '*.obj')
        s = self.r.RandomInt([0, len(a)-1]) #selected index
        self.fname = os.path.join(self.dirpath, a[s])
        self.debug(self._d, '__vert_count()', 'self.fname', self.fname)
        v = 0
        with open(self.fname, 'r' ) as obj_file:
            for line in obj_file:
                if line.split(' ')[0] == 'v':
                    v+=1
        self.vert_count = v
        self.debug(self._d, '__vert_count()', 'vert count:', self.vert_count)
        self.debug(self._d, '__vert_count()', 'scene count:', self.count)

        return self.count * self.vert_count

    def Name(self):
        return self.name

    def GetVerts(self, complexity, count = 1):
        #Vert count
        self.count = count
        return self.__vert_count()

    def __set_volume_to_one(self, ob):
##        ob = bpy.context.scene.objects[0]
        ##
        vol = ob.dimensions.x * ob.dimensions.y * ob.dimensions.z
        n = (100/vol)**(1/3.0)
        ob.dimensions = list(ob.dimensions[i]*n for i in range(3))
        ##ob.dimensions = temp_v
        self.bpy.ops.object.transform_apply(scale=True)

    def __secondary_motion(self, ob):
        ob.scale *= self.r.RandomUnif([0.5, 1.5])
        rot = list(radians(self.r.RandomInt([0,1]) * self.r.RandomUnif([-180,180])) for i in range(3))
        ob.rotation_euler = rot
        self.bpy.ops.object.transform_apply( rotation = True )


    def GetObject(self, complexity, extra = 0):
        #exra == left over verts to use for subdividing or beveling or what not

        if self.fname != '':
            self.bpy.ops.import_scene.obj(filepath = self.fname)
            imported_obj = self.bpy.context.selected_objects[0]
            imported_obj.data.materials.clear()

        ob = self.bpy.context.selected_objects[0]
        self.__set_volume_to_one(ob)
        self.__secondary_motion(ob)

        self.bpy.ops.object.shade_smooth()
#        for f in ob.data.polygons:
#            f.use_smooth = True

        if extra > self.vert_count*3:
            subs = ob.modifiers.new('Subsurf', type = 'SUBSURF')
        elif extra > self.vert_count*2:
            bev = ob.modifiers.new('Bevel', type = 'BEVEL')
            bev.width = 0.01
            bev.segments = 2

        self.debug(self._d, 'GetObject()', 'imported obj', 'COMPLETE')
        return ob
