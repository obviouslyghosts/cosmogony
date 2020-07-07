from Utilities.OEF import OEFClass
from math import radians, sin, cos

class BubbleClass():
    # GET OBJECT LIST
    # PLACE OBJECTS

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
        _d = [_d[0],_d[1] + ' --', 'BUBL']
        self._d = _d
        self.bpy = bpy
        self.r = r

        self.name = 'BUBBLE'
        self.ob_1 = {   'NAME' : 'CENTER',
                        'COUNT': 1,
                        'UNIF' : True
                    }

#        self.ob_1 = 'CENTER'
#        ob_1_count = 1

        self.ob_2 = {   'NAME' : 'BUBBLE',
                        'COUNT': self.r.RandomInt([5,100]),
                        'UNIF' : self.r.RandomInt([0,1])
                    }

#        self.ob_2 = 'BUBBLE'
#        ob_2_count =


        self.Objects = {}
        super(BubbleClass, self).__init__()

    def __set_volume(self, ob, v = 1):
        vol = ob.dimensions.x * ob.dimensions.y * ob.dimensions.z
        n = (v/vol)**(1/3.0)
        ob.dimensions = list(ob.dimensions[i]*n for i in range(3))
#        temp_v = []
#        for i in ob.dimensions:
#            temp_v.append(i*n)
#        ob.dimensions = temp_v
        self.bpy.ops.object.transform_apply(scale=True)

    def __deselect_all(self):
        if len(self.bpy.context.selected_objects) > 0:   #
            #self.debug(self._d,'__deselect_all()','deselecting All','BEGIN')
            self.bpy.ops.object.select_all()             # delect all

    def Name(self):
        return self.name

    def Get_Object_List(self, complexity):
        self.Objects = {
                self.ob_1['NAME']: self.__new_OEF(NAME=self.ob_1['NAME'], COUNT = self.ob_1['COUNT'], ISUNIFORM=self.ob_1['UNIF']),
                self.ob_2['NAME']: self.__new_OEF(NAME=self.ob_2['NAME'], COUNT = self.ob_2['COUNT'], ISUNIFORM=self.ob_2['UNIF'])
        }
        self.debug(self._d,'Get_Object_List()','Getting List from', self.name)
        return self.Objects

    def Place_Objects(self, object_list):
        self.debug(self._d,'Place_Objects()','Placing Objects','BEGIN')

        self.debug(self._d,'Place_Objects()', 'Object 1', self.ob_1['NAME'])
        object_list[self.ob_1['NAME']].PrintAttr()

        self.debug(self._d,'Place_Objects()', 'Object 2', self.ob_2['NAME'])
        object_list[self.ob_2['NAME']].PrintAttr()

        child = []
        self.__deselect_all()

        #Get base objects
        c_ob = object_list[self.ob_1['NAME']].GetAttribute('OBJECT_LINK')
        c_ob.name = self.ob_1['NAME']
        b_ob = object_list[self.ob_2['NAME']].GetAttribute('OBJECT_LINK')
        b_ob.name = self.ob_2['NAME']

        #draw empty
        self.bpy.ops.object.empty_add(type='PLAIN_AXES')
        e = self.bpy.context.selected_objects[0]
        e.name = 'bubble_parent'
        e.location = (0,0,0)
        self.__set_volume(c_ob, v = 100)
        c_ob.parent = e
        self.bpy.ops.object.select_all()
        self.__deselect_all()

        for o in range(object_list[self.ob_1['NAME']].GetAttribute('SCENE_COUNT')):
            ##c_ob = self.bpy.context.scene.objects[object_list[self.ob_1].GetAttribute('OBJECT_LINK')]
            #c_ob = object_list[self.ob_1].GetAttribute('OBJECT_LINK')
            c_ob.select_set(state=True)
            c_ob.name = self.ob_1['NAME']
            c_ob.location = (0,0,0)
            c_ob.rotation_euler = (0,0,0)
            self.__set_volume(c_ob, v = 100)
            c_ob.parent = e
            c_ob.select_set(state=False)
            self.__deselect_all()

        self.debug(self._d,'Place_Objects()', 'Bubbles Scene Count', str(object_list[self.ob_2['NAME']].GetAttribute('SCENE_COUNT')))

        avg_dim = (b_ob.dimensions.x + b_ob.dimensions.y + b_ob.dimensions.z)/3
        new_size = self.r.RandomUnif([avg_dim/3,avg_dim/1.2])

        #self.debug(self._d,'Place_Objects()', 'placing bubbles', object_list[self.ob_2].GetAttribute('SCENE_COUNT'))

        avg_dim = sum(c_ob.dimensions[i] for i in range(3))/3

        for o in range(object_list[self.ob_2['NAME']].GetAttribute('SCENE_COUNT')):
            #new_ob = self.bpy.context.scene.objects[object_list[self.ob_2].name]
            new_ob = b_ob #object_list[self.ob_2].GetAttribute('OBJECT_LINK')
            new_ob.name = self.ob_2['NAME']
            new_ob.select_set(state=True)

            ##### ##### new_ob.dimensions = list(i for i in range(3))

            # get new location
            tx = radians( 360 * self.r.RandomUnif( [0,1] ) )
            ty = radians( 360 * self.r.RandomUnif( [0,1] ) )
            #self.debug(self._d,'Place_Objects()', 'tx & ty', (str(tx) + ' & '+ str(ty)))

            new_point = (
                (e.location.x + (c_ob.dimensions.x/2 + new_ob.dimensions.x/2) * cos(ty) * sin(tx)),
                (e.location.y + (c_ob.dimensions.y/2 + (new_ob.dimensions.y/2)) * sin(ty) * sin(tx)),
                (e.location.z + (c_ob.dimensions.z/2 + (new_ob.dimensions.z/2)) * cos(ty))
                )

            #self.debug(self._d,'Place_Objects()', 'new point', new_point)
            # scale it
            # rotate it
            # set new position, rotation
            # append to child
            new_ob.location = new_point
            new_ob.dimensions = list(i*new_size for i in c_ob.dimensions)
            new_ob.rotation_euler = (tx,ty,0)
            child.append(new_ob)

            if o < object_list[self.ob_2['NAME']].GetAttribute('SCENE_COUNT')-1:
                self.bpy.ops.object.duplicate()
                self.__deselect_all()
                new_ob = self.bpy.context.scene.objects[0]
            # duplicate if repeating

        self.debug(self._d,'Place_Objects()','Placing Objects','COMPLETE')
