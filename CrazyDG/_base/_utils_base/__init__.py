import asyncio

from asyncio import create_task

from numpy import array



## gravity
g     = 9.81

## PD loop
w = array( [1.000, 1.000, 1.000] )
j = array( [0.800, 0.800, 0.800] )

Kp = w * w
Kd = 2 * j * w


async def _Timer( dt ):
    await asyncio.sleep( dt )


async def _PD_Lp( cmd, _Pc, _Pp, _Dc, _Dp ):

    cmd[:] = 0
    cmd[:] += ( _Pc - _Pp ) * Kp
    cmd[:] += ( _Dc - _Dp ) * Kd
    cmd[2] += g


async def _Loop_Handler( cmd, des, pos, vel, dt ):

    timer = create_task( _Timer( dt ) )
    _task = create_task( _PD_Lp( cmd, des[0:3], pos, des[3:6], vel ) )

    await timer
    await _task
