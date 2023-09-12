## empty

from ..packet import Packet


from ._navigation_base import *

from ._controller_base import *

from ._utils_base import *



class CommunicationBase:

    def __init__( self ):

        self.connected = False


    def TxConnect( self, packet: Packet ):
        raise NotImplementedError

    
    def RxConnect( self, packet: Packet ):
        raise NotImplementedError


    def Transmit( self ):
        raise NotImplementedError


    def is_connected( self ): return self.connected