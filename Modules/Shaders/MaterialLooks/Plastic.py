# Returns Plastic Materials

# Random, complimentary, RGB values

class PlasticClass():

    def __debug(self, f, n, v):
        if self.debug:
            print('%s %s -- %s -- %s: %s' % (self.inset, self.cname, f, n, v) )

    def __value_wiggle(self, v):
        n = self.total_materials_requested
        return v + ( ( (1/n) * self.r.RandomUnif([v-1,1-v])) / 2 )

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'PLASTIC']
        self._d = _d
        self.r = r
        self.bpy = bpy

        self.total_materials_requested = 0

        self.subsurface = self.r.RandomUnif([0,1])
        self.metallic = self.r.RandomUnif([0,1])
        self.anisotropic = self.r.RandomUnif([0,1])
        self.clearcoat = self.r.RandomUnif([0,1])
        self.transmission = self.r.RandomUnif([0,1])

        super(PlasticClass, self).__init__()

    def GetMaterial(self, name, colors):
        self.total_materials_requested += 1
        #self.__debug('GetMaterial()', 'Writing Material', 'BEGIN')
        mat = self.bpy.data.materials.new(name)
        mat.use_nodes = True
        nt = mat.node_tree

        output = nt.nodes.get('Material Output')
        princ = nt.nodes.new('ShaderNodeBsdfPrincipled')
        rgbNode = nt.nodes.new('ShaderNodeRGB')

        nt.links.new(rgbNode.outputs['Color'], princ.inputs['Base Color'])
        nt.links.new(princ.outputs['BSDF'], output.inputs['Surface'])

        rgbNode.outputs['Color'].default_value = colors.GetRGB()

        princ.inputs["Metallic"].default_value = self.__value_wiggle(self.metallic)
        princ.inputs["Anisotropic"].default_value = self.__value_wiggle(self.anisotropic)
        princ.inputs["Clearcoat"].default_value = self.__value_wiggle(self.clearcoat)
        princ.inputs["Transmission"].default_value = self.__value_wiggle(self.transmission)
        return mat
