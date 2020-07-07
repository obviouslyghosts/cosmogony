#bpy.ops.mesh.primitive_uv_sphere_add(
#       segments=32,
#       ring_count=16,
#       size=1,
#       calc_uvs=False,
#       view_align=False,
#       enter_editmode=False,
#       location=(0, 0, 0),
#       rotation=(0, 0, 0),
#       layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

# ------------------
class P_SphereUVClass():

    def __init__(self, bpy, r, DEBUG, _d, _FPATH = ''):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'P UV']
        self._d = _d

        self.r = r
        self.bpy = bpy
        self.name = 'P_SPHERE_ICO'
        self.count = 1
        self.vert_count = 8

        self.segments = 3
        self.ring_count = 3
        self.bevel = 0
        self.calc_uvs = 1
        self.size = 1 #self.r.RandomUnif([0.5,1.5])

        super(P_SphereUVClass, self).__init__()

    def Name(self):
        return self.name

    def GetVerts(self, complexity, count = 1):
        self.segments = self.r.RandomInt([3,32])
        self.ring_count = self.r.RandomInt([3,16])
        self.bevel = self.r.RandomInt([0,1])
        self.size = self.r.RandomUnif([0.5,1.5])
        #Vert count
        self.debug(self._d,'GetVerts()', 'Getting Verts', count)
        self.count = count

        if self.bevel:
            self.vert_count = (self.ring_count-1)*self.segments*4 + 2*self.segments
        else:
            self.vert_count =  2 + self.segments*(self.ring_count-1)
        return self.vert_count * self.count

    def GetObject(self, complexity):

        self.attr = {
            'segments' : self.segments,
            'ring_count': self.ring_count,
            'radius': self.size,
            'calc_uvs': self.calc_uvs
            }
        self.bpy.ops.mesh.primitive_uv_sphere_add(**self.attr)
        self.bpy.ops.object.shade_smooth()

        ob = self.bpy.context.selected_objects[0]
        print(ob.name_full)
#        for f in ob.data.polygons:
#            f.use_smooth = True

        if self.bevel:
            bev = ob.modifiers.new('Bevel', type = 'BEVEL')
            bev.width = 0.01
            bev.segments = self.bevel

        self.debug(self._d,'GetObject()', 'Built ICO Sphere.py', 'COMPLETE')
        return ob
