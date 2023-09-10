



def _RK4(dy_dx, x, y, dt, args=None):
    '''
    Runge-Kutta 4th order Method

    y(t+dt) = y(t) + (1/6) * (k1 + 2*k2 + 2*k3 + k4) * dt 

    where 

    k1: f(x(t)           , y(t))
    k2: f(x(t) + (1/2)*dt, y(t) + (1/2)*k1*dt)
    k3: f(x(t) + (1/2)*dt, y(t) + (1/2)*k2*dt)
    k4: f(x(t) + dt      , y(t) + k3*dt)

    f(x, y) = dy/dx
    '''

    k1 = dy_dx( x           , y                , args )
    k2 = dy_dx( x + 0.5 * dt, y + 0.5 * k1 * dt, args )
    k3 = dy_dx( x + 0.5 * dt, y + 0.5 * k2 * dt, args )
    k4 = dy_dx( x + dt      , y + k3 * dt      , args )

    y += ( 1.0 / 6.0 ) * ( k1 + 2 * k2 + 2 * k3 + k4 ) * dt


def _A_RK4(dy_dx, x, y, dt, args=None):
    '''
    Alternative Runge-Kutta 4th order method

    '''

    k1 = dy_dx( x             , y                              , args)
    k2 = dy_dx( x + (1/3) * dt, y + (1/3) * k1 * dt            , args)
    k3 = dy_dx( x + (2/3) * dt, y - (1/3) * k1 * dt + k2 * dt  , args)
    k4 = dy_dx( x + dt        , y + k1 * dt - k2 * dt + k3 * dt, args)

    ny = y + ( 1.0 / 8.0 ) * ( k1 + 3 * k2 + 3 * k3 + k4 )

    return ny