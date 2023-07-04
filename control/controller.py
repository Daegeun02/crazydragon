from threading import Thread

from time import sleep

from numpy import array, zeros

from .integral_loop import _dot_thrust
from .integral_loop import _thrust_clip

from .optimus_prime import _command_as_RPY
from .optimus_prime import _command_is_not_in_there

from .constants import *



acc_cmd = zeros(3)


class Controller( Thread ):
    
    
    def __init__( self, scf, dt ):

        super().__init__( self, daemon=True )

        ## crazyflie
        self.cf = scf.cf
        ## time step
        self.dt = dt

        self.thrust = array( [alpha * 9.81], dtype=int )
        ## memory that restores thrust command
        self.ready_for_command = False
        ## store commands
        self.command = zeros( 4 )
    

    def run( self ):
        ## initialize
        cf      = self.cf

        print( 'ready for guidance start' )
    
        ## wait until start flag on
        while not self.ready_for_command:
            sleep( 0.1 )

        print( 'guidance is on, start to send command' )

        ## start flag is on
        while self.ready_for_command:
            ## read command
            acc_cmd[:] = cf.command
            ## call control function
            self._send_setpoint_ENU( acc_cmd )

        print( 'mission finished' )

    
    def init_send_setpoint( self ):
        ## commander
        commander = self.cf.commander
        ## initialize
        commander.send_setpoint( 0, 0, 0, 0 )
        self.ready_for_command = True

    
    ## commander should be given in ENU
    def _send_setpoint_ENU( self, acc_cmd, n=5 ):
        ## crazyflie
        cf = self.cf
        ## commander
        commander = cf.commander
        command   = self.command
        thrust    = self.thrust
        ## timestep
        dt = self.dt / n
        ## acceleration current
        euler_cur = cf.euler_pos
        acc_cur   = cf.acc

        ## transform command
        acc_cmd = _command_is_not_in_there( euler_cur, acc_cmd )
        _command_as_RPY( acc_cmd, command )

        if ( acc_cmd[2] == 0 ):
            sleep( dt )
            return 

        for _ in range(n):

            ## closed loop
            thrust[0] += _dot_thrust( command, acc_cur )
            
            ## cliping
            thrust[0] = _thrust_clip( thrust[0] )

            ## input
            commander.send_setpoint(
                command[0],         ## roll
                command[1],         ## pitch
                command[2],         ## yawRate
                thrust[0]           ## thrust
            )

            sleep( dt )


    def stop_send_setpoint( self ):
        ## commander
        commander = self.cf.commander
        ## stop command
        self.cf.command[:] = zeros(3)
        ## stop signal
        self.ready_for_command = False
        commander.send_stop_setpoint()