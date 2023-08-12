from threading import Thread

from ..crazy import CrazyDragon

from .._packet import _Packet

from time import sleep



class CommunicationCenter( Thread ):

    def __init__( self, _cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.packet = None
        self.Hz     = config['Hz']
        self.cf     = _cf

        self.Rxheader = config['Rxheader']
        self.Txheader = config['Txheader']

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )

        packet = self.packet
        packet._enroll_receiver( 12, self.Rxheader )

        thread = Thread( target=packet._recvfrom, args=(), daemon=True )
        thread.start()


    def run( self ):

        packet = self.packet
        rxData = packet.RxData

        dt = 1 / self.Hz

        if self.packet is not None:

            packet = self.packet
            packet._enroll( 3, self.Txheader )

        txData = packet.TxData

        while self.AllGreen:

            packet._sendto()

            sleep( dt )
