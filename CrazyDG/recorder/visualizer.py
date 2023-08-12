import matplotlib.pyplot as plt



def plot_acc_pos_cmd( acc, acccmd, vel, pos, posref, _len, _stt, _end, date ):

    fig = plt.figure( figsize=(14,14) )

    ax1 = fig.add_subplot( 331 )
    ax1.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax1.plot(acc[0,:_len], label='realtime acceleration x')
    ax1.plot(acccmd[0,:_len], label='command input x')
    ax1.legend()
    ax1.grid()

    ax2 = fig.add_subplot( 332 )
    ax2.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax2.plot(acc[1,:_len], label='realtime acceleration y')
    ax2.plot(acccmd[1,:_len], label='command input y')
    ax2.legend()
    ax2.grid()

    ax3 = fig.add_subplot( 333 )
    ax3.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax3.plot(acc[2,:_len], label='realtime acceleration z')
    ax3.plot(acccmd[2,:_len], label='command input z')
    ax3.legend()
    ax3.grid()

    ax4 = fig.add_subplot( 334 )
    ax4.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax4.plot(vel[0,:_len], label='realtime velocity x')
    ax4.legend()
    ax4.grid()

    ax5 = fig.add_subplot( 335 )
    ax5.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax5.plot(vel[1,:_len], label='realtime velocity y')
    ax5.legend()
    ax5.grid()

    ax6 = fig.add_subplot( 336 )
    ax6.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax6.plot(vel[2,:_len], label='realtime velocity z')
    ax6.legend()
    ax6.grid()

    ax7 = fig.add_subplot( 337 )
    ax7.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax7.plot(pos[0,:_len], label='realtime position x')
    ax7.plot(posref[0,:_len], label='destination position x')
    ax7.legend()
    ax7.grid()

    ax8 = fig.add_subplot( 338 )
    ax8.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax8.plot(pos[1,:_len], label='realtime position y')
    ax8.plot(posref[1,:_len], label='destination position y')
    ax8.legend()
    ax8.grid()

    ax9 = fig.add_subplot( 339 )
    ax9.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax9.plot(pos[2,:_len], label='realtime position z')
    ax9.plot(posref[2,:_len], label='destination position z')
    ax9.legend()
    ax9.grid()

    plt.savefig( f'./flight_data/{date}/trg.png' )


def plot_thrust( thrust, thrustcmd, _len, _stt, _end, date ):

    fig = plt.figure( figsize=(8,8) )

    ax = fig.add_subplot()
    ax.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )

    ax.plot(thrust[:_len], label='realtime thrust')
    ax.plot(thrustcmd[:_len], label='reference thrust')
    ax.legend()
    ax.grid()

    plt.savefig( f'./flight_data/{date}/thr.png' )


def plot_att( att, attcmd, _len, _stt, _end, date ):

    fig = plt.figure( figsize=(14,14) )

    ax1 = fig.add_subplot( 311 )
    ax1.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax1.plot(att[0,:_len], label='realtime euler x')
    ax1.plot(attcmd[0,:_len], label='realtime euler input x')
    ax1.legend()
    ax1.grid()

    ax2 = fig.add_subplot( 312 )
    ax2.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax2.plot(att[1,:_len], label='realtime euler y')
    ax2.plot(attcmd[1,:_len], label='realtime euler input y')
    ax2.legend()
    ax2.grid()

    ax3 = fig.add_subplot( 313 )
    ax3.axvspan( _stt, _end, facecolor='gray', alpha=0.5 )
    ax3.plot(att[2,:_len], label='realtime euler z')
    ax3.plot(attcmd[2,:_len], label='realtime euler input z')
    ax3.legend()
    ax3.grid()

    plt.savefig( f'./flight_data/{date}/att.png' )


def plot_trj( pos, _len, _stt, _end, date ):

    fig = plt.figure( figsize=(14,14) )

    ax = fig.add_subplot( 111, projection='3d' )
    ax.plot( pos[0,    :_len], pos[1,_stt:_end], pos[2,_stt:_end], label='trajectory', linewidth=10, alpha=0.5 )
    ax.plot( pos[0,_stt:_end], pos[1,_stt:_end], pos[2,_stt:_end], label='optimal guidance' )

    ax.legend()

    plt.savefig( f'./flight_data/{date}/3d-trj.png' )