from ...crazy import CrazyDragon

from ..._base._utils_base import asyncio
from ..._base._utils_base import _Loop_Handler

from numpy import zeros



def takeoff( cf: CrazyDragon, h=1.5, T=3, dt=0.1 ):

    des = zeros(6)

    print( "<<< takeoff >>>")

    n = int( T / dt )

    cmd = cf.command
    pos = cf.pos
    vel = cf.vel

    des[0] = pos[0]
    des[1] = pos[1]
    des[2] = h

    for _ in range( n ):
        asyncio.run( _Loop_Handler( cmd, des[0:3], pos, des[3:6], vel, dt ) )