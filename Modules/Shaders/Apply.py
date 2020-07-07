import bpy

class ApplyClass():
    def __debug(self, f, n, v):
        if self.debug:
            print('%s %s -- %s -- %s: %s' % (self.inset, self.cname, f, n, v) )

    def __init__(self, _DEBUG = False, _INSET = ''):
        self.inset = _INSET + '-- '
        self.cname = 'APPLY'
        self.debug = _DEBUG

        super(ApplyClass, self).__init__()

    def ApplyMaterial(oef, material):
        for ob in bpy.data.objects:
            if ob.type == 'MESH':
                # parse name
                ob_name_type = ob.name.split('.')[0]

        if oef.GetAttribute('IS_UNIFORM'):
            # get ALLLLLL OEF Objects
        else:
            # UNIQUESSS
