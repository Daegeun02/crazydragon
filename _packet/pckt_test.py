from numpy import array
from numpy import float32, uint8
from numpy import frombuffer
from numpy import ndarray



_arr = array( [ 24, 256, 2 ], dtype=float32 )
_bit = _arr.astype( uint8 ).tobytes()
_byt = _arr.tobytes()

_fir = _byt[0:12]
_Fir = frombuffer( _fir, dtype=float32 )

print( _arr )
print( _bit )
print( _bit[1] )
print( _fir )
print( _Fir )
print( _byt[3] )