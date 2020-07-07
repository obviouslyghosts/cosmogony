import os
import inspect
import test

class TestClass():

    def __init__( self ):
        super( DebugClass, self ).__init__()

    def SampleDebug():
        d = test.DebugClass( )
        _d = [ True,'--' ]
        d.debug( _d, self )

