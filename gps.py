import pyb
import ure
import time


class Gps:

    def __init__(self):
        self._uart1 = pyb.UART(1)
        self.buff = bytearray(500)
        self._longitude = 0.0
        self._latitude = 0.0
        self._time = ''
        self._date = ''
        self._d = {
            'GPRMC':
                    ['Cmd',
                    'TimeStamp',
                    'Validity',
                    'CurrLatitude',
                    'LatDir',
                    'CurrLongitude',
                    'LongDir',
                    'SpeedInKnots',
                    'TrueCourse',
                    'DateStamp',
                    'Variation',
                    'VarDir',
                    'Checksum'],
            'GPVTG':
                    ['Cmd',
                     'TrackDegTrue',
                    'FixedTextT',
                    'TrackDegMag',
                    'FixedTextM',
                    'SpeedKnots',
                    'FixedTextN',
                    'SpeedKmvsHr',
                    'FixedTextK',
                    'Checksum'],
            'GPGGA':
                    ['Cmd',
                     'UTCOfPosition',
                    'Latitude',
                    'LatDir',
                    'Longitude',
                    'LongDir',
                    'GPSQualityIndicator',
                    'NumberOfSatInUse',
                    'HorizontalDilution',
                    'AntenaAltitude',
                    'AntMeters',
                    'GeoidalSeparation',
                    'GeoMeters',
                    'AgeInSeconds',
                    'DiffID',
                    'Checksum'],
            'GPGSA':
                    ['Cmd',
                     'Mode1',
                    'Mode2',
                    'ID1',
                    'ID2',
                    'ID3',
                    'ID4',
                    'ID5',
                    'ID6',
                    'ID7',
                    'ID8',
                    'ID9',
                    'ID10',
                    'ID11',
                    'ID12',
                    'PDOP',
                    'HDOP',
                    'VDOP',
                    'Checksum'],
            'GPGSV':
                    ['Cmd',
                     'TotalMEssages',
                    'MessageNumber',
                    'TotalSVsInView',
                    'SVNumber1',
                    'ElevationDeg1',
                    'AzimuthDeg1',
                    'SNR1',
                    'SVNumber2',
                    'ElevationDeg2',
                    'AzimuthDeg2',
                    'SNR2',
                    'SVNumber3',
                    'ElevationDeg3',
                    'AzimuthDeg3',
                    'SNR3',
                    'SVNumber4',
                    'ElevationDeg4',
                    'AzimuthDeg4',
                    'SNR4',
                    'Checksum'],
            'GPGLL':
                    ['Cmd',
                     'CurrLatitude',
                    'LatDir',
                    'CurrLongitude',
                    'LongDir',
                    'UTC',
                    'DataValid',
                    'Checksum'],
        }
        self._cmd = None
        self._regx = [
            '^\$(GPRMC)' + ',([^,]*)' * 12 + '\r\n',
            '^\$(GPVTG)' + ',([^,]*)' * 9 + '\r\n',
            # '^\$(GPGGA)' + ',([^,]*)' * 15 + '\r\n',
            # '^\$(GPGSA)' + ',([^,]*)' * 16 + '\r\n',
            # '^\$(GPGSV)' + ',([^,]*)' * 20 + '\r\n',
            '^\$(GPGLL)' + ',([^,]*)' * 7 + '\r\n',
            #^\$(GPRMC),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),(\w*)\*([0-9A-F]{2})$
        ]

        self._regxc = [ure.compile(s) for s in self._regx]
        self._uart1.init(9600, read_buf_len=1024)

    def start(self):
        #self._uart1.init(9600, read_buf_len=1024)

        #while True:
        self.buff = self._uart1.readline()
        if self.buff is None:
            #continue
            return

        buf_dec = self.buff.decode()

        # print(buf_dec)
        dictionary = {}
        for r in self._regxc:
            m = r.match(buf_dec)

            if m is None:
                continue

            self._cmd = m.group(1)
            # print('cmd -> {}'.format(self._cmd))
            i = 1
            for name in self._d[self._cmd]:
                dictionary[name] = m.group(i)
                i += 1

            break

        if dictionary.get('Cmd') is 'GPRMC':
            # print('CurrLatitude -> {}'.format(dictionary.get('CurrLatitude')))
            # print('CurrLongitude -> {}'.format(dictionary.get('CurrLongitude')))
            if (dictionary.get('CurrLatitude') is not '' and dictionary.get('CurrLongitude') is not '' and
                dictionary.get('DateStamp') is not '' and dictionary.get('TimeStamp') is not ''):

                latitude = float(dictionary.get('CurrLatitude'))
                longitude = float(dictionary.get('CurrLongitude'))
                self._time = dictionary.get('TimeStamp')
                self._date = dictionary.get('DateStamp')

                lat_deg = (latitude // 100)
                long_deg = (longitude // 100)

                a = (((latitude * 1000000.0) % 100000000) / 60.0) % 1000000
                b = (((longitude * 1000000.0) % 100000000) / 60.0) % 1000000

                c = a / 1000000.0 + lat_deg
                d = b / 1000000.0 + long_deg

                # print('lat -> {:.6f}'.format(c))
                # print('long -> {:.6f}'.format(d))

                if (not ((self._latitude + 0.0002) > c and (self._latitude - 0.0002) < c) or
                        not ((self._longitude + 0.0002) > d and (self._longitude - 0.0002) < d)):

                    self._latitude = c
                    self._longitude = d
                    # print('Time -> {}'.format(self._time))
                    #print('Latitude -> {:.6f}'.format(self._latitude))
                    #print('Longitude -> {:.6f}'.format(self._longitude))

                    try:
                        f = open(self._date + '_log.csv', 'r+')
                    except OSError:
                        f = open(self._date + '_log.csv', 'w+')
                        f.write('Latitude,Longitude,Date,Time\n')

                    f.seek(0, 2)
                    pyb.LED(1).toggle()
                    f.write(str(self._latitude) + ',' +
                            str(self._longitude) + ',' +
                            self._date + ',' +
                            self._time + '\n')
                    f.close()

        return
            #time.sleep(1)


# b'$GPRMC,083139.00,V,,,,,,,260517,,,N*7A\r\n'
# b'$GPVTG,,,,,,,,,N*30\r\n'
# b'$GPGGA,083139.00,,,,,0,00,99.99,,,,,,*66\r\n'
# b'$GPGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*30\r\n'
# b'$GPGSV,3,1,12,01,04,040,,10,05,324,,12,27,245,,13,53,178,*77\r\n'
# b'$GPGSV,3,2,12,15,58,254,,17,52,085,,18,09,300,,19,52,128,*7A\r\n'
# b'$GPGSV,3,3,12,20,03,234,,24,41,302,,28,25,054,,30,09,105,*7E\r\n'
# b'$GPGLL,,,,,083139.00,V,N*4A\r\n'