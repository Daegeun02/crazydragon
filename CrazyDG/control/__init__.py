from ..crazy import CrazyDragon

from threading import Thread

from ..packet import Packet

from .._base import CommunicationBase

from .._base._controller_base.integral_loop import _dot_thrust
from .._base._controller_base.integral_loop import _thrust_clip

from .._base._controller_base.optimus_prime import _command_as_RPY
from .._base._controller_base.optimus_prime import _command_is_not_in_there

from .._base._controller_base.constants import alpha

from numpy import zeros, array
from numpy import frombuffer, float32

from time import sleep



class Controller( Thread, CommunicationBase ):

    def __init__( self, cf: CrazyDragon, config ):
        
        super().__init__()

        self.daemon = True

        self.cf = cf
        self.dt = config['dt']
        self.n  = config['n']

        self.acc_cmd = zeros(3)
        self.command = zeros(4)
        self.thrust  = array( [alpha * 9.81], dtype=int )

        self.packet = None
        self.config = config


    def RxConnect( self, packet: Packet ):

        config = self.config

        try:
            packet._RxConfigure( config['Rxbfsize'], config['Rxheader'] )
        except:
            print( "\033[KRxConfigure need 'Rxbfsize' and 'Rxheader'" )
            raise KeyError

        self.packet    = packet
        self.connected = True


    def Parser( self, data, args ):

        Data = frombuffer( data, dtype=float32 )

        _check = Data[3]

        for byte in Data[0:3]:
            _check -= byte

        if ( abs( _check ) < 1e-2 ):

            args[0][:] = Data[0:3]
        
        else:
            print( "checksum error" )

    
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

        packet = self.packet

        Receiver = Thread( target=packet.start_receive, args=[self.Parser, cf.command], daemon=True )
        Receiver.start()

        ## wait until start flag on
        while not cf.ready_for_command:
            sleep( 0.1 )

        while cf.ready_for_command:

            # acc_cmd[:] = cf.command
            acc_cmd[2] = 10

            _command_is_not_in_there( acc_cmd, att_cur )

            _command_as_RPY( acc_cmd, command )

            if ( acc_cmd[2] == 0 ):
                sleep( dt )
                # return

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

        packet.join()