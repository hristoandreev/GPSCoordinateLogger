from unittest import TestCase

import gps


class TestGps(TestCase):
    def setUp(self):
        self.g = gps.Gps()

    def tearDown(self):
        print(self.res)

    def test_parse_gprmc(self):
        self.res = self.g.parse(b'$GPRMC,083139.00,V,44.5673,N,25.56789,S,88,99,260517,88,77,N*7A\r\n')
        self.res = self.g.parse(b'$GPGGA,083139.00,6,7,8,9,7,8,99.99,76,4,38,54,67,10*66\r\n')
        self.res = self.g.parse(b'$GPRMC,083139.00,V,44.5673,N,25.56789,S,88,99,260517,88,77,N*7A\r\n')
        #self.fail()

    def test_parse_gpgga(self):
        self.res = self.g.parse(b'$GPGGA,083139.00,,,,,0,00,99.99,,,,,,*66\r\n')

    def test_parse(self):
        self.res = self.g.parse(b'$XXXXX,083139.00,V,,,,,,,260517,,,N*7A\r\n')