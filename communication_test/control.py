from threading import Thread

from ..crazy import CrazyDragon

from .._packet import _Packet

from time import sleep



class Controller_TEST( Thread ):

    def __init__( self, _cf: CrazyDragon, config ):
        
        super().__init__()

        self.daemon = True

        self.packet = None
        self.header = config['header']
        self.dt     = config['dt']
        self.n      = config['n']
        self.cf     = _cf

        self.ready_for_command = True

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )

        packet = self.packet
        packet._enroll_receiver( 3, self.header )

        thread = Thread( target=packet._recvfrom, args=(), daemon=True )
        thread.start()

    def run( self ):

        packet = self.packet
        rxData = packet.RxData

        n  = self.n
        dt = self.dt / n

        while self.ready_for_command:

            for _ in range( n ):

                print( rxData )

                sleep( dt )
