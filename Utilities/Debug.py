class DebugClass():
    """master print command"""

    def __init__( self   ):
        super( DebugClass, self ).__init__()

    def debug( self, d, l, f, n, v ):
        """file, function, name, value"""
        if d[0]: print('%s %s : %s : %s: %s' % ( d[1], d[2], l, f, n, v ) )
        #if d: print('%s %s : %s -- %s: %s' % (f, n, v) )
