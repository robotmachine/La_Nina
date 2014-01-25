La Niña: Command Line Weather
=============================

La Niña is a simple command line interface for the Wunderground API written in Python.  
Originally a fork of [Niño][1]

You Will Need:
--------------

* Python 3.3+ (Tested with 3.3.3)  
* [Wunderground API key][2]

Usage:
------

La Niña can be used with either command line arguments or with a config file.

With arguments:
`$> nina -z 97405 -k [redacted]`

If no arguments are provided, La Niña will ask to set a ~/.nina config file for your API key and a default ZIP code.

[1]: https://github.com/drbunsen/nino
[2]: http://www.wunderground.com/weather/api/
