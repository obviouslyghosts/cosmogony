class FolderStructureClass():

    def Make_Folder( self, os, path ):
        f = os.path.basename( path )
        p = os.path.dirname( path )
        if not os.path.isdir( p ):
            self.Make_Folder( os, p )
        if not os.path.isdir( path ):
            os.mkdir(p ath )
        return path

    def __init__( self, os, project_folder, DEBUG, _d ):
        self.debug = DEBUG
        _d = [ _d[0], _d[1] + ' --', os.path.basename(__file__) ]
        self._d = _d
        dirs = project_folder ## added for blender
        self.debug( self._d, '__init__()', 'dirs', dirs )
        self.f_post_history = self.Make_Folder( os, os.path.join( dirs, 'POSTS' ) )
        self.debug( self._d, '__init__()', 'history', self.f_post_history )
        self.debug( self._d, '__init__()', 'dirs', os.path.join( dirs, 'Scenes', 'Objects', 'Mesh', 'OBJ' ) )
        self.f_obj = self.Make_Folder( os, os.path.join(dirs, 'Modules', 'Scenes', 'Objects', 'Mesh', 'OBJ' ) )
        super( FolderStructureClass, self ).__init__()
