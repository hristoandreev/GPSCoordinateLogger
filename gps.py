try:
    import pyb
except ImportError:
    import tests.pyb as pyb

try:
    import ure
except ImportError:
    import re as ure


class Gps:

    def __init__(self):
        self._uart1 = pyb.UART(1)
        #self.buff = bytearray(500)
        self._longitude = 0.0
        self._latitude = 0.0
        self._time = 0
        self._date = ''
        self._usedSats = 0
        self._dataQuality = 0
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
                    'dummy',
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
            #'^\$(GPRMC)' + ',([^,]*)' * 12 + '\r\n',
            '^\$(GPRMC),([0-9][0-9][0-9][0-9][0-9][0-9]).[0-9][0-9],([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),'
            '([^,]*),([^,]*),([^,]*),([^,]*),(\w?)\*([0-9A-F][0-9A-F])',
            '^\$(GPGGA),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),'
            '([^,]*),([^,]*),([0-9]*)\*([0-9A-F][0-9A-F])',
            #'^\$(GPVTG)' + ',([^,]*)' * 9 + '\r\n',
            #'^\$(GPGGA),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)',
            # '^\$(GPGSA)' + ',([^,]*)' * 16 + '\r\n',
            # '^\$(GPGSV)' + ',([^,]*)' * 20 + '\r\n',
            #'^\$(GPGLL)' + ',([^,]*)' * 7 + '\r\n',
            #^\$(GPRMC),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),(\w*)\*([0-9A-F]{2})$
        ]

        self._regxc = [ure.compile(s) for s in self._regx]
        self._uart1.init(9600, read_buf_len=4096)

    def readData(self):
        return self._uart1.readline()

    def parse(self, buff:bytearray):
        #print(buff)
        buf_dec = buff.decode('utf-8')

        #print(buf_dec)
        dictionary = {}
        for r in self._regxc:
            m = r.match(buf_dec)

            if m is None:
                continue

            self._cmd = m.group(1)
            # print('cmd -> {}'.format(self._cmd))
            i = 1
            for name in self._d[self._cmd]:
                 #print('{} -> {}'.format(name, m.group(i)))
                 dictionary[name] = m.group(i)
                 i += 1

            break
        else:
            return None

        #print('Dict -> {}'.format(dictionary))
        #print('Cmd -> {}'.format(dictionary.get('Cmd')))
        if dictionary.get('Cmd') == 'GPGGA':
            if (dictionary.get('NumberOfSatInUse') != '' and dictionary.get('NumberOfSatInUse') is not None and
                dictionary.get('GPSQualityIndicator') != '' and dictionary.get('GPSQualityIndicator') is not None):
                self._usedSats = int(dictionary.get('NumberOfSatInUse'))
                self._dataQuality = int(dictionary.get('GPSQualityIndicator'))
                print('Used Satellites -> {:d}'.format(self._usedSats))
                print('Quality -> {:d}'.format(self._dataQuality))
        elif dictionary.get('Cmd') == 'GPRMC':
            print('CurrLatitude -> {:s}'.format(dictionary.get('CurrLatitude')))
            print('CurrLongitude -> {:s}'.format(dictionary.get('CurrLongitude')))

            if (dictionary.get('CurrLatitude') != '' and dictionary.get('CurrLongitude') != '' and
                dictionary.get('DateStamp') != '' and dictionary.get('TimeStamp') != ''):

                latitude = float(dictionary.get('CurrLatitude'))
                longitude = float(dictionary.get('CurrLongitude'))
                self._time = int(dictionary.get('TimeStamp'))
                self._time += 30000; # +3 hours forward for summer time.
                self._date = dictionary.get('DateStamp')

                c, d = self.dm2dd(latitude, longitude)

                # print('lat -> {:.6f}'.format(c))
                # print('long -> {:.6f}'.format(d))

                if (not ((self._latitude + 0.0002) > c and (self._latitude - 0.0002) < c) or
                        not ((self._longitude + 0.0002) > d and (self._longitude - 0.0002) < d)):
                    if self._dataQuality > 0:
                        if self._usedSats >= 5:
                            self._latitude = c
                            self._longitude = d
                            # print('Time -> {}'.format(self._time))
                            # print('Latitude -> {:.6f}'.format(self._latitude))
                            # print('Longitude -> {:.6f}'.format(self._longitude))

                            dict = {}
                            dict['Latitude'] = str(self._latitude)
                            dict['Longitude'] = str(self._longitude)
                            dict['Date'] = '{0}{1}.{2}{3}.{4}{5}'.format(*self._date)
                            dict['Time'] = '{0}{1}:{2}{3}:{4}{5}'.format(*str(self._time))
                            dict['Satellites'] = str(self._usedSats)
                            dict['Quality'] = str(self._dataQuality)

                            pyb.LED(1).toggle()

                            return dict
        else:
            return None


        return None


    def dm2dd(self, latitude:float, longitude:float):
        """ Convert degrees minute to decimal degrees GPS coordinate. """

        lat_deg = (latitude // 100)
        long_deg = (longitude // 100)
        a = (((latitude * 1000000.0) % 100000000) / 60.0) % 1000000
        b = (((longitude * 1000000.0) % 100000000) / 60.0) % 1000000
        c = a / 1000000.0 + lat_deg
        d = b / 1000000.0 + long_deg

        return c, d
