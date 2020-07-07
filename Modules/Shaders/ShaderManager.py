from Modules.Shaders.Colorway.ColorwayManager import ColorwayManagerClass

from Modules.Shaders.MaterialLooks.Plastic import PlasticClass as m_PLASTIC
from Modules.Shaders.MaterialLooks.Gradient import GradientClass as m_GRADIENT

from Modules.Shaders.Backgrounds.B_Solid import SolidClass as b_SOLID
#from Modules.Shaders.Apply import ApplyClass
# ADD TEMPLATES HERE


class ShaderManagerClass():

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'SHADE']
        self._d = _d
        self.r = r
        self.bpy = bpy

        self.color_manager = ColorwayManagerClass(r,self.debug, self._d)
        self.materials = {
            'm_PLASTIC': m_PLASTIC(bpy, r, self.debug, self._d),
            'm_GRADIENT':m_GRADIENT(bpy, r, self.debug, self._d)
            }

        self.backgrounds = {
            'b_solid' : b_SOLID(bpy, r, self.debug, self._d)
        }
        super(ShaderManagerClass, self).__init__()

    def __apply_shader(self, object, shader='', mat=''):
        pass

    def __is_valid_key(self, d, k):
        if type(d.get(k)) != type(None):
            return True
        else:
            return False

    def ApplyShaders(self, complexity, object_list='', MATERIAL=''): #,seed, scene_complexity, k=''):
        self.debug(self._d, 'ApplyShaders()','Applying Shaders','BEGIN')
        colors = self.color_manager.Get_Color_Palette(complexity)
        background = self.r.ChoiceDict(self.backgrounds)
        for o in object_list:
            self.debug(self._d, 'ApplyShaders()','Applying Shaders to', o)
            if object_list[o].GetAttribute('IS_UNIFORM'):
                self.debug(self._d, 'ApplyShaders()','Object is uniform', 'TRUE')
                materials = self.r.ChoiceDict(self.materials)
                mat = materials.GetMaterial(o, colors) #.GetRGB())
                for ob in self.bpy.data.objects:
                    if ob.name.split('.')[0] == o.split('.')[0]:
                        ob.data.materials.append(mat)
            else:
                self.debug(self._d, 'ApplyShaders()','Object is uniform', 'FALSE')
                for ob in self.bpy.data.objects:
                    if ob.name.split('.')[0] == o.split('.')[0]:
                        materials = self.r.ChoiceDict(self.materials)
                        ob.data.materials.append(materials.GetMaterial(o, colors) ) #.GetRGB()))
        background.SetBackground(colors) #.GetRGB())
        return colors.GetRGB(_LIGHT=True)
