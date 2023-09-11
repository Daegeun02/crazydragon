from ..crazy import CrazyDragon

from threading import Thread

from ..packet import Packet

from .._base import CommunicationBase

from .utils import *

from numpy import frombuffer, float32

from time import sleep



class Guidance( Thread, CommunicationBase ):

    def __init__( self, cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.cf = cf

        self.packet = None
        self.config = config


    def TxConnect( self, packet: Packet ):

        config = self.config

        try: 
            packet._TxConfigure( config['Txbfsize'], config['Txheader'] )
        except:
            print( "\033[KTxConfigure need 'Txbfsize' and 'Txheader'" )
            raise KeyError

        self.packet    = packet
        self.connected = True


    def RxConnect( self, packet: Packet ):

        config = self.config

        try:
            packet._RxConfigure( config['Rxbfsize'], config['Txheader'] )
        except:
            print( "\033[KRxConfigure need 'Rxbfsize' and 'Rxheader'" )
            raise KeyError

        self.packet    = packet
        self.connected = True

    
    def Transmit( self ):

        if ( self.packet != None ):
            _cf    = self.cf
            packet = self.packet

            packet.TxData[:] = _cf.command

            packet._Transmit()

        else:
            print( "something is weird" )


    def Parser( self, data, *args ):

        Data = frombuffer( data, dtype=float32 )

        args[0][:] = Data[0:3]
        args[1][:] = Data[3:6]
        args[2][:] = Data[6:9]
