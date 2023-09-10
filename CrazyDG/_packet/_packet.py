from serial import Serial

from numpy import zeros
from numpy import frombuffer
from numpy import float32, uint8
from numpy import ndarray

_FLOAT=4



class _Packet( Serial ):

    def _enroll( self, size: int, header: ndarray ):

        self.TxData = zeros( size, dtype=float32 )
        self.header = ( header.astype( uint8 ) ).tobytes()

    
    def _enroll_receiver( self, size: int, header: ndarray ):

        self.RxData   = zeros( size, dtype=float32 )
        self.RxHeader = ( header.astype( uint8 ) ).tobytes()
        self.RxBfsize = size * _FLOAT


    def _sendto( self ):

        buffer = self.header + self.TxData.tobytes()

        self.write( buffer )

    
    def start_receive( self, buff, parser=None ):

        RxData   = self.RxData
        RxHeader = self.RxHeader
        size     = self.RxBfsize         ## float

        hdrf = 0

        while True:

            if ( self.readable() ):
                
                if ( hdrf == 2 ):

                    data = self.read( size )

                    RxData[:] = frombuffer( data, dtype=float32 )

                    hdrf = 0

                elif ( hdrf == 0 ):
                    data = self.read()
                    if ( data == RxHeader[0] ):
                        hdrf = 1

                elif ( hdrf == 1 ):
                    data = self.read()
                    if ( data == RxHeader[1] ):
                        hdrf = 2

                else:
                    hdrf = 0
                
            if ( parser != None ):
                parser( buff, RxData )

                    

    
    def _recvfrom( self ):

        RxData   = self.RxData
        RxHeader = self.RxHeader
        size     = self.RxBfsize         ## float

        hdrf = 0

        while True:

            if self.readable():

                if ( hdrf == 2 ):

                    data = self.read( size )

                    RxData[:] = frombuffer( data, dtype=float32 )

                    hdrf = 0

                elif ( hdrf == 0 ):
                    data = self.read()
                    if ( data == RxHeader[0] ):
                        hdrf = 1

                elif ( hdrf == 1 ):
                    data = self.read()
                    if ( data == RxHeader[1] ):
                        hdrf = 2

                else:
                    hdrf = 0