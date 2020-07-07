from random import uniform,randint,gauss,seed,choice

class SeededRandomClass():

    def __init__(self, sd):
        seed(sd)
        super(SeededRandomClass, self).__init__()

    def RandomInt(self, v):
        return randint(v[0],v[1])

    def RandomUnif(self, v):
        return uniform(v[0],v[1])

    def ChoiceDict(self, v):
        return v[choice(list(v.keys()))]
