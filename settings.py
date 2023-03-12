import json

version = '1.4.0'
settings = {}


def writesettings():
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, ensure_ascii=True, sort_keys=True)


def initialise():
    global settings
    settings['logging'] = {}
    settings['logging']['logfilepath'] = './logs/pumpreader.log'
    settings['logging']['logappname'] = 'Pumpreader-Py'
    settings['logging']['gunicornpath'] = './logs/'
    settings['logging']['cputemp'] = '/sys/class/thermal/thermal_zone0/temp'
    settings['logging']['syslog'] = '/var/log/syslog'
    settings['turbo'] = {}
    settings['turbo']['port'] = '/dev/ttyUSB0'
    settings['turbo']['speed'] = 9600
    settings['tank'] = {}
    settings['tank']['port'] = '/dev/ttyUSB1'
    settings['tank']['speed'] = 9600
    settings['ion'] = {}
    settings['ion']['port'] = '/dev/ttyUSB2'
    settings['ion']['speed'] = 9600
    settings['pyro'] = {}
    settings['pyro']['port'] = '/dev/ttyUSB3'
    settings['pyro']['speed'] = 115200
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, ensure_ascii=True, sort_keys=True)


def readsettings():
    global settings
    try:
        with open('settings.json') as json_file:
            settings = json.load(json_file)
    except FileNotFoundError:
        initialise()
    settings['turbo']['string1'] = b'PR1\r'
    settings['turbo']['string2'] = b'\x05'
    settings['turbo']['start'] = 5
    settings['turbo']['length'] = 16
    settings['tank']['string1'] = b'PR1\r'
    settings['tank']['string2'] = b'\x05'
    settings['tank']['start'] = 5
    settings['tank']['length'] = 16
    settings['ion']['string1'] = b'~ 05 0B 00\r'
    settings['ion']['start'] = 9
    settings['ion']['length'] = 16
    settings['pyro']['readtemp'] = b'\x01'
    settings['pyro']['readlaser'] = b'\x25'
    settings['pyro']['laseron'] = b'\xA5\x01\xA4'
    settings['pyro']['laseroff'] = b'\xA5\x00\xA5'


readsettings()
