import asyncio
from asyncio import create_task

from CrazyDG import CrazyDragon

from threading import Thread

from time import sleep


async def print_state( _cf: CrazyDragon, t ):
    print( "\033[A\033[K", _cf.pos, _cf.vel, _cf.command, t )

async def _Timer( dt ):
    await asyncio.sleep( dt )

async def Print( _cf, t, dt ):

    timer = create_task( _Timer( dt ) )
    _task = create_task( print_state( _cf, t ) )

    await timer
    await _task


def interface( _cf: CrazyDragon, thread: Thread, t ):

    dt = 0.01

    while thread.is_alive():

        asyncio.run( Print( _cf, t, dt ) )

        t += dt