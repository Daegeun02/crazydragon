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

        except:
            print( "without serial communication" )

            self.packet = None

        self.connected = False


    def connect( self, header: ndarray, bytes: int ):

        self.packet._enroll( bytes, header )

        self.connected = True

    
    def isconnected( self ):

        return self.connected

    
    def transmit( self, _cf: CrazyDragon ) -> ndarray:

        print( "\033[KTransmit function is not defined" )
        print( "\033[KYou said that need serial communication" )
        print( "\033[KYou don't make Transmit functon and overload it" )

        print( "\033[Kfunction should be like" )
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

        ## setup imu sensor
        preflight_sequence( cf )

        sleep( 1 )

        ## start imu sensor
        imu.start_get_acc()
        imu.start_get_vel()

        ## get ready qtm it will automatically send data 
        for bodyname, _ in qtm._cfs.items():
            ## this is parser
            qtm.on_pose[bodyname] = lambda pose: __class__._on_pose( cf, pose )

        ## _Packet or None type
        packet = self.packet

        ##transmit function
        if self.connected:
            transmit = self.transmit
            transmit( cf )

        while self.navigate:

            if self.connected:

                packet.TxData[:] = transmit( cf )

                packet._sendto()

            sleep( 0.01 )


    def join( self ):

        self.navigate = False

        super().join()