from numpy import array

## gravity
g     = 9.81

## PD loop
w = array( [1.000, 1.000, 1.000] )
j = array( [0.800, 0.800, 0.800] )

Kp = w * w
Kd = 2 * j * w