from navigation import Navigation

from control import Controller

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie               import Crazyflie
from cflib.utils                   import uri_helper

from numpy import array



nav_config = {
    'header'   : array([ 4,26]).tobytes(),
    'scf'      : None,
    'body_name': 'cf1',
    'port'     : '/dev/ttyUSB0',
    'baud'     : 115200
}

ctr_config = {
    'header': array([26, 4]).tobytes(),
    'scf'   : None,
    'dt'    : 0.1,
    'Hz'    : 5,
    'port'  : '/dev/ttyUSB0',
    'baud'  : 115200
}

uri1 = uri_helper.uri_from_env(default='radio://0/65/2M/E7E7E7E707')


if __name__ == "__main__":

    with SyncCrazyflie( uri1, cf=Crazyflie( rw_cache='./cache' ) ) as scf:

        nav_config['scf'] = scf
        ctr_config['scf'] = scf

        NAV = Navigation( nav_config )
        CTR = Controller( ctr_config )

        NAV.start()
        CTR.start()
