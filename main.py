import gps
import _thread
import time

g = gps.Gps()

def th_gps():
    global g

    print('GPS thread started.')

    while True:
        time.sleep_ms(100)
        ba = g.readData()
        # print(ba)
        if ba is None:
            continue

        #print(ba)
        d = g.parse(ba)

        if d is None:
            continue

        #print('d -> {}'.format(d))

        try:
            f = open('gps_logs/' + d.get('Date') + '_log.csv', 'r+')
        except OSError:
            f = open('gps_logs/' + d.get('Date') + '_log.csv', 'w+')
            f.write('Latitude,Longitude,Date,Time,Satellites,Quality\n')

        f.seek(0, 2)
        print('Writing GPS data to file...', end=' ')
        f.write(d.get('Latitude') + ',' +
                d.get('Longitude') + ',' +
                d.get('Date') + ',' +
                d.get('Time') + ',' +
                d.get('Satellites') + ',' +
                d.get('Quality') + '\n')
        f.close()
        print('done')

_thread.start_new_thread(th_gps, ())
