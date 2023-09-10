from threading import Thread

from ..swarm_handler import SwarmHandler

from ..._base._controller_base.integral_loop import _dot_thrust
from ..._base._controller_base.integral_loop import _thrust_clip

from ..._base._controller_base.optimus_prime import _command_as_RPY
from ..._base._controller_base.optimus_prime import _command_is_not_in_there

from ..._base._controller_base.constants import alpha

from ...crazy import CrazyDragon

from numpy import zeros, array
from numpy import zeros_like

from time import sleep




class SwarmController( Thread, SwarmHandler ):

    def __init__( self, _cfs: dict, config ):

        super().__init__()

        self.daemon = True

        self._cfs = _cfs

        self.dt = config['dt']
        self.n  = config['n']

        self.acc_cmd = zeros(3)
        self.command = zeros(4)
        self.thrust  = array( [alpha * 9.81], dtype=int )

    
    def init_send_setpoint( self ):

        _cfs = self._cfs

        self.parallel_run( self.__class__._init_send_setpoint, _cfs )

    
    @classmethod
    def _init_send_setpoint( cls, _cf: CrazyDragon ):
        
        commander = _cf.commander

        commander.send_setpoint( 0, 0, 0, 0 )

        _cf.ready_for_command = True


    def stop_send_setpoint( self ):

        _cfs = self._cfs

        self.parallel_run( self.__class__._stop_send_setpoint, _cfs )


    @classmethod
    def _stop_send_setpoint( cls, _cf: CrazyDragon ):

        commander = _cf.commander

        _cf.command[:] = 0

        _cf.ready_for_command = False

        for _ in range( 50 ):

            commander.send_setpoint( 0, 0, 0, 10001 )

            sleep( 0.02 )

        commander.send_stop_setpoint()


    def run( self ):
        
        _cfs = self._cfs

        n  = self.n
        dt = self.dt / n

        args_list = [ n, dt ]
        args_dict = {}

        for bodyname, _ in _cfs.items():
            args_dict[bodyname] = [ 
                zeros_like( self.acc_cmd ),
                zeros_like( self.command ),
                zeros_like( self.thrust )
            ]

        self.parallel_run( self.__class__._run, _cfs, args_list=args_list, args_dict=args_dict )


    @classmethod
    def _run( cls, _cf: CrazyDragon, *args ):

        commander = _cf.commander

        n  = args[0]
        dt = args[1]

        att_cur = _cf.att
        acc_cur = _cf.att

        acc_cmd = args[2]
        command = args[3]
        thrust  = args[4]
        
        while not _cf.ready_for_command:
            sleep( 0.1 )

        while _cf.ready_for_command:

            acc_cmd[:] = _cf.command

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