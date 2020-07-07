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
class P_CylinderClass():

    def __init__(self, bpy, r, DEBUG, _d, _FPATH = ''):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'P CYLINDER']
        self._d = _d

        self.r = r
        self.bpy = bpy
        self.name = 'P_CYLINDER'
        self.count = 1
        self.vert_count = 8
        self.vertices = self.r.RandomInt([3,32])
        self.radius = self.r.RandomUnif([0.1,5])
        self.depth = self.r.RandomUnif([0.1,8])
        self.calc_uvs = self.r.RandomInt([1,1])
        if (self.vertices <= 20):
            self.subdivide = True
        else: self.subdivide = False
##        self.attr = {
##            'vertices': self.vertices,
##            'radius': self.radius,
##            'depth': self.depth,
##            'calc_uvs': self.calc_uvs
##            }
        super(P_CylinderClass, self).__init__()

    def __set_volume_to_one(self):
        ob = self.bpy.context.scene.objects[0]
        ##
        vol = ob.dimensions.x * ob.dimensions.y * ob.dimensions.z
        n = (1/vol)**(1/3.0)
        temp_v = list(i*n for i in ob.dimensions)

        ob.dimensions = temp_v
        self.bpy.ops.object.transform_apply(scale=True)

    def __vert_count(self):
        if self.subdivide:
            return self.count * (self.vertices*60 + 2) + (self.vertices*28) # with bevel/subdivide
        else:
            return self.count * self.vertices * 7
        #return self.count * self.vertices * 2 * 3

    def Name(self):
        return self.name

    def GetVerts(self, complexity, count = 1):
        #Vert count
        self.count = count
        return self.__vert_count()

    def GetObject(self, complexity):
    #bpy.ops.mesh.primitive_cylinder_add(
    #       vertices=32,
    #       radius=1,
    #       depth=2,
    #       end_fill_type='NGON',
    #       calc_uvs=False,
    #       view_align=False,
    #       enter_editmode=False,
    #       location=(0, 0, 0),
    #       rotation=(0, 0, 0),
    #       layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        self.attr = {
            'vertices': self.vertices,
            'radius': self.radius,
            'depth': self.depth,
            'calc_uvs': self.calc_uvs
            }
        self.bpy.ops.mesh.primitive_cylinder_add(**self.attr)
        ob = self.bpy.context.selected_objects[0]

        self.bpy.ops.object.shade_smooth()

        bev = ob.modifiers.new('Bevel', type = 'BEVEL')
        bev.width = 0.01
        bev.segments = 2
        if self.subdivide:
            bev.limit_method = 'ANGLE'
            subs = ob.modifiers.new('Subsurf', type = 'SUBSURF')

        print(ob.name_full)

#        for f in ob.data.polygons:
#            f.use_smooth = True

#        if self.bev_segments > 0:
#            bev = ob.modifiers.new('Bevel', type = 'BEVEL')
#            bev.width = 0.01
#            bev.segments = self.bev_segments

        self.debug(self._d, 'GetObject()', 'Built Cylinder.py', 'COMPLETE')
        return ob
