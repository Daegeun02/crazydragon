from CrazyDG import CrazyDragon

import asyncio
from asyncio import create_task

from numpy import array, zeros

## gravity
g     = 9.81

## PD loop
w = array( [1.000, 1.000, 1.000] )
j = array( [0.800, 0.800, 0.800] )

Kp = w * w
Kd = 2 * j * w

async def _Timer( dt ):
    await asyncio.sleep( dt )


async def _PD_Loop( cmd, _Pc, _Pp, _Dc, _Dp ):

    cmd[:] = 0
    cmd[:] += ( _Pc - _Pp ) * Kp
    cmd[:] += ( _Dc - _Dp ) * Kd
    cmd[2] += g


async def _Loop_Handler( cmd, des, pos, vel, dt ):

    timer = create_task( _Timer( dt ) )
    _task = create_task( _PD_Loop( cmd, des[0:3], pos, des[3:6], vel ) )

    await timer
    await _task


def goto( cf: CrazyDragon, destination, T, dt = 0.1 ):

    des = zeros(6)

    print( "goto" )

    n = int( T / dt )

    cmd = cf.command
    pos = cf.pos
    vel = cf.vel

    des[0:3] = destination

    for _ in range( n ):
        asyncio.run( _Loop_Handler( cmd, des, pos, vel, dt ) )
