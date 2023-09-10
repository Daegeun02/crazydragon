from ..crazy import CrazyDragon

from threading import Thread

from .._packet import _Packet

from .._base._navigation_base.imu       import IMU
from .._base._navigation_base.imu_setup import preflight_sequence
from .._base._navigation_base.qualisys  import Qualisys

from time import sleep

from numpy import ndarray



class Navigation( Thread ):

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

            self.connected = False

        except:
            print( "without serial communication" )

            self.connected = True

            self.packet = None


    def connect( self, header: ndarray, bytes: int ):

        self.packet._enroll( bytes, header )

        self.connected = True

    
    def transmit( self, _cf: CrazyDragon ) -> ndarray:

        print( "\033[KTransmit function is not defined" )
        print( "\033[KYou said that need serial communication" )
        print( "\033[KYou don't make Transmit functon and overload it" )

        print( "\033[Kfuncion should be like" )
        print( "\033[KINPUT : CrazyDragon" )
        print( "\033[KOUTPUT: numpy ndarray with size that you said in Navigation.connect funciont" )


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]
        cf.att[:] = data[3:6]

        cf.extpos.send_extpos( data[0], data[1], data[2] )


    def run( self ):

        cf = self.cf

        imu = self.imu
        qtm = self.qtm

        preflight_sequence( cf )

        sleep( 1 )

        imu.start_get_acc()
        imu.start_get_vel()

        qtm.on_pose = lambda pose: __class__._on_pose( cf, pose )

        packet = self.packet

        transmit = self.transmit

        if not self.connected:
            print( "warning: not connected with serial" ) 

        while self.navigate:

            if ( packet != None ):

                packet.TxData[:] = transmit( cf )

                self.packet._sendto()

            sleep( 0.01 )


    def join( self ):

        self.navigate = False

        super().join()