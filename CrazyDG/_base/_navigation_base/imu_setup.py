from ...crazy import CrazyDragon

from time import sleep

from cflib.crazyflie.log        import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger



orientation_std_dev = 8.0e-3
SEND_FULL_POSE      = True


def preflight_sequence( _cf: CrazyDragon ):
    """
    This is the preflight sequence. It calls all other subroutines before takeoff.
    """

    adjust_orientation_sensitivity( _cf )

    activate_kalman_estimator( _cf )

   # enable high level commander
    _cf.param.set_value('commander.enHighLevel', '1')

    # prepare for motor shut-off
    _cf.param.set_value('motorPowerSet.enable', '0')
    _cf.param.set_value('motorPowerSet.m1', '0')
    _cf.param.set_value('motorPowerSet.m2', '0')
    _cf.param.set_value('motorPowerSet.m3', '0')
    _cf.param.set_value('motorPowerSet.m4', '0')

    print( 'upload' )

    # ensure params are downloaded
    _wait_for_param_download( _cf )

    print( 'upload done' )

    # reset the estimator
    _reset_estimator( _cf )

    print( 'reset_done' )

    # check state
    _check_state( _cf )

    print( 'sensors is on all green' )


def _wait_for_param_download( _cf: CrazyDragon ):

    while not _cf.param.is_updated: 
        
        print( 'waiting' )

        sleep(1.0)
 

def adjust_orientation_sensitivity( cf: CrazyDragon ):
    cf.param.set_value('locSrv.extQuatStdDev', orientation_std_dev)


def activate_kalman_estimator( cf: CrazyDragon ):
    cf.param.set_value('stabilizer.estimator', '2')

    # Set the std deviation for the quaternion data pushed into the
    # kalman filter. The default value seems to be a bit too low.
    cf.param.set_value('locSrv.extQuatStdDev', 0.06)


def _reset_estimator( cf: CrazyDragon ):

    cf.param.set_value('kalman.resetEstimation', '1')

    sleep(0.1)

    cf.param.set_value('kalman.resetEstimation', '0')

    # time.sleep(1)
    wait_for_position_estimator( cf )


def wait_for_position_estimator( cf: CrazyDragon ):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=10)
    log_config.add_variable('kalman.varPX', 'FP16')
    log_config.add_variable('kalman.varPY', 'FP16')
    log_config.add_variable('kalman.varPZ', 'FP16')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger( cf, log_config ) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append( data['kalman.varPX'] )
            var_x_history.pop( 0 )
            var_y_history.append( data['kalman.varPY'] )
            var_y_history.pop( 0 )
            var_z_history.append( data['kalman.varPZ'] )
            var_z_history.pop( 0 )

            min_x = min( var_x_history )
            max_x = max( var_x_history )
            min_y = min( var_y_history )
            max_y = max( var_y_history )
            min_z = min( var_z_history )
            max_z = max( var_z_history )

            if ( max_x - min_x ) < threshold and (
                    max_y - min_y ) < threshold and (
                    max_z - min_z ) < threshold:
                break


def _check_state( _cf: CrazyDragon ):

    log_config = LogConfig(name='State', period_in_ms=500)
    log_config.add_variable('stabilizer.roll', 'float')
    log_config.add_variable('stabilizer.pitch', 'float')
    log_config.add_variable('stabilizer.yaw', 'float')

    with SyncLogger( _cf, log_config ) as sync_logger:

        for log_entry in sync_logger:

            log_data = log_entry[1]
            roll     = log_data['stabilizer.roll']
            pitch    = log_data['stabilizer.pitch']
            yaw      = log_data['stabilizer.yaw']

            #('yaw', yaw)
            if SEND_FULL_POSE:
                euler_checks = [('roll', roll, 5), ('pitch', pitch, 5)]
            else:
                euler_checks = [('roll', roll, 5), ('pitch', pitch, 5), ('yaw', yaw, 5)]

            for name, val, val_max in euler_checks:
                if abs(val) > val_max:
                    msg = "too much {:s}, {:10.4f} deg, for {:s}".format(
                        name, val, _cf.link_uri)
                    print(msg)
            return