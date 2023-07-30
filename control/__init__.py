from threading import Thread

from .integral_loop import _dot_thrust
from .integral_loop import _thrust_clip

from .optimus_prime import _command_as_RPY
from .optimus_prime import _command_is_not_in_there

from constants import alpha

from _packet import _Packet

from numpy import zeros, array

from time import sleep

_FLOAT=4



class Controller( Thread ):

    def __init__( self, config ):
        
        super().__init__( self, daemon=True )

        self.packet = None
        self.header = config['header']
        self.cf     = config['scf'].cf
        self.dt     = config['dt']
        self.n      = config['Hz']

        self.ready_for_command = False

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )

        packet = self.packet

        packet._enroll_receiver( 3*_FLOAT, self.header )

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
        commander.send_stop_setpoint()


    def run( self ):

        packet = self.packet

        cf = self.cf
        commander = cf.commander
        n  = self.n
        dt = self.dt / n

        att_cur = cf.att
        acc_cur = cf.acc

        acc_cmd = zeros(3)
        command = zeros(4)
        thrust  = array( [alpha * 9.81], dtype=int )

        while not self.ready_for_command:
            sleep( 0.1 )

        while self.ready_for_command:

            acc_cmd[:] = packet.RxData

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
                    command[3]
                )

                sleep( dt )