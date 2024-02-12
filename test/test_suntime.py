import unittest
from suntime import Sun, DegreesOffset, SunTimeException

MADRID_LAT = 40.416775
MADRID_LON = -3.703790
LISBON_LAT = 38.736946
LISBON_LON = -9.142685


class SuntimeTest(unittest.TestCase):
    def test_dusk(self):
        madrid_sun = Sun(MADRID_LAT, MADRID_LON)
        lisbon_sun = Sun(LISBON_LAT, LISBON_LON)
        # Get today's sunrise and sunset in UTC
        sunrise_madrid = madrid_sun.get_sunset_time()
        sunrise_lisbon = lisbon_sun.get_sunset_time()
        self.assertTrue(sunrise_madrid < sunrise_lisbon)

    def test_dawn(self):
        madrid_sun = Sun(MADRID_LAT, MADRID_LON)
        lisbon_sun = Sun(LISBON_LAT, LISBON_LON)
        # Get today's sunrise and sunset in UTC
        sunrise_madrid = madrid_sun.get_sunrise_time()
        sunrise_lisbon = lisbon_sun.get_sunrise_time()
        self.assertTrue(sunrise_madrid < sunrise_lisbon)

    def test_suntime_error(self):
        sun = Sun(85.0, 21.00)
        self.assertRaises(SunTimeException, sun.get_sunrise_time)

    def test_dusk_offset(self):
        madrid_sun = Sun(MADRID_LAT, MADRID_LON)

        sunrise_madrid = madrid_sun.get_sunset_time()
        horizon = madrid_sun.get_local_sunset_time(
            degrees_offset=DegreesOffset.horizon.value)
        civil = madrid_sun.get_local_sunset_time(
            degrees_offset=DegreesOffset.civil.value)
        nautical = madrid_sun.get_local_sunset_time(
            degrees_offset=DegreesOffset.nautilcal.value)
        astronomical = madrid_sun.get_local_sunset_time(
            degrees_offset=DegreesOffset.astronomical.value)

        self.assertTrue(sunrise_madrid == horizon)
        self.assertTrue(horizon < civil)
        self.assertTrue(civil < nautical)
        self.assertTrue(nautical < astronomical)

    def test_dawn_offset(self):
        madrid_sun = Sun(MADRID_LAT, MADRID_LON)

        sunrise_madrid = madrid_sun.get_local_sunrise_time()
        horizon = madrid_sun.get_local_sunrise_time(
            degrees_offset=DegreesOffset.horizon.value)
        civil = madrid_sun.get_local_sunrise_time(
            degrees_offset=DegreesOffset.civil.value)
        nautical = madrid_sun.get_local_sunrise_time(
            degrees_offset=DegreesOffset.nautilcal.value)
        astronomical = madrid_sun.get_local_sunrise_time(
            degrees_offset=DegreesOffset.astronomical.value)

        self.assertTrue(sunrise_madrid == horizon)
        self.assertTrue(horizon > civil)
        self.assertTrue(civil > nautical)
        self.assertTrue(nautical > astronomical)
