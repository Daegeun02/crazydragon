from numpy import array, zeros
from numpy import frombuffer
from numpy import float32, uint8



header = array( [4, 26], dtype=uint8 ).tobytes()
data   = array( [1,2,3], dtype=float32 )
buff   = ''
RxData = zeros( 3 )
RxBuff = zeros( 3*4 )

byte = header + data.tobytes()

print( byte )

size = 2 + 12

hdrf = 0
idxn = 0

for i in range( size ):
    _byt = byte[i]

    if ( hdrf == 2 ):
        if ( idxn < size ):
            RxBuff[idxn] = _byt
            idxn += 1

            if ( idxn == size - 2 ):
                hdrf = 0
                idxn = 0

                buff      = RxBuff.astype( uint8 ).tobytes()
                RxData[:] = frombuffer( buff, dtype=float32 )
        
    elif ( hdrf == 0 ):
        if ( _byt == header[0]):
            hdrf = 1
            print( 'pass' )
    
    elif ( hdrf == 1 ):
        if ( _byt == header[1] ):
            hdrf = 2
            print( 'pass' )

print( RxData )