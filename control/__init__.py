from threading import Thread

from controller import Controller

from _packet import _Packet

from numpy import zeros

from time import sleep



class Controller( Thread ):

    def __init__( self, config ):
        
        super().__init__( self, daemon=True )

        self.packet = None
        self.header = config['header']
        self.cf     = config['scf'].cf

        self.ready_for_command = False

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )


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

        _cf = self.cf
        _commander = _cf.commander

        acc_cmd = zeros(3)

        while not self.ready_for_command:
            sleep( 0.1 )

        while self.ready_for_command:

            acc_cmd[:] = _cf.command

            # _send_setpoint_ENU( acc_cmd )