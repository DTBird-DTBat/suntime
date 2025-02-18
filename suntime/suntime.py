import calendar
import math
import datetime
from dateutil import tz
from enum import Enum


class DegreesOffset(Enum):
    horizon = 0
    civil = 6
    nautilcal = 12
    astronomical = 18


class SunTimeException(Exception):

    def __init__(self, message):
        super(SunTimeException, self).__init__(message)


class Sun:
    """
    Approximated calculation of sunrise and sunset datetimes. Adapted from:
    https://stackoverflow.com/questions/19615350/calculate-sunrise-and-sunset-times-for-a-given-gps-coordinate-within-postgresql
    """
    def __init__(self, lat, lon, zenith=90.8):
        """
        :param lat(float): Latitude
        :param lon(float): Longitude
        :param zenith(float): zenith default position (degrees)
        """
        self._lat = lat
        self._lon = lon
        self._ZENITH = zenith

    def get_sunrise_time(
            self,
            date: datetime.datetime = None,
            degrees_offset: float = DegreesOffset.horizon.value):
        """
        Calculate the sunrise time for given date.
        :param date: Reference date. Today if not provided.
        :param degrees_offset(DegreesOffset): offset degrees respect
        the horizon
        :raises: SunTimeException when there is no sunrise and sunset
        on given location and date
        :return: UTC sunrise datetime
        """
        return self._calc_sun_time(date, True, offset=degrees_offset)

    def get_local_sunrise_time(
            self,
            date: datetime = None,
            degrees_offset: float = DegreesOffset.horizon.value,
            local_time_zone: tz.tzlocal = tz.tzlocal()):
        """
        Get sunrise time for local or custom time zone.
        :param date: Reference date. Today if not provided.
        :param degrees_offset(DegreesOffset): offset degrees
        respect the horizon
        :param local_time_zone: Local or custom time zone.
        :raises: SunTimeException when there is no sunrise and sunset
        on given location and date.
        :return: Local time zone sunrise datetime
        """
        return self._calc_sun_time(
            date,
            True,
            offset=degrees_offset,
            timezone=local_time_zone)

    def get_sunset_time(
            self,
            date: datetime.datetime = None,
            degrees_offset: float = DegreesOffset.horizon.value):
        """
        Calculate the sunset time for given date.
        :param date: Reference date. Today if not provided.
        :param degrees_offset(DegreesOffset): offset degrees
        respect the horizon
        :return: UTC sunset datetime
        :raises: SunTimeException when there is no sunrise and sunset
        on given location and date.
        """
        return self._calc_sun_time(date, False, offset=degrees_offset)

    def get_local_sunset_time(
            self,
            date: datetime.datetime = None,
            degrees_offset: float = DegreesOffset.horizon.value,
            local_time_zone: tz.tzlocal = tz.tzlocal()):
        """
        Get local sunset time for local or custom time zone.
        :param date: Reference date. Today if not provided.
        :param degrees_offset(DegreesOffset): offset degrees
        respect the horizon
        :param local_time_zone: Local or custom time zone.
        :raises: SunTimeException when there is no unrise and sunset
        on given location and date.
        :return: Local time zone sunrise datetime
        """
        return self._calc_sun_time(
            date,
            False,
            offset=degrees_offset,
            timezone=local_time_zone)

    def _calc_sun_time(
            self,
            date,
            isRiseTime=True,
            offset=None,
            timezone=None):
        """
        Calculate sunrise or sunset date.
        :param date: Reference date
        :param isRiseTime: True if you want to calculate sunrise time.
        :param offset: Dawn/dusk offset relative to the Sun reference zenith
        :param local_time_zone: Local or custom time zone.
        :return: UTC sunset or sunrise datetime if no local_timezone specified.
        :raises: SunTimeException when there is no dawn/dusk
        on given location and date
        """
        date = datetime.date.today() if date is None else date
        zenith = self._ZENITH\
            if offset is None else (self._ZENITH + (+1 * offset))
        # isRiseTime == False, returns sunsetTime
        day = date.day
        month = date.month
        year = date.year

        TO_RAD = math.pi/180.0

        # 1. first calculate the day of the year
        N1 = math.floor(275 * month / 9)
        N2 = math.floor((month + 9) / 12)
        N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
        N = N1 - (N2 * N3) + day - 30

        # 2. convert the longitude to hour value and calculate
        # an approximate time
        lngHour = self._lon / 15

        if isRiseTime:
            t = N + ((6 - lngHour) / 24)
        else:  # sunset
            t = N + ((18 - lngHour) / 24)

        # 3. calculate the Sun's mean anomaly
        M = (0.9856 * t) - 3.289

        # 4. calculate the Sun's true longitude
        L = M \
            + (1.916 * math.sin(TO_RAD*M))\
            + (0.020 * math.sin(TO_RAD * 2 * M))\
            + 282.634

        # NOTE: L adjusted into the range [0,360)
        L = self._force_range(L, 360)

        # 5a. calculate the Sun's right ascension

        RA = (1/TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD*L))
        # NOTE: RA adjusted into the range [0,360)
        RA = self._force_range(RA, 360)

        # 5b. right ascension value needs to be in the same quadrant as L
        Lquadrant = (math.floor(L/90)) * 90
        RAquadrant = (math.floor(RA/90)) * 90
        RA = RA + (Lquadrant - RAquadrant)

        # 5c. right ascension value needs to be converted into hours
        RA = RA / 15

        # 6. calculate the Sun's declination
        sinDec = 0.39782 * math.sin(TO_RAD*L)
        cosDec = math.cos(math.asin(sinDec))

        # 7a. calculate the Sun's local hour angle
        cosH = (
            math.cos(TO_RAD*zenith) - (sinDec * math.sin(TO_RAD*self._lat)))\
            / (cosDec * math.cos(TO_RAD*self._lat))

        if cosH > 1 or cosH < -1:
            # The sun never rises on this location (on the specified date)
            msg = 'The sun never sets on this location (on the specified date)'
            raise SunTimeException(msg)

        # 7b. finish calculating H and convert into hours

        if isRiseTime:
            H = 360 - (1/TO_RAD) * math.acos(cosH)
        else:  # setting
            H = (1/TO_RAD) * math.acos(cosH)

        H = H / 15

        # 8. calculate local mean time of rising/setting
        T = H + RA - (0.06571 * t) - 6.622

        # 9. adjust back to UTC
        UT = T - lngHour
        # UTC time in decimal format (e.g. 23.23)
        UT = self._force_range(UT, 24)

        # 10. Return
        hr = self._force_range(int(UT), 24)
        min = round((UT - int(UT))*60, 0)
        if min == 60:
            hr += 1
            min = 0

        # 11. check corner case https://github.com/SatAgro/suntime/issues/1
        if hr == 24:
            hr = 0
            day += 1

            if day > calendar.monthrange(year, month)[1]:
                day = 1
                month += 1

                if month > 12:
                    month = 1
                    year += 1
        result = datetime.datetime(
            year,
            month,
            day,
            hr,
            int(min),
            tzinfo=tz.tzutc())
        return result.astimezone(timezone) if timezone else result

    @staticmethod
    def _force_range(v, max):
        # force v to be >= 0 and < max
        if v < 0:
            return v + max
        elif v >= max:
            return v - max

        return v
