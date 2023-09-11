from ..crazy import CrazyDragon

from threading import Thread

from .._packet import _Packet

from .._base import CommunicationBase

from .._base._navigation_base.imu       import IMU
from .._base._navigation_base.imu_setup import preflight_sequence
from .._base._navigation_base.qualisys  import Qualisys

from time import sleep

from numpy import ndarray



class Navigation( Thread, CommunicationBase ):

    def __init__( self, cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.cf = cf

        self.imu = IMU( cf )
        self.qtm = Qualisys( config['body_name'] )

        self.navigate = True

        try:
            port = config['port']
            baud = config['baud']

            self.packet = _Packet( port=port, baudrate=baud )

        except:
            print( "without serial communication" )

            self.packet = None

        self.config = config

    
    def TxConnect( self ):

        config = self.config
        packet = self.packet

        try:
            packet._TxConfigure( config['bfsize'], config['header'] )
        except:
            print( "\033[KTxConfigure need 'bfsize' and 'header'" )
            raise KeyError

        self.connected = True


    def Transmit( self ):

        _cf    = self.cf
        packet = self.packet

        packet.TxData[0:3] = _cf.pos
        packet.TxData[3:6] = _cf.vel
        packet.TxData[6:9] = _cf.att

        packet._Transmit()

    
    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]
        cf.att[:] = data[3:6]

        cf.extpos.send_extpos( data[0], data[1], data[2] )


    def run( self ):

        cf = self.cf

        imu = self.imu
        qtm = self.qtm

        config = self.config

        ## setup imu sensor
        preflight_sequence( cf )

        sleep( 1 )

        ## start imu sensor
        imu.start_get_acc()
        imu.start_get_vel()

        ## setup my qtm data
        qtm.on_pose[config['bodyname']] = lambda pose: __class__._on_pose( cf, pose )

        while self.navigate:

            if self.connected:

                self.Transmit()

            sleep( 0.01 )


    def join( self ):

        self.navigate = False

        super().join()