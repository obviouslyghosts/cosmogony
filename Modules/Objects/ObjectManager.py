import fnmatch
import os
from Utilities.OEF import OEFClass

from Modules.Scenes.Objects.Primitive.p_cube import P_CubeClass as P_CUBE
from Modules.Scenes.Objects.Primitive.p_sphereico import P_SphereIcoClass as P_SPHERE_ICO
from Modules.Scenes.Objects.Primitive.p_sphereuv import P_SphereUVClass as P_SPHERE_UV
from Modules.Scenes.Objects.Primitive.p_cylinder import P_CylinderClass as P_CYLINDER
from Modules.Scenes.Objects.Mesh.m_OBJ import M_ObjImportClass as M_OBJ


# ADD TEMPLATES HERE


class ObjectManagerClass():

    def __init__(self, bpy, r, f_obj_import, DEBUG, _d):
        self.debug = DEBUG
        _d = [_d[0],_d[1] + ' --', 'OB MAN']
        self._d = _d
        self.f_obj_path = f_obj_import

        self.r = r
        self.bpy = bpy
        self.obj_class = {
            'PRIMITIVE_CUBE' : P_CUBE,
            'PRIMITIVE_SPH_IC': P_SPHERE_ICO,
            'PRIMITIVE_SPH_UV': P_SPHERE_UV,
            'PRIMITIVE_CYLINDER':P_CYLINDER
            }

        c = len(fnmatch.filter(os.listdir(f_obj_import), '*.obj'))
        if c > 0:
            nm = 'OBJ'
            for i in range(c):
                self.obj_class.update({ nm + str(i) : M_OBJ}) #M_ObjImportClass(r, f_obj_import, _DEBUG = self.debug, _INSET = self.inset) }) #M_OBJECTIMPORT })

        self.debug(self._d, '__init__()', 'ObjectList', self.obj_class)
        super(ObjectManagerClass, self).__init__()


    def Get_Objects(self, complexity, object_list):
        total_verts = complexity * 2
        tries = 10;
        while (total_verts > complexity) & (tries > 0):
            self.debug(self._d, 'Get_Objects()', 'Lowering Total Verts...','BEGIN')
            total_verts = 0

            for n in object_list:
                self.debug(self._d, 'Get_Objects()', 'Getting Object', n)
                # Get 1 random object
                o = self.r.ChoiceDict(self.obj_class)
                o = o(self.bpy, self.r, self.debug, self._d, _FPATH = self.f_obj_path)

                # Get Name
                nm = o.Name()
                # Get Scene Count
                sc = int(object_list[n].GetAttribute('SCENE_COUNT'))
                # Get Vert count
                vc = o.GetVerts(complexity, count = sc)
                self.debug(self._d, 'Get_Objects()', 'Count Type', type(vc))
                # Get Link
                lk = o
                # Update OEF
                object_list[n].Update(OBJECT_TYPE = nm, OBJECT_LINK = lk,  MIN_VERTS=vc)

                # Update Total verts
                total_verts += vc # * sc)

            self.debug(self._d,'Get_Objects()', 'Total Vert Count', str(total_verts))
            tries -= 1

        if tries <= 0:
            return {None}

        for n in object_list:
            self.debug(self._d, 'Get_Objects()', 'Building Object', object_list[n].GetAttribute('SCENE_NAME') )
            lk = object_list[n].GetAttribute('OBJECT_LINK').GetObject(complexity)

            object_list[n].Update(OBJECT_LINK = lk)

        return object_list
