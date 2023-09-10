from ..crazy import CrazyDragon

from threading import Thread

from .._packet import _Packet

from .._base._controller_base.integral_loop import _dot_thrust
from .._base._controller_base.integral_loop import _thrust_clip

from .._base._controller_base.optimus_prime import _command_as_RPY
from .._base._controller_base.optimus_prime import _command_is_not_in_there

from .._base._controller_base.constants import alpha

from numpy import zeros, array
from numpy import ndarray

from time import sleep



class Controller( Thread ):

    def __init__( self, cf: CrazyDragon, config ):
        
        super().__init__()

        self.daemon = True

        self.cf = cf
        self.dt = config['dt']
        self.n  = config['n']

        self.acc_cmd = zeros(3)
        self.command = zeros(4)
        self.thrust  = array( [alpha * 9.81], dtype=int )

        try:
            port = config['port']
            baud = config['baud']

            self.packet = _Packet( port=port, baudrate=baud )

            self.connected = False

        except:
            print( "without serial communication" )

            self.packet = None

    
    def connect( self, header: ndarray, bytes: int ):

        self.packet._enroll_receiver( bytes, header )

        self.connected = True


    def init_send_setpoint( self ):
        ## commander
        commander = self.cf.commander
        ## initialize
        commander.send_setpoint( 0, 0, 0, 0 )
        self.cf.ready_for_command = True


    def stop_send_setpoint( self ):
        ## commander
        commander = self.cf.commander
        ## stop command
        self.cf.command[:] = zeros(3)
        ## stop signal
        self.cf.ready_for_command = False

        for _ in range( 50 ):
            commander.send_setpoint( 0, 0, 0, 10001 )
            sleep( 0.2 )

        commander.send_stop_setpoint()


    def run( self ):

        cf        = self.cf
        commander = cf.commander

        n  = self.n
        dt = self.dt / n

        att_cur = cf.att
        acc_cur = cf.acc

        acc_cmd = self.acc_cmd
        command = self.command
        thrust  = self.thrust

        while not cf.ready_for_command:
            sleep( 0.1 )

        packet = self.packet

        if self.connected:
            Thread( target=packet.start_receive, args=[cf.command], daemon=True )
        else:
            print( "warning: not connected with serial" )

        print( 'controller starts working' )

        while cf.ready_for_command:

            acc_cmd[:] = cf.command

            _command_is_not_in_there( acc_cmd, att_cur )

            _command_as_RPY( acc_cmd, command )

            if ( acc_cmd[2] == 0 ):
                sleep( dt )
                return

            for _ in range( n ):

                thrust[0] += _dot_thrust( command, acc_cur )

                thrust[0] = _thrust_clip( thrust[0] )

                commander.send_setpoint(
                    command[0],
                    command[1],
                    command[2],
                    thrust[0]
                )

                sleep( dt )

        print( 'controller end' )