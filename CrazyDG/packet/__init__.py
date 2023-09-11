from serial import Serial

from numpy import zeros
from numpy import float32, uint8
from numpy import ndarray
from numpy import frombuffer

_FLOAT=4



class Packet( Serial ):

    def _TxConfigure( self, size: int, header: ndarray ):

        self.TxData   = zeros( size, dtype=float32 )
        self.Txheader = ( header.astype( uint8 ) ).tobytes()

    
    def _RxConfigure( self, size: int, header: ndarray ):

        self.RxData   = zeros( size, dtype=float32 )
        self.RxHeader = ( header.astype( uint8 ) ).tobytes()

        self.RxBfsize = size * _FLOAT

    
    def _Transmit( self ):

        buffer = self.Txheader + self.TxData.tobytes()

        self.write( buffer )

    
    def start_receive( self, parser, *args ):

        RxHeader = self.RxHeader
        size     = self.RxBfsize         ## float

        hdrf = 0

        while True:

            if ( self.readable() ):
                print( 'reading' )
                
                if ( hdrf == 2 ):

                    data = self.read( size )

                    hdrf = 0

                    parser( data, args )

                elif ( hdrf == 0 ):
                    data = frombuffer( self.read(), dtype=uint8 )
                    if ( data == RxHeader[0] ):
                        hdrf = 1

                elif ( hdrf == 1 ):
                    data = frombuffer( self.read(), dtype=uint8 )
                    if ( data == RxHeader[1] ):
                        hdrf = 2

                else:
                    hdrf = 0