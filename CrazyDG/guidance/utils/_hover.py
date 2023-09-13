from ...crazy import CrazyDragon

from ..._base._utils_base import asyncio
from ..._base._utils_base import _Loop_Handler

from numpy import zeros



def hover( cf: CrazyDragon, T, dt=0.1 ):

    des = zeros(6)

    print( "<<< hover >>>" )

    n = int( T / dt )

    cmd = cf.command
    pos = cf.pos
    vel = cf.vel

    des[0:3] = pos

    for _ in range( n ):
        asyncio.run( _Loop_Handler( cmd, des[0:3], pos, des[3:6], vel, dt ) )