class PerspectiveClass():

    def __init__(self, r, grid_size, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'PERSP']
        self._d = _d

        self.r = r
        self.attr = {
                'TYPE': 'PERSP',
                'LENS': self.r.RandomUnif([15,60]),
                'ORTHO_SCALE' : self.r.RandomUnif([1,10]),
                'SENSOR': self.r.RandomUnif([20,60]),
                'DOF_DISTANCE' : self.r.RandomUnif([(grid_size/2)-1, grid_size]),
                'APERTURE': self.r.RandomUnif([1.2,3])
            }

        super(PerspectiveClass,self).__init__()

    def __is_valid_key(self, d, k):
        if type(d.get(k)) != type(None):
            return True
        else:
            return False

    def GetAttribute(self, a):
        if self.__is_valid_key(self.attr, a):    #Make sure it's there
            return self.attr[a]
        else: return ''
