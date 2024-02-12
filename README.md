# SunTime

Simple sunset and sunrise time calculation python library forked from pypi [suntime](https://github.com/SatAgro/suntime/) library.


## Usage

You can use the library to get UTC and local time sunrise and sunset times typing:

```python
from suntime import Sun, DegreesOffset, SunTimeException

MADRID_LAT = 40.416775
MADRID_LON = -3.703790

madrid_sun = Sun(MADRID_LAT, MADRID_LON)

# Get today's sunrise and sunset in UTC
sunrise_madrid = madrid_sun.get_sunrise_time()

today_ss = sun.get_sunset_time()
today_sr = sun.get_local_sunset_time()
print('Today at Madrid the sun raised at {} and get down at {} UTC'.
      format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

# On a special date in your machine's local time zone
abd = datetime.date(2014, 10, 3)
abd_sr = sun.get_local_sunrise_time(abd)
abd_ss = sun.get_local_sunset_time(abd)
print('On {} the sun at Madrid raised at {} and get down at {}.'.
      format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))

# offsets
horizon = madrid_sun.get_local_sunset_time(
    degrees_offset=DegreesOffset.horizon.value) # 0

civil = madrid_sun.get_local_sunset_time(
    degrees_offset=DegreesOffset.civil.value) # 6

nautical = madrid_sun.get_local_sunset_time(
    degrees_offset=DegreesOffset.nautilcal.value) # 12

astronomical = madrid_sun.get_local_sunset_time(
    degrees_offset=DegreesOffset.astronomical.value) # 18

```

## References

* [library improvement: Dusk dawn calculation](https://www.timeanddate.com/astronomy/different-types-twilight.html)
* Forked from [suntime](https://github.com/SatAgro/suntime/)