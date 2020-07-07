# COLRWAY
# Random, complimentary, RGB values
#from Utilities.SeededRandom import SeededRandomClass
#from random import uniform, randint

class MonoChromaticClass():
    def __set_rgb(self):
        a = [self.r.RandomUnif([0,1]) for i in range(3)]
        return a.append(1)

    def __value_wiggle(self, v):
        n = self.total_colors_requested
        return v + ( ( (1/n) * self.r.RandomUnif([v-1,1-v])) / 2 )

    def __init__(self, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'MONO']
        self._d = _d

        self.total_colors_requested = 0
        self.r = r
        self.light_threshhold = 0.3
##        self.lastRGB = self.__set_rgb()
        self.lastRGB = [self.r.RandomUnif([0,1]) for i in range(3)]
        self.lastRGB.append(1)
        self.newRGB = self.lastRGB
        super(MonoChromaticClass, self).__init__()

    def __is_light(self, rgb):
        delta = 0
        rgb_ = list(rgb)
        for v in rgb:
            if v <= self.light_threshhold:
                if (self.light_threshhold - v) > delta:
                    delta = self.light_threshhold - v
        if delta > 0:
            for i in range(len(rgb)-1):
                self.debug(self._d, '__is_light()','RGB', rgb)
                self.debug(self._d, '__is_light()','RGB', delta)
                rgb_[i] += delta
        return tuple(rgb_)

    def GetRGB(self, _LIGHT = False):
        self.total_colors_requested += 1

        if self.r.RandomInt([0,15]) == 3:
            # add black
            black_white = (0.05,0.05,0.05,1)
            if(self.r.RandomInt([0,1])):
                # nope white
                black_white = (0.95,0.95,0.95,1)
            if _LIGHT:
                black_white = self.__is_light(black_white)

            return black_white

        else:
            # Ok Color
            self.lastRGB = self.newRGB
            self.debug(self._d, 'GetRGB()','lastRGB', self.lastRGB)

            self.newRGB = [self.__value_wiggle(self.lastRGB[i]) for i in range(3)]
            self.newRGB.append(1)

            if _LIGHT:
                self.newRGB = self.__is_light(self.newRGB)
            self.debug(self._d, 'GetRGB()','newRGB', self.newRGB)

        return self.newRGB
