from CrazyDG import CrazyDragon

from threading import Thread

from time import sleep



def interface( _cf: CrazyDragon, thread: Thread, t ):

    while thread.is_alive():
        print( "\033[A\033[K", _cf.pos, _cf.vel, _cf.command, t )

        sleep( 0.01-0.002)

        t += 0.01