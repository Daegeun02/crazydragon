import asyncio

from asyncio import create_task

from .._controller_base.constants import Kp, Kd, g



async def _Timer( dt ):
    await asyncio.sleep( dt )


async def _PD_Lp( cmd, _Pc, _Pp, _Dc, _Dp ):

    cmd[:] = 0
    cmd[:] += ( _Pc - _Pp ) * Kp
    cmd[:] += ( _Dc - _Dp ) * Kd
    cmd[2] += g


async def _Loop_Handler( cmd, Pc, Pp, Dc, Dp, dt ):

    timer = create_task( _Timer( dt ) )
    _task = create_task( _PD_Lp( cmd, Pc, Pp, Dc, Dp ) )

    await timer
    await _task
