from ..crazy import CrazyDragon

from threading import Thread

from .integrator import _RK4
from .integrator import _A_RK4

from numpy import zeros
from numpy import ndarray


from time import sleep



class Dynamic4PILS( Thread ):

    def __init__( self, cf: CrazyDragon, dt ):

        super().__init__()

        self._cf = cf
        self._dt = dt

        self.dxdt = zeros((6,9))

        self._build_dynamic( dt )

        self.propagate = True

    
    def _build_dynamic( self, dt ):

        dxdt = self.dxdt

        dxdt[0,0] = 1
        dxdt[1,1] = 1
        dxdt[2,2] = 1
        dxdt[3,3] = 1
        dxdt[4,4] = 1
        dxdt[5,5] = 1
        dxdt[0,3] = dt
        dxdt[1,4] = dt
        dxdt[2,5] = dt

        dxdt[0,6] = 0.5 * dt * dt
        dxdt[1,7] = 0.5 * dt * dt
        dxdt[2,8] = 0.5 * dt * dt
        dxdt[3,6] = dt
        dxdt[4,7] = dt
        dxdt[5,8] = dt

    
    def deriv_x( cf: CrazyDragon, out: ndarray ):

        if( out.size != 6 ):
            raise ValueError( 'wrong size' )

        def _dxdt( t, x, args ):

            out[0:3] = x[3:6]
            out[3:6] = cf.command

            return out

        return _dxdt


    def run( self ):

        cf   = self._cf
        dt   = self._dt

        pos = cf.pos
        vel = cf.vel

        x    = zeros(6)
        xdot = zeros(6)
        dxdt = self.deriv_x( cf, xdot )

        t = 0

        x[0:3] = pos
        x[3:6] = vel

        while self.propagate:
            _RK4( dxdt, t, x, dt )

            pos[:] = x[0:3]
            vel[:] = x[3:6]            

            t += dt

            sleep( dt )