from threading import Thread

from _packet import _Packet

from .utils import *

from time import sleep



class Guidance( Thread ):

    def __init__( self, config ):

        super().__init__( self, daemon=True )

        self.packet = None
        self.header = config['header']
        self.cf     = config['scf'].cf

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )

        packet = self.packet

        packet._enroll_receiver( 12*4, self.header )

        thread = Thread( target=packet._recvfrom, args=(), daemon=True )

        thread.start()


    def run( self ):

        pos = self.cf.pos
        vel = self.cf.vel
        acc = self.cf.acc
        att = self.cf.rpy

        acc_cmd = self.cf.command

        if self.packet is not None:

            packet = self.packet

            packet._enroll( 3, self.header )

        while self.AllGreen:

            packet.TxData[0:3] = acc_cmd

            packet._sendto()

            pos[:] = packet.RxData[0:3]
            vel[:] = packet.RxData[3:6]
            acc[:] = packet.RxData[6:9]
            att[:] = packet.RxData[9: ]

            sleep( 0.01 )