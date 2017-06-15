from unittest import TestCase

import gps


class TestGps(TestCase):
    def setUp(self):
        self.g = gps.Gps()

    def tearDown(self):
        # print(self.res)
        pass

    def test_parse_gprmc(self):
        res = self.g.parse(b'$GPRMC,083139.00,V,4252.228736,N,2518.899679,S,88,99,260517,88,77,N*7A\r\n')
        self.assertIsNone(res)
        res = self.g.parse(b'$GPGGA,083139.00,6,7,8,9,7,8,99.99,76,4,38,54,67,10*66\r\n')
        self.assertIsNone(res)
        res = self.g.parse(b'$GPRMC,083139.00,V,4252.228736,N,2518.899679,S,88,99,260517,88,77,N*7A\r\n')
        latitude, longitude = self.g.dm2dd(4252.228736, 2518.899679)
        dict = {}
        dict['Latitude'] = str(latitude)
        dict['Longitude'] = str(longitude)
        dict['Date'] = '260517'
        dict['Time'] = '083139.00'
        self.assertDictEqual(dict, res)

    def test_parse_gpgga(self):
        res = self.g.parse(b'$GPGGA,083139.00,,,,,0,00,99.99,,,,,,*66\r\n')
        self.assertIsNone(res)

    def test_parse(self):
        res = self.g.parse(b'$XXXXX,083139.00,V,,,,,,,260517,,,N*7A\r\n')
        self.assertIsNone(res)


class TestGps(TestCase):
    def setUp(self):
        self.g = gps.Gps()

    def test_dm2dd(self):
        res = self.g.dm2dd(4252.228736, 2518.899679)
        self.assertTupleEqual((42.87047893333333, 25.31499465), res)
