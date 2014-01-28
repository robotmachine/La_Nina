#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Brian Carter
http://github.com/robotmachine/La_Nina
""" """
Originally forked from niño || https://github.com/drbunsen/nino
"""
import os, sys, urllib, urllib.request, http.client, configparser, textwrap, argparse, json

""" Set config file """
settings = os.path.expanduser("~/.nina")
config = configparser.ConfigParser()

""" Main """
def main():
	parser = argparse.ArgumentParser(description='Niña: Gets Wunderground weather reports. Example: nina 29072', prog='nina')
	parser.add_argument('-z','--zip',
		action='store', dest='ZIP', default=None,
		help='Zip code for weather. If nothing is provided, use favourite zip from config file.')
	parser.add_argument('-k','--key',
		action='store', dest='APIKEY', default=None,
		help='API key from http://www.wunderground.com/weather/api')
	args = parser.parse_args()
	APIKEY = args.APIKEY
	ZIP = args.ZIP
	if os.path.exists(settings):
		config.read(settings)
		if APIKEY is None:
			APIKEY = config['NINA']['APIKEY']
		if ZIP is None:
			ZIP = config['NINA']['ZIP']
	if ZIP is not None and APIKEY is not None:
		simple_forecast(APIKEY, ZIP)
	if ZIP is None and APIKEY is None:
		set_config()

""" Create config file """
def set_config():
	print(textwrap.dedent("""
	A Wunderground API Key is required.
	Create one for free here:
	http://www.wunderground.com/weather/api
	"""))
	APIKEY = input("Wunderground API Key: ")
	if (APIKEY == ""):
		print(textwrap.dedent("""
		API Key is not optional!
		Create one for free and return!
		http://www.wunderground.com/weather/api
		"""))
		quit()
	print(textwrap.dedent("""
	Set your local ZIP code to use as the default
	"""))
	ZIP = input("ZIP: ")
	if (APIKEY == ""):
		print(textwrap.dedent("""
		API Key is not optional!
		Create one for free and return!
		http://www.wunderground.com/weather/api
		"""))
		quit()
	config ['NINA'] = {'APIKEY': APIKEY,
		'ZIP': ZIP}
	with open(settings, 'w') as configfile:
		config.write(configfile)
	print("Settings saved!")
	quit()

""" Assemble weather data. """
def weather(data, day_idx):
    dat = data['forecast']['txt_forecast']['forecastday'][day_idx]
    day = dat['title']
    forecast = dat['fcttext']
    temps = data['forecast']['simpleforecast']['forecastday'][day_idx]
    high = temps['high']['fahrenheit']
    low = temps['low']['fahrenheit']
    return day, forecast, high, low

""" Format weather data. """
def cli_format(d):
    forecast = '\n'.join(textwrap.wrap(d[1], 60))
    temp = '{loc}\n{delim}\n\nHigh {high}{deg}, Low {low}{deg}\n\n{forecast}\n'
    out = temp.format(loc=d[0], 
                      forecast=forecast, 
                      high=d[2], 
                      low=d[3], 
                      delim=60*'=',
                      deg='°F')
    return out


""" Simple forecast (today, tonight, and tomorrow)  """
def simple_forecast(APIKEY, ZIP):
	wunder_data = {'api_url': 'http://api.wunderground.com/api/',
			'api_key': APIKEY,
			'query': '/conditions/forecast/q/',
			'zip': ZIP}	
	url = '{api_url}{api_key}{query}{zip}.json'.format(**wunder_data)
	response = urllib.request.urlopen(url)
	content = response.read()
	data = json.loads(content.decode("utf8"))
	location = data['current_observation']['display_location']['full']
	print('\n{0}\n'.format(location))
	times = (0, 1, 2)
	for time in times:
		weather_data = weather(data, time)
		cli_output = cli_format(weather_data)
		print(cli_output)
main()
