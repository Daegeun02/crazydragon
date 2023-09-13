from ..crazy import CrazyDragon

from threading import Thread

import asyncio
from asyncio import create_task

from numpy import zeros
from numpy import ndarray



async def _Timer( dt ):
    await asyncio.sleep( dt )


async def _propagate( dxdt, x, pos, vel, cmd, gra ):

    x[0:3] = pos
    x[3:6] = vel
    x[6:9] = cmd

    x[:] = dxdt @ x + gra

    if ( ( x[2] < 0 ) and ( x[5] < 0 ) ):
        x[2] = 0
        x[5] = 0

    pos[:] = x[0:3]
    vel[:] = x[3:6]


async def Propagation( dxdt, x, pos, vel, cmd, gra, dt ):

    timer = create_task( _Timer( dt ) )
    _task = create_task( _propagate( dxdt, x, pos, vel, cmd, gra ) )

    await timer
    await _task


class Dynamic4PILS( Thread ):

    def __init__( self, cf: CrazyDragon, dt ):

        super().__init__()

        self.daemon = True

        self._cf = cf
        self._dt = dt / 5

        self.dxdt = zeros((9,9))

        self._build_dynamic( self._dt )

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

    
    def run( self ):

        cf   = self._cf
        dt   = self._dt

        pos = cf.pos
        vel = cf.vel
        cmd = cf.command

        x    = zeros(9)
        dxdt = self.dxdt

        gra = zeros(9)
        gra[2] -= 0.5 * 9.81 * dt * dt
        gra[5] -= 9.81 * dt

        t = 0

        while self.propagate:

            asyncio.run( Propagation( dxdt, x, pos, vel, cmd, gra, dt ) )

            t += dt

    
    def join( self ):

        self.propagate = False

        super().join()