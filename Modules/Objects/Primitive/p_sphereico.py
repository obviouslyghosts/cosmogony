#from Utilities.SeededRandom import SeededRandomClass
#

# --CREATES A MESH--
# ------------------
# -provide currency-
# returns the object
# ------------------
# loc = (0,0,0)-----
# rot = (0,0,0)-----
# size = (1,1,1)----
# dim = (<1,<1,<1)--
# ------------------
class P_SphereIcoClass():

    def __init__(self, bpy, r, DEBUG, _d,  _FPATH = ''):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'P ICO']
        self._d = _d

        self.r = r
        self.bpy = bpy
        self.name = 'P_SPHERE_ICO'
        self.count = 1
        self.radius = [0.5,1.5]
        self.uvs = [1,1]
        self.sub_divisions = [1,4]

        self.bev_segments = self.r.RandomInt([0,1])


        self.calc_uvs = self.r.RandomInt(self.uvs)
        self.subdivisions = 0 #self.r.RandomInt(self.sub_divisions)
        self.v_c =  12 #(10 * 4**(self.subdivisions-1)) + 2
        self.size = self.r.RandomUnif(self.radius)

##        self.attr = {
##            'subdivisions' : self.subdivisions,
##            'size': self.size,
##            'calc_uvs': self.calc_uvs
##            }
        super(P_SphereIcoClass, self).__init__()

    def Name(self):
        return self.name

    def GetVerts(self, complexity, count = 1):
        #Vert count
        #self.__debug('GetVerts()', 'Getting Verts', count)
        self.count = count
        self.subdivisions = self.r.RandomInt(self.sub_divisions)
        self.debug(self._d, 'GetVerts()', 'subdivisions', self.subdivisions)
        f = 20 * 4** (self.subdivisions-1)
        self.debug(self._d,'GetVerts()', 'f', f)

        if self.bev_segments:
            self.v_c = f*3
        else:
            self.v_c = f/2 + 2
        self.debug(self._d,'GetVerts()', 'v_c', self.v_c)

        return self.v_c * self.count
#        #v = self.count * self.v_c[int(self.subdivisions)-1]
#        return self.v_c * self.count *
#        return v + (v * 5 * self.bev_segments)

    def GetObject(self, complexity):
    #bpy.ops.mesh.primitive_cube_add(
    #       radius=1,
    #       calc_uvs=False,
    #       view_align=False,
    #       enter_editmode=False,
    #       location=(0, 0, 0),
    #       rotation=(0, 0, 0),
    #       layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #global attr
        #self.attr = __distribute(complexity,self.attr)
        self.attr = {
            'subdivisions' : self.subdivisions,
            'radius': self.size,
            'calc_uvs': self.calc_uvs
            }
        self.bpy.ops.mesh.primitive_ico_sphere_add(**self.attr)

        self.bpy.ops.object.shade_smooth()

        ob = self.bpy.context.selected_objects[0]
        print(ob.name_full)
#        for f in ob.data.polygons:
#            f.use_smooth = True

        if self.bev_segments:
            bev = ob.modifiers.new('Bevel', type = 'BEVEL')
            bev.width = 0.01
            bev.segments = self.bev_segments

        self.debug(self._d,'GetObject()', 'Built ICO Sphere.py', 'COMPLETE')
        return ob
