from ...crazy import CrazyDragon

from .smoother import smooth_command

from .constants import Kp, Kd, g

from numpy        import array, zeros
from numpy.linalg import norm

from time import sleep



def landing( cf: CrazyDragon, option=1, h=0.2, T=5, dt=0.1, step=0.075 ):

    cur     = zeros(3)
    des     = zeros(3)
    des_cmd = zeros(3)
    acc_cmd = zeros(3)
    P_pos   = zeros(3)
    D_pos   = zeros(3)
    care_g  = array([0,0,g])

    print( 'landing' )

    n = int( T / dt )
    t = 0

    command = cf.command

    cur[:] = cf.pos
    pos    = cf.pos
    vel    = cf.vel

    if option:
        des[0] = cur[0]
        des[1] = cur[1]
        des[2] = h
    else:
        des[0] = 0
        des[1] = 0
        des[2] = h

    cf.destination[:] = des

    for _ in range( n ):

        des_cmd[:] = smooth_command( 
            des, cur, t, 5.0
        )

        P_pos[:] = des_cmd - pos
        D_pos[:] = vel

        if ( norm( pos - des ) ) < 0.2:
            break

        acc_cmd[:] = 0
        acc_cmd[:] += P_pos * Kp
        acc_cmd[:] -= D_pos * Kd
        acc_cmd[:] += care_g

        command[:] = acc_cmd

        t += dt

        sleep( dt )