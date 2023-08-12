from ..crazy import CrazyDragon

from threading import Thread

from os import system

from datetime import datetime

from numpy import zeros, array

from time  import sleep

from ..control import alpha

from .visualizer import *



class Recorder( Thread ):


    def __init__(self, cf: CrazyDragon, commander, n=10000):
        ## for threading
        super().__init__()

        self.record_length = 0
        self.recording     = True

        self.guidance_start_idx = -1
        self.guidance_end_idx   = -1

        self.cf = cf

        ## callback functions
        self.record_callback = {
            'acccmd': array_type_data_callback,
            'vel'   : array_type_data_callback,
            'pos'   : array_type_data_callback,
            'posref': array_type_data_callback,
            'att'   : array_type_data_callback,
            'cmd'   : array_type_data_callback,
            'thrust': float_type_data_callback
        }
        ## data storage
        self.record_datastrg = {
            'acc'   : zeros((3,n)),
            'acccmd': zeros((3,n)),
            'vel'   : zeros((3,n)),
            'pos'   : zeros((3,n)),
            'posref': zeros((3,n)),
            'att'   : zeros((3,n)),
            'cmd'   : zeros((4,n)),
            'thrust': zeros((1,n))
        }
        ## realtime data
        self.realtime_data = {
            'acc'   : cf.acc,
            'acccmd': cf.command,
            'vel'   : cf.vel,
            'pos'   : cf.pos,
            'posref': cf.destination,
            'att'   : cf.att,
            'cmd'   : commander.command,
            'thrust': commander.thrust
        }

    
    def run(self):

        sleep(0.1)

        cf = self.cf

        while self.recording:

            self.record_datastrg['acc'][:,self.record_length] = self.realtime_data['acc']

            for key, callback in self.record_callback.items():

                datastrg = self.record_datastrg[key]
                data     = self.realtime_data[key]

                callback( datastrg, data, self.record_length )

            self.record_length += 1

            sleep(0.05)

    
    def stop_record(self):

        self.recording = False

    
    def guidance_start(self):

        self.guidance_start_idx = self.record_length


    def guidance_end(self):

        self.guidance_end_idx = self.record_length

    
    def join(self):

        self.recording = False

        super().join()

        _len = self.record_length
        _stt = self.guidance_start_idx
        _end = self.guidance_end_idx

        acc    = self.record_datastrg['acc']
        acccmd = self.record_datastrg['acccmd']

        vel    = self.record_datastrg['vel']

        pos    = self.record_datastrg['pos']
        posref = self.record_datastrg['posref']

        att    = self.record_datastrg['att']
        cmd    = self.record_datastrg['cmd']
        thrust = self.record_datastrg['thrust']

        d = datetime.now()
        date      = f'{d.year}-{d.month}-{d.day:02}-{d.hour:02}-{d.minute:02}-{d.second:02}'
        self.date = date

        system( f'cd ./flight_data && mkdir {date}' )

        plot_acc_pos_cmd( acc, acccmd, vel, pos, posref, _len, _stt, _end, date )
        plot_thrust( thrust[0,:], cmd[3,:]*alpha, _len, _stt, _end, date )
        plot_att( att, cmd[:3,:], _len, _stt, _end, date )

        plot_trj( pos, _len, _stt, _end, date )


def array_type_data_callback( datastrg, data, i ):

    datastrg[:,i] = array( data )


def float_type_data_callback( datastrg, data, i ):

    datastrg[0,i] = data