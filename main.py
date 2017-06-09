import gps
import _thread

g = gps.Gps()

def th_gps():
    global g
    print('GPS thread started.')
    while True:
        g.start()

_thread.start_new_thread(th_gps, ())
