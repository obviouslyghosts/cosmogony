
from Modules.Cameras.Lenses.Perspective import PerspectiveClass as PERSP
from Modules.Cameras.Lenses.Orthographic import OrthographicClass as ORTHO

class CameraManagerClass():

    def __init__(self, bpy, r, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'CAM']
        self._d = _d
        self.bpy = bpy
        self.r = r
        self.lighting_grid_size = self.r.RandomUnif([9,15])

        self.lenses = {
            'PERSP': PERSP(r, self.lighting_grid_size, DEBUG, _d),
            'ORTHO': ORTHO(r, self.lighting_grid_size, DEBUG, _d)
            }
        super(CameraManagerClass, self).__init__()

    def __deselect_all(self):
        if len(self.bpy.context.selected_objects) > 0:
            bpy.ops.object.select_all()             # delect all

    def __domeverts(self):
        attr = {
            'subdivisions' : 3,
            'radius': self.lighting_grid_size
            }
        self.bpy.ops.mesh.primitive_ico_sphere_add(**attr)
        dome = self.bpy.context.selected_objects[0]
        dome.name = 'delete'
        v = list(i.co.to_tuple() for i in dome.data.vertices)
        for ob in self.bpy.data.objects:
            if ob.name == 'delete':
                ob.select_set(state=True)
            else:
                ob.select_set(state=False)
        self.bpy.ops.object.delete()
        return v

    def AddCam(self, complexity, k=''):
        if self.lenses.get(k):
            lens = self.lenses[k]
        else:
            lens = self.r.ChoiceDict(self.lenses)

        self.__deselect_all()
        self.bpy.ops.object.empty_add(type='PLAIN_AXES')
        e = self.bpy.context.selected_objects[0]
        e.name = 'camera_target'
        cam_list = []
        for o in self.bpy.data.objects:
            o.select_set(state=False)
            if o.type == 'CAMERA':
                cam_list.append(o)
        self.debug(self._d, 'AddCam()', 'CameraCount', str(len(cam_list)))
        if len(cam_list) >= 1:
            camera = cam_list.pop()
            for c in cam_list:
                c.select_set(state=True)
            self.bpy.ops.object.delete()
        else:
            self.bpy.ops.object.camera_add()
            camera = self.bpy.context.scene.objects[0]
        self.debug(self._d, 'PositionCamera()', 'Camera', camera.name)
        v = self.__domeverts()
        camera.location = v.pop(self.r.RandomInt([0,len(v)-1]))
        self.__deselect_all()
        camera.select_set(state=True)
        track_constraint = camera.constraints.new(type='TRACK_TO')
        track_constraint.target = e
        track_constraint.up_axis = 'UP_Y'
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'

        cam = self.bpy.data.cameras.get(camera.data.name)
        cam.lens = lens.GetAttribute('LENS')
        cam.ortho_scale = lens.GetAttribute('ORTHO_SCALE')
        cam.sensor_width = lens.GetAttribute('SENSOR')
        cam.dof.focus_object = e
        cam.dof.aperture_fstop = lens.GetAttribute('APERTURE')
        cam.dof.use_dof = True
        #cam.dof_distance = lens.GetAttribute('DOF_DISTANCE')
        cam.show_passepartout = True
        cam.passepartout_alpha = 0.9
        cam.clip_end = 10000
