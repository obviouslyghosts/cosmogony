from Utilities.OEF import OEFClass
from math import radians

class ArrayClass():

    def __new_OEF(self, NAME='', COUNT=0, ISUNIFORM=True):
        o = OEFClass(self.debug, self._d)
        o.Update(   SCENE_NAME=NAME,
                    OBJECT_LINK='',
                    SCENE_COUNT=COUNT,
                    IS_UNIFORM=ISUNIFORM,
                    MIN_VERTS=0
                )
        return o

    def __list_product(self, a):
        n = 1
        if type(a) is list:
            for i in a: n*=i
            return n
        return a

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'ARRAY']
        self._d = _d
        self.bpy = bpy
        self.r = r

        self.name = 'ARRAY'
        self.array_size = list(self.r.RandomInt([1,10]) for i in range(3))

        n=1
        self.ob_1 = {   'NAME' : 'ARRAY',
                        'COUNT': self.__list_product(self.array_size),
                        'UNIF' : self.r.RandomInt([0,1])#True
                    }

        self.Objects = {}
        super(ArrayClass, self).__init__()

    def __deselect_all(self):
        if len(self.bpy.context.selected_objects) > 0:   #
            #self.debug(self._d,'__deselect_all()','deselecting All','BEGIN')
            self.bpy.ops.object.select_all()             # delect all

    def Name(self):
        return self.name

    def Get_Object_List(self, complexity):
        self.Objects = {
                self.ob_1['NAME']: self.__new_OEF(NAME=self.ob_1['NAME'], COUNT = self.ob_1['COUNT'], ISUNIFORM=self.ob_1['UNIF'])
            }
        self.debug(self._d, 'Get_Object_List()','Getting List from', self.name)
        return self.Objects

    def Place_Objects(self, object_list):
        self.debug(self._d,'Place_Objects()','Placing Objects','BEGIN')

        c_ob = object_list[self.ob_1['NAME']].GetAttribute('OBJECT_LINK')
        c_ob.name = self.ob_1['NAME']

        c_ob.rotation_euler = list(radians(self.r.RandomUnif([0,90])) for i in range(3))

        self.__deselect_all()
        child = []
        #draw empty
        self.bpy.ops.object.empty_add(type='PLAIN_AXES')
        e = self.bpy.context.selected_objects[0]
        e.name = 'array_parent'

        self.__deselect_all()

        c_ob.select_set(state=True)

        if self.r.RandomInt([0,1]):
            a_step = list(self.r.RandomUnif([c_ob.dimensions[i]*.5,c_ob.dimensions[i]*2]) for i in range(3))
        else:
            avg = sum(c_ob.dimensions[i] for i in range(3)) / 3
            a_step = list(self.r.RandomUnif([avg*.5, avg*2]) for i in range(3))

        self.debug(self._d,'Place_Objects()','Array Step Size', a_step)

        a_start = list(self.array_size[i]*a_step[i] for i in range(3))
        self.debug(self._d,'Place_Objects()','Array Start Location', a_start)

        a = 0
        for x in range(self.array_size[0]):
            for y in range(self.array_size[1]):
                for z in range(self.array_size[2]):

                    if a > 0:
                        self.bpy.ops.object.duplicate()
                        c_ob = self.bpy.context.selected_objects[0]
                    c_ob.location = (
                            (-a_start[0]/2) + (x*a_step[0]),
                            (-a_start[1]/2) + (y*a_step[1]),
                            (-a_start[2]/2) + (z*a_step[2]),
                            )
                    child.append(c_ob)
                    a+=1

        for i in child:
            i.parent = e

        a_rot = list(radians(self.r.RandomUnif([0,90])) for i in range(3))
        c_ob.select_set(state=False)
        e.select_set(state=True)
        e.rotation_euler = a_rot
        e.select_set(state=False)
