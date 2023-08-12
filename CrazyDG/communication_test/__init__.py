
from .control import Controller_TEST

from .guidance import CommunicationCenter

from .navigation import Navigation_TEST

from time import sleep



def NAV_AND_CTR( _cf, NavConfig, CtrConfig ):

    NAV = Navigation_TEST( _cf, NavConfig )
    CTR = Controller_TEST( _cf, CtrConfig )

    NAV.start()
    CTR.start()

    while ( CTR.AllGreen and NAV.AllGreen ):
        sleep( 0.1 )


def GUIDANCE( _cf, GuiConfig ):

    CMC = CommunicationCenter( _cf, GuiConfig )

    CMC.start()

    while CMC.AllGreen:
        sleep( 0.1 )