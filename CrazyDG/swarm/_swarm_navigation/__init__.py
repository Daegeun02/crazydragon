from ...crazy import CrazyDragon

from threading import Thread

from ..swarm_handler import SwarmHandler

from ..._base._navigation_base.imu       import IMU
from ..._base._navigation_base.imu_setup import preflight_sequence
from ..._base._navigation_base.qualisys  import Qualisys

from time import sleep



class SwarmNavigation( Thread, SwarmHandler ):

    def __init__( self, _cfs: dict ):

        super().__init__()

        self.daemon = True

        self._cfs = _cfs

        self.imu = {}

        for bodyname, _cf in _cfs.items():
            self.imu[bodyname] = IMU( _cf )

        self.qtm         = Qualisys( _cfs )
        self.qtm.on_pose = {}

        self.navigate = True
        self.doing    = True


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):

        cf.pos[:] = data[0:3]
        cf.att[:] = data[3:6]

        cf.extpos.send_extpos( data[0], data[1], data[2] )


    def run( self ):

        _cfs = self._cfs

        imu = self.imu
        qtm = self.qtm

        print( 'preflight sequence' )

        self.parallel_run( preflight_sequence, _cfs )

        for bodyname, _imu in imu.items():
            
            _imu.start_get_acc()
            _imu.start_get_vel()

        for bodyname, _cf in _cfs.items():

            qtm.on_pose[bodyname] = lambda pose: __class__._on_pose( _cf, pose )

        print( 'false' )
        
        self.doing = False

        while self.navigate:

            sleep( 0.1 )


    def wait_until_init( self ):

        while self.doing:

            sleep( 0.1 )


    def join(self):

        self.navigate = False

        super().join()