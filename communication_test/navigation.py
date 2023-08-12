from threading import Thread

from ..crazy import CrazyDragon

from .._packet import _Packet

from time import sleep



class Navigation_TEST( Thread ):

    def __init__( self, _cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.packet = None
        self.header = config['header']
        self.Hz     = config['Hz']
        self.cf     = _cf

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )


    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=0.02 )

    def run( self ):

        pos = self.cf.pos
        vel = self.cf.vel
        acc = self.cf.acc
        att = self.cf.att

        dt = 1 / self.Hz

        if self.packet is not None:

            packet = self.packet

            packet._enroll( 12, self.header )

        txData = packet.TxData

        while self.AllGreen:

            txData[0:3] = pos
            txData[3:6] = vel
            txData[6:9] = acc
            txData[9: ] = att

            packet._sendto()

            sleep( dt )