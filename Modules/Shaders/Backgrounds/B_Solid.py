import bpy

class SolidClass():

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'B_SOLID']
        self._d = _d
        self.r = r
        self.bpy = bpy

        super(SolidClass, self).__init__()

    def SetBackground(self, colors):
        wd = self.bpy.context.scene.world
        self.bpy.data.worlds[wd.name].use_nodes = True
        nt = self.bpy.data.worlds[wd.name].node_tree
        #create new gradient texture node
        for g in nt.nodes:
            if g.type == 'RGB':
                nt.nodes.remove(g)
        rgbNode = nt.nodes.new(type="ShaderNodeRGB")
        rgbNode.outputs[0].default_value = colors.GetRGB()

        #find location of background node and position grad node to the left
        backNode = nt.nodes['Background']
        rgbNode.location.x = backNode.location.x-300
        rgbNode.location.y = backNode.location.y
        #connect color out of Grad Node to color in Background node
        rgbColOut = rgbNode.outputs['Color']
        backColIn = backNode.inputs['Color']
        nt.links.new(rgbColOut, backColIn)
