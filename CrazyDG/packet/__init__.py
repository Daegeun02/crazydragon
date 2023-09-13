import asyncio
from asyncio import create_task

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
        self.receiving = True

    
    def _Transmit( self ):

        TxData = self.TxData

        _check = zeros(1, dtype=float32)

        for byte in TxData:
            _check[0] += byte

        buffer = self.Txheader + TxData.tobytes() + _check.tobytes()
        
        self.write( buffer )

    
    async def Transmit( self, dt ):

        timer = create_task( _Timer( dt ) )
        _task = create_task( _Transmit( self ) )

        await timer
        await _task

    
    def start_receive( self, parser, *args ):

        RxHeader = self.RxHeader
        size     = self.RxBfsize + _FLOAT

        hdrf = 0

        while self.receiving:

            if ( self.readable() ):
                
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


    def join( self ):

        self.receiving = False


async def _Timer( dt ):
    await asyncio.sleep( dt )


async def _Transmit( packet: Packet ):

    TxData = packet.TxData

    _check = zeros( 1, dtype=float32 )

    for byte in TxData:
        _check[0] += byte
    
    buffer = packet.Txheader + TxData.tobytes() + _check.tobytes()

    packet.write( buffer )

