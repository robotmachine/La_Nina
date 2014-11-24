#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La Niña
Command Line Weather using the http://wunderground.com API
Author: Brian Carter
http://github.com/robotmachine/La_Nina

Originally forked from niño || https://github.com/drbunsen/nino
"""
import os, sys, urllib, urllib.request, http.client, configparser, textwrap, argparse, json

settings = os.path.expanduser("~/.nina")
if os.path.exists(settings):
	dotfile = True
elif not os.path.exists(settings):
	dotfile = False
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
	parser.add_argument('--edit-config', dest="EDIT",
		action='store_true', default=False,
		help='Create or edit config file.')
	args = parser.parse_args()
	EDIT = args.EDIT
	APIKEY = args.APIKEY
	ZIP = args.ZIP
	if EDIT is True:
		set_config()
	if dotfile is True and APIKEY is None:
		config.read(settings)
		APIKEY = config['NINA']['APIKEY']
	if dotfile is True and ZIP is None:
		config.read(settings)
		ZIP = config['NINA']['ZIP']
	if ZIP is not None and APIKEY is not None:
		"""print("Would have called a simple forecast with API key {} and ZIP {}".format(APIKEY, ZIP))"""
		simple_forecast(APIKEY, ZIP)
	if ZIP is None and APIKEY is None:
		set_config(dotfile)

""" Create config file """
def set_config(dotfile):
	if dotfile is False:
		try:
			print(textwrap.dedent("""
			A Wunderground API Key is required.
			Create one for free here:
			http://www.wunderground.com/weather/api
			"""))
			APIKEY = input("Wunderground API Key: ")
			print(textwrap.dedent("""
			Set your local ZIP code to use as the default
			"""))
			ZIP = input("ZIP: ")
			if (ZIP == ""):
				ZIP = False
			config ['NINA'] = {'APIKEY': APIKEY,
				'ZIP': ZIP}
			with open(settings, 'w') as configfile:
				config.write(configfile)
			print("Settings saved!")
			dotfile = True
			main()
		except KeyboardInterrupt:
			print("\nUser exit.")
			quit()
		except SyntaxError:
			print("\nSyntax Error.")
			set_config(dotfile)
			
	elif dotfile is True:
		config.read(settings)
		APIKEY = config['NINA']['APIKEY']
		ZIP = config['NINA']['ZIP']
		print(textwrap.dedent("""
		Current stored API key is {}
		Would you like to change it?
		""".format(APIKEY)))
		BOOL1 = input("Y/N: ")
		if BOOL1 in ['Y', 'y', 'Yes', 'YES', 'yes']:
			APIKEY = input("New API key: ")
			config ['NINA'] = {'APIKEY': APIKEY}
			with open(settings, 'w') as configfile:
				config.write(configfile)
		else:
			print(textwrap.dedent("Keeping {} in config file.".format(APIKEY)))
		print(textwrap.dedent("""
		Current stored ZIP is {}
		Would you like to change it?
		""".format(ZIP)))
		BOOL2 = input("Y/N: ")
		if BOOL2 in ['Y', 'y', 'Yes', 'YES', 'yes']:
			ZIP = input("New ZIP: ")
			config ['NINA'] = {'ZIP': ZIP}
			with open(settings, 'w') as configfile:
				config.write(configfile)
		else:
			print(textwrap.dedent("Keeping {} in config file.".format(ZIP)))
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
	""" Test if the provided ZIP code is valid. """	
	try:
		location = data['current_observation']['display_location']['full']
	except:
		location = False
	try:
		error = data['response']['error']['description']
	except:
		error = False
	if location is False and error is not False:
		print(error)
		quit()
	elif location is not False and error is False:
		print('\n{0}\n'.format(location))
	else:
		print("Location returned: {}".format(location))
		print("Error returned: {}".format(error))
		quit()
	times = (0, 1, 2)
	for time in times:
		weather_data = weather(data, time)
		cli_output = cli_format(weather_data)
		print(cli_output)
main()
