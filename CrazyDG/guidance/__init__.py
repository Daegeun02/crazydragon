from ..crazy import CrazyDragon

from threading import Thread

from ..packet import Packet

from .._base import CommunicationBase

from . import utils

from numpy import zeros
from numpy import frombuffer, float32

from time import sleep



class Guidance( Thread, CommunicationBase ):

    def __init__( self, cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.cf = cf

        self.guidance = True

        self.packet = None
        self.config = config


    def TxConnect( self, packet: Packet ):

        config = self.config

        try: 
            packet._TxConfigure( config['Txbfsize'], config['Txheader'] )
        except:
            print( "\033[KTxConfigure need 'Txbfsize' and 'Txheader'" )
            raise KeyError

        self.Packet    = packet
        self.connected = True


    def RxConnect( self, packet: Packet ):

        config = self.config

        try:
            packet._RxConfigure( config['Rxbfsize'], config['Txheader'] )
        except:
            print( "\033[KRxConfigure need 'Rxbfsize' and 'Rxheader'" )
            raise KeyError

        self.Packet    = packet
        self.connected = True

    
    def Transmit( self ):

        if ( self.Packet != None ):
            _cf    = self.cf
            packet = self.Packet

            packet.TxData[:] = _cf.command

            packet._Transmit()

        else:
            print( "something is weird" )


    def Parser( self, data, args ):

        Data = frombuffer( data, dtype=float32 )

        _check = Data[9]

        for byte in Data[0:9]:
            _check -= byte

        if ( abs( _check ) < 1e-2 ):

            args[0][:] = Data[0:3]
            args[1][:] = Data[3:6]
            args[2][:] = Data[6:9]
        else:
            print( "checksum error" )

        self.Transmit()


    def run( self ):

        cf = self.cf
        packet = self.Packet

        Receiver = Thread( target=packet.start_receive, args=[self.Parser, cf.pos, cf.vel, cf.att] )
        Receiver.start()

        while self.guidance:

            sleep( 0.01 )

        packet.join()