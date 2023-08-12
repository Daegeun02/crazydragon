from threading import Thread

from ..crazy import CrazyDragon

from .integral_loop import _dot_thrust
from .integral_loop import _thrust_clip

from .optimus_prime import _command_as_RPY
from .optimus_prime import _command_is_not_in_there

from .constants import alpha

from .._packet import _Packet

from numpy import zeros, array

from time import sleep

_FLOAT = 4



class Controller( Thread ):

    def __init__( self, _cf: CrazyDragon, config ):
        
        super().__init__( self, daemon=True )

        self.packet = None
        self.header = config['header']
        self.cf     = _cf
        self.dt     = config['dt']
        self.n      = config['Hz']

        self.acc_cmd = zeros(3)
        self.command = zeros(4)
        self.thrust  = array( [alpha * 9.81], dtype=int )

        self.ready_for_command = False

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )

        packet = self.packet

        packet._enroll_receiver( 3, self.header )

        thread = Thread( target=packet._recvfrom, args=(), daemon=True )

        thread.start()



    def init_send_setpoint( self ):
        ## commander
        commander = self.cf.commander
        ## initialize
        commander.send_setpoint( 0, 0, 0, 0 )
        self.ready_for_command = True


    def stop_send_setpoint( self ):
        ## commander
        commander = self.cf.commander
        ## stop command
        self.cf.command[:] = zeros(3)
        ## stop signal
        self.ready_for_command = False

        for _ in range( 50 ):
            commander.send_setpoint( 0, 0, 0, 10001 )
            sleep( 0.05 )

        commander.send_stop_setpoint()


    def run( self ):

        packet = self.packet
        rxData = packet.RxData

        cf        = self.cf
        commander = cf.commander
        n  = self.n
        dt = self.dt / n

        acc_cmd = self.acc_cmd
        command = self.command
        thrust  = self.thrust

        att_cur = cf.att
        acc_cur = cf.acc

        while not self.ready_for_command:
            sleep( 0.1 )

        while self.ready_for_command:

            acc_cmd[:] = rxData

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