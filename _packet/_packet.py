from serial import Serial

from numpy import zeros
from numpy import frombuffer
from numpy import float32, uint8
from numpy import ndarray



class _Packet( Serial ):

    def _enroll( self, size: int, header: ndarray ):

        self.TxData = zeros( size, dtype=float32 )
        self.header = ( header.astype( uint8 ) ).tobytes()

    
    def _enroll_receiver( self, size: int, header: ndarray ):

        self.RxData   = zeros( size, dtype=float32 )
        self.RxHeader = ( header.astype( uint8 ) ).tobytes()
        self.RxBfsize = size

        self.parser   = None


    def _sendto( self ):

        buffer = self.header + self.TxData.tobytes()

        self.write( buffer )

    
    def _recvfrom( self ):

        RxData   = self.RxData
        RxHeader = self.RxHeader
        size     = self.RxBfsize * 4        ## float

        hdrf = 0
        idxn = 0

        data = None
        buff = None

        while True:

            if self.readable():
                data = self.read()

                if ( hdrf == 2 ):
                    if ( idxn < size ):
                        buff[idxn] = data
                        idxn += 1

                        if ( idxn == size ):
                            hdrf = 0
                            idxn = 0

                            RxData[:] = frombuffer( buff, dtype=float32 )

                elif ( hdrf == 0 ):
                    if ( data == RxHeader[0] ):
                        hdrf = 1

                elif ( hdrf == 1 ):
                    if ( data == RxHeader[1] ):
                        hdrf = 2
                    
                else:
                    hdrf = 0