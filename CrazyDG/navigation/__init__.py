from threading import Thread

from ..crazy import CrazyDragon

from .imu       import IMU
from .qualisys  import Qualisys

from .._packet import _Packet

from time import sleep



class Navigation( Thread ):

    def __init__( self, _cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.packet = None
        self.header = config['header']
        self.cf     = _cf

        self.imu = IMU( config['scf'] )
        self.qtm = Qualisys( config['body_name'] )

        self.navigate = True

        self._on_link( config['port'], config['baud'] )


    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]
        cf.att[:] = data[3:6]

        cf.extpos.send_extpos( data[0], data[1], data[2] )

    
    def run( self ):

        cf = self.cf

        pos = self.cf.pos
        vel = self.cf.vel
        acc = self.cf.acc
        att = self.cf.att

        self.imu.start_get_vel()
        self.imu.start_get_acc()

        self.qtm.on_pose = lambda data: __class__._on_pose( cf, data )

        if self.packet is not None:

            packet = self.packet

            packet._enroll( 12, self.header )

        while self.navigate:

            packet.TxData[0:3] = pos
            packet.TxData[3:6] = vel
            packet.TxData[6:9] = acc
            packet.TxData[9: ] = att

            packet._sendto()

            sleep( 0.01 )

    
    def join( self ):

        self.navigate = False

        super().join()