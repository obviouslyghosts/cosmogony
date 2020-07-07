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
class P_CubeClass():

    def __init__(self, bpy, r, DEBUG, _d, _FPATH = ''):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'P CUBE']
        self._d = _d

        self.r = r
        self.bpy = bpy
        self.name = 'P_CUBE'
        self.count = 1
        self.vert_count = 8
        self.calc_uvs = self.r.RandomInt([1,1])
        self.radius = self.r.RandomUnif([0.2,2])
        self.attr = {
            'size': self.radius,
            'calc_uvs': self.calc_uvs
            }
        super(P_CubeClass, self).__init__()

    def __vert_count(self):
        v = 8
        #v += v*self.bev_segments*2
        v = 8*2*2
        return self.count * v

    def Name(self):
        return self.name

    def GetVerts(self, complexity, count = 1):
        #Vert count
        self.count = count
        return self.__vert_count()

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
        self.bpy.ops.mesh.primitive_cube_add(**self.attr)
        ob = self.bpy.context.selected_objects[0]

        bev = ob.modifiers.new('Bevel', type = 'BEVEL')
        bev.width = 0.01
        bev.segments = 2
        self.bpy.ops.object.shade_smooth()

        print(ob.name_full)
        self.debug(self._d, 'GetObject()', 'Built Cube.py', 'COMPLETE')
        return ob
