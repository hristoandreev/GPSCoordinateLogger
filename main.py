import gps
import _thread

g = gps.Gps()

def th_gps():
    global g
    print('GPS thread started.')
    while True:
        d = g.parse(g.readData)

        if d is None:
            continue

        try:
            f = open(d.get('Date') + '_log.csv', 'r+')
        except OSError:
            f = open(d.get('Date') + '_log.csv', 'w+')
            f.write('Latitude,Longitude,Date,Time\n')

        f.seek(0, 2)
        f.write(d.get('Latitude') + ',' +
                d.get('Longitude') + ',' +
                d.get('Date') + ',' +
                d.get('Time') + '\n')
        f.close()

_thread.start_new_thread(th_gps, ())
