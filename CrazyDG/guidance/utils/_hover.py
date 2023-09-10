from ...crazy import CrazyDragon

from .constants import Kp, Kd, g

from numpy import array, zeros

from time import sleep



def hover( cf: CrazyDragon, T, dt=0.1 ):

    cur     = zeros(3)
    des     = zeros(3)
    acc_cmd = zeros(3)
    P_pos   = zeros(3)
    D_pos   = zeros(3)
    care_g  = array([0,0,g])

    print( 'hover' )

    n = int( T / dt )
    t = 0

    command = cf.command

    cur[:] = cf.pos
    pos    = cf.pos
    vel    = cf.vel

    des[:] = cur[:]

    cf.destination[:] = des

    for _ in range( n ):

        P_pos[:] = des - pos
        D_pos[:] = vel

        acc_cmd[:] = 0
        acc_cmd[:] += P_pos * Kp
        acc_cmd[:] -= D_pos * Kd
        acc_cmd[:] += care_g

        command[:] = acc_cmd

        t += dt

        sleep( dt )