from threading import Thread

from _packet import _Packet



class Guidance( Thread ):

    def __init__( self, config ):

        super().__init__( self, daemon=True )

        self.packet = None
        self.header = config['header']
        self.cf     = config['scf'].cf

        self.AllGreen = True

        self._on_link( config['port'], config['baud'] )

        self.algorithm = config['algorithm']

    
    def _on_link( self, port, baud ):

        self.packet = _Packet( port, baud, timeout=1 )


    ## command Rx


    def run( self ):

        acc_cmd = self.cf.command