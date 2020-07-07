from Modules.Shaders.Colorway.Palettes.MonoChromatic import MonoChromaticClass as c_MONO
from Modules.Shaders.Colorway.Palettes.ColorStep import ColorStepClass as c_STEP
from Modules.Shaders.Colorway.Palettes.ColorStepDouble import ColorStepDoubleClass as C_STEPDBL
from Modules.Shaders.Colorway.Palettes.Binary import BinaryClass as C_BINARY
# ADD TEMPLATES HERE

class ColorwayManagerClass():

    def __init__(self, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'COLOR']
        self._d = _d
        self.r = r
        self.colorway = {
            'c_MONO': c_MONO(r, self.debug, self._d),
            'C_STEP': c_STEP(r, self.debug, self._d),
            'C_STEPDBL': C_STEPDBL(r, self.debug, self._d),
            'C_BINARY': C_BINARY(r, self.debug, self._d)
            }
        super(ColorwayManagerClass, self).__init__()

    def Get_Color_Palette(self, complexity, k=''): #,seed, scene_complexity, k=''):
        if self.colorway.get(k):
            return self.colorway[k]
        return self.r.ChoiceDict(self.colorway)
