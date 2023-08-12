from cflib.crazyflie import Crazyflie

from numpy import zeros, eye



class CrazyDragon( Crazyflie ):

    def __init__( self ):
        super().__init__( rw_cache='./cache' )

        self.pos         = zeros(3)
        self.vel         = zeros(3)
        self.att         = zeros(3)
        self.acc         = zeros(3)
        self.command     = zeros(3)
        self.destination = zeros(3)
        self.rot         = eye(3)
