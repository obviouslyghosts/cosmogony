from Modules.Scenes.Layouts.Standard.S_Bubble import BubbleClass as TLBC
from Modules.Scenes.Layouts.Standard.S_Array import ArrayClass as ARRAY
from Modules.Scenes.Layouts.Standard.S_Chaos import ChaosClass as CHAOS
# ADD TEMPLATES HERE VVVVVVVVVVVV



class LayoutManagerClass():

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'LAY MAN']
        self._d = _d
        self.bpy = bpy
        self.r = r


        self.layouts = {
            'Bubbles': TLBC(bpy, r, self.debug, self._d),
            'Array': ARRAY(bpy, r, self.debug, self._d),
            'Chaos' : CHAOS(bpy, r, self.debug, self._d)
            }
        super(LayoutManagerClass, self).__init__()

    def __is_valid_key(self, d, k):
        if type(d.get(k)) != type(None):
            return True
        else:
            return False

    def Get_Layout(self, complexity, k=''): #,seed, scene_complexity, k=''):
        if self.__is_valid_key(self.layouts, k):
            return self.layouts[k]
        return self.r.ChoiceDict(self.layouts)
##        return self.layouts[choice(list(self.layouts.keys()))]
