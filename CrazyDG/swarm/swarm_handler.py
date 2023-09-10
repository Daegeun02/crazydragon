from ..crazy import CrazyDragon

from threading import Thread

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from time import sleep



class SwarmHandler:

    @staticmethod
    def OPENLINK( _uris: dict ):

        _cfs = {}

        _scfs = {}

        for _uri, bodyname in _uris.items():
            
            print( "<<< ", _uri, " >>>" )

            _cf  = CrazyDragon()
            _scf = SyncCrazyflie( _uri, cf=_cf )
        
            _cfs[bodyname]  = _cf
            _scfs[bodyname] = _scf

            _scf.open_link()

            sleep( 2 )

        return _cfs, _scfs

    
    @staticmethod
    def CLOSELINK( _scfs: dict ):

        for _, _scf in _scfs.items():
            _scf.close_link()


    def parallel_run( self, func, _cfs: dict, args_list: list=None, args_dict: dict=None ):

        threads = []

        for bodyname, _cf in _cfs.items():

            args = [ _cf ]

            if ( args_list != None ):
                args += args_list

            if ( args_dict != None ):
                args += args_dict[bodyname]

            thread = Thread( target=func, args=args )
            threads.append( thread )
            thread.start()

        for thread in threads:
            
            thread.join()