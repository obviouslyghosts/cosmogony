class DebugClass():
    """master print command"""

    def __init__( self ):
        super( DebugClass, self ).__init__()

    def debug( self, s ):
        """file, function, name, value"""
        print( s.os.path.basename(__file__) )
##        if d[0]: print('%s %s : %s : %s : %s: %s' % ( d[1], d[2], l, f, n, v ) )
##        if d[0]: print('%s %s : %s : %s : %s: %s' % (
##            d[1], self.os.path.basename(__file__),
##            self.inspect.currentframe().f_code.co_name,
##            f, n, v ) )
