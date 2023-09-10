from cflib.crazyflie import Crazyflie

from numpy import zeros, eye



class CrazyDragon( Crazyflie ):

    def __init__( self ):
        super().__init__( rw_cache='./cache' )

        self.pos         = zeros(2)
        self.vel         = zeros(2)
        self.att         = zeros(2)
        self.acc         = zeros(2)
        self.command     = zeros(2)
        self.destination = zeros(2)
        self.rot         = eye(2)

        self.ready_for_command = False
