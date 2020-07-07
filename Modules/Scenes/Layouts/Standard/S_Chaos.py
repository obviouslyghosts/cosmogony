from Utilities.OEF import OEFClass
from math import radians

class ChaosClass():

    def __new_OEF(self, NAME='', COUNT=0, ISUNIFORM=True):
        o = OEFClass(self.debug, self._d)
        o.Update(   SCENE_NAME=NAME,
                    OBJECT_LINK='',
                    SCENE_COUNT=COUNT,
                    IS_UNIFORM=ISUNIFORM,
                    MIN_VERTS=0
                )
        return o

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'CHAOS']
        self._d = _d
        self.bpy = bpy
        self.r = r

        self.name = 'CHAOS'
        self.cnt = [3,35]#[3,35]
        self.sz = list(self.r.RandomUnif([1,10]) for i in range(3)) #[5,5,5] #size, safe zone,
        self.obsz = [.8,2] # new object size
        self.Objects = {}
        super(ChaosClass, self).__init__()

    def __set_volume(self, ob, v = 1):
        vol = ob.dimensions.x * ob.dimensions.y * ob.dimensions.z
        n = (v/vol)**(1/3.0)
        temp_v = []
        for i in ob.dimensions:
            temp_v.append(i*n)
        ob.dimensions = temp_v
        self.bpy.ops.object.transform_apply(scale=True)

    def __deselect_all(self):
        if len(self.bpy.context.selected_objects) > 0:   #
            #self.__debug('__deselect_all()','deselecting All','BEGIN')
            self.bpy.ops.object.select_all()             # delect all

    def Name(self):
        return self.name

    def Get_Object_List(self, complexity):
        for i in range(self.r.RandomInt(self.cnt)):
            n = self.name + '_' + str(i)
            self.Objects.update({ n : self.__new_OEF(NAME=n, COUNT = 1, ISUNIFORM=False) })
        self.debug(self._d, 'Get_Object_List()','Getting List from', self.name)
        return self.Objects

    def Place_Objects(self, object_list):
        self.debug(self._d, 'Place_Objects()','Placing Objects','BEGIN')

        for o in object_list:
            c_ob = object_list[o].GetAttribute('OBJECT_LINK')
            c_ob.name = object_list[o].GetAttribute('SCENE_NAME')
            self.__set_volume(c_ob, v = 100)
            new_size = self.r.RandomUnif(self.obsz) #get new dimensions
            c_ob.dimensions = list(i*new_size for i in c_ob.dimensions)
            #c_ob.dimensions = [c_ob.dimensions[0]*new_size,new_size,new_size]
            c_ob.location = list(self.r.RandomUnif([-self.sz[i], self.sz[i]]) for i in range(3))
            c_ob.rotation_euler = list(radians(self.r.RandomUnif([0,90])) for i in range(3))
