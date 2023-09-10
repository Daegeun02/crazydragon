from threading import Thread

from .utils import *

from time import sleep



class Guidance( Thread ):

    def __init__( self, config ):

        super().__init__( self, daemon=True )