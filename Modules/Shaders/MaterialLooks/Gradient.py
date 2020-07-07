class GradientClass():

    def __debug(self, f, n, v):
        if self.debug:
            print('%s %s -- %s -- %s: %s' % (self.inset, self.cname, f, n, v) )

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'GRADIENT']
        self._d = _d
        self.r = r
        self.bpy = bpy

        self.total_materials_requested = 0
        self.subsurface = self.r.RandomUnif([0,1])
        self.metallic = self.r.RandomUnif([0,1])
        self.anisotropic = self.r.RandomUnif([0,1])
        self.clearcoat = self.r.RandomUnif([0,1])
        self.transmission = self.r.RandomUnif([0,1])

        super(GradientClass, self).__init__()

    def __value_wiggle(self, v):
        n = self.total_materials_requested
        return v + ( ( (1/n) * self.r.RandomUnif([v-1,1-v])) / 2 )


    def GetMaterial(self, name, colors):
        self.total_materials_requested += 1
        #self.__debug('GetMaterial()', 'Writing Material', 'BEGIN')
        mat = self.bpy.data.materials.new(name)
        mat.use_nodes = True
        nt = mat.node_tree

        output = nt.nodes.get('Material Output')
        princ = nt.nodes.new('ShaderNodeBsdfPrincipled')
        #rgbNode = nt.nodes.new('ShaderNodeRGB')
        grdNode = nt.nodes.new('ShaderNodeValToRGB')
        texCoord = nt.nodes.new('ShaderNodeTexCoord')
        texGrad = nt.nodes.new('ShaderNodeTexGradient')

        nt.links.new(texCoord.outputs['Generated'], texGrad.inputs['Vector'] )
        nt.links.new(texGrad.outputs['Color'], grdNode.inputs['Fac'])

        nt.links.new(grdNode.outputs['Color'], princ.inputs['Base Color'])
        nt.links.new(princ.outputs['BSDF'], output.inputs['Surface'])

        n = len(grdNode.color_ramp.elements)
        #n = ( 1 / n ) / n
        #n *= 0.5

        for c,i in zip(grdNode.color_ramp.elements, range(n)):
            c.color = colors.GetRGB()
            a = (1/n)*(i)
            b = (1/n)*(i+1)
            c.position = self.r.RandomUnif([a,b])

        princ.inputs["Metallic"].default_value = self.__value_wiggle(self.metallic)
        princ.inputs["Anisotropic"].default_value = self.__value_wiggle(self.anisotropic)
        princ.inputs["Clearcoat"].default_value = self.__value_wiggle(self.clearcoat)
        princ.inputs["Transmission"].default_value = self.__value_wiggle(self.transmission)
        return mat
