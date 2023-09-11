## empty


from ._navigation_base import *

from ._controller_base import *



class CommunicationBase:

    def __init__( self ):

        self.connected = False


    def TxConnect( self ):
        raise NotImplementedError

    
    def RxConnect( self ):
        raise NotImplementedError


    def Transmit( self ):
        raise NotImplementedError


    def is_connected( self ): return self.connected