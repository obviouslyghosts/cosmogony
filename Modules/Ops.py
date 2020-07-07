class OpsClass():

    def __init__(self, bpy, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'OPS']
        self._d = _d
        self.bpy = bpy
        
        self.wd = bpy.context.scene.world
        self.r = bpy.context.scene.render
        self.fpath = ''
        self.fname = ''
        super(OpsClass,self).__init__()


    def ClearScene(self):
        try:
            for i in range(1, len( self.bpy.context.object.material_slots ) ):
                self.bpy.context.object.active_material_index = 1
                self.bpy.ops.object.material_slot_remove()
        except:
            self.debug(self._d, 'ClearScene()', 'Objects to load', 'NONE')


        for ob in self.bpy.data.objects:
            if ob.type == 'CAMERA':
                ob.select_set(state=False)
            else:
                ob.select_set(state=True)
        self.bpy.ops.object.delete()
        self.debug(self._d, 'ClearScene()', 'COMPLETE', 'Deleting Objects')

        for mat in self.bpy.data.materials:
            self.bpy.data.materials.remove(mat)
        self.debug(self._d, 'ClearScene()', 'COMPLETE', 'Deleting Materials')
        self.debug(self._d, 'ClearScene()', 'COMPLETE', 'Scene Clear')

    def SetupRender(self, engine = 'CYCLES', features = 'SUPPORTED', processor = 'CPU', resolution = [1000,1000,100]):
        self.debug(self._d, 'SetupRender()', 'Setting Up', 'BEGIN')
        self.r.engine = engine
        self.bpy.context.scene.cycles.feature_set = features
        self.bpy.context.scene.cycles.device = processor
        if engine == 'CYCLES':
            self.bpy.context.scene.cycles.dicing_rate = 4
            self.wd.light_settings.ao_factor = 0.5
            self.wd.light_settings.use_ambient_occlusion = True
            self.bpy.context.scene.use_denoising = True
        if engine == 'BLENDER_EEVEE':
            # Ambient Occlusion
#            self.ev.use_gtao = True
#            self.ev.gtao_distance = 10
#            self.ev.gtao_factor = 0.8
            self.bpy.context.scene.eevee.use_gtao = True
            self.bpy.context.scene.eevee.gtao_distance = 10
            self.bpy.context.scene.eevee.gtao_factor = 0.8
            # Subsurface Scattering
            #self.bpy.context.scene.eevee.use_sss = True
            # Screen Space Reflections
            self.bpy.context.scene.eevee.use_ssr = True
#            bpy.context.scene.eevee.use_ssr_refraction = True
            self.bpy.context.scene.eevee.taa_render_samples = 128
        self.r.resolution_x = resolution[0]
        self.r.resolution_y = resolution[1]
        self.r.resolution_percentage = resolution[2]

        self.debug(self._d, 'SetupRender()', 'Engine', self.r.engine)
        self.debug(self._d, 'SetupRender()', 'Resolution', str(self.r.resolution_x) + ' : ' + str(self.r.resolution_y) )
        self.debug(self._d, 'SetupRender()', 'Quality', self.r.resolution_percentage)
