import json
from datetime import datetime
import base64

version = '2.0.0'


def json_encoder(byte_obj):
    if isinstance(byte_obj, (bytes, bytearray)):
        # File Bytes to Base64 Bytes then to String
        return base64.b64encode(byte_obj).decode('utf-8')
    raise ValueError('No encoding handler for data type ' + type(byte_obj))


def writesettings():
    settings['LastSave'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True, default=json_encoder)


def initialise():  # These are the default values written to the settings.json file the first time the app is run
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'gunicornpath': './logs/',
                 'ion-length': 16,
                 'ion-port': '/dev/ttyUSB2',
                 'ion-speed': 9600,
                 'ion-start': 9,
                 'ion-string1': b'~ 05 0B 00\r',
                 'logappname': 'Pumpreader-Py',
                 'logfilepath': './logs/pumpreader.log',
                 'pyro-laseroff':b'\xA5\x00\xA5',
                 'pyro-laseron': b'\xA5\x01\xA4',
                 'pyro-port': '/dev/ttyUSB3',
                 'pyro-speed': 115200,
                 'pyro-readlaser': b'\x25',
                 'pyro-readtemp': b'\x01',
                 'tank-length': 16,
                 'tank-port': '/dev/ttyUSB1',
                 'tank-speed': 9600,
                 'tank-start': 5,
                 'tank-string1': b'PR1\r',
                 'tank-string2': b'\x05',
                 'turbo-length': 16,
                 'turbo-port': '/dev/ttyUSB0',
                 'turbo-speed': 9600,
                 'turbo-start': 5,
                 'turbo-string1': b'PR1\r',
                 'turbo-string2': b'\x05'}
    return isettings

def readsettings():
    try:
        with open('settings.json') as json_file:
            jsettings = json.load(json_file)
            # decode the encoded values
            if 'ion-string1' in jsettings.keys() : jsettings['ion-string1'] = base64.b64decode(jsettings['ion-string1'])
            if 'pyro-laseroff' in jsettings.keys(): jsettings['pyro-laseroff'] = base64.b64decode(
                jsettings['pyro-laseroff'])
            if 'pyro-laseron' in jsettings.keys(): jsettings['pyro-laseron'] = base64.b64decode(
                jsettings['pyro-laseron'])
            if 'pyro-readlaser' in jsettings.keys(): jsettings['pyro-readlaser'] = base64.b64decode(
                jsettings['pyro-readlaser'])
            if 'pyro-readtemp' in jsettings.keys(): jsettings['pyro-readtemp'] = base64.b64decode(
                jsettings['pyro-readtemp'])
            if 'tank-string1' in jsettings.keys(): jsettings['tank-string1'] = base64.b64decode(
                jsettings['tank-string1'])
            if 'tank-string2' in jsettings.keys(): jsettings['tank-string2'] = base64.b64decode(
                jsettings['tank-string2'])
            if 'turbo-string1' in jsettings.keys(): jsettings['turbo-string1'] = base64.b64decode(
                jsettings['turbo-string1'])
            if 'turbo-string2' in jsettings.keys(): jsettings['turbo-string2'] = base64.b64decode(
                jsettings['turbo-string2'])
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}

def loadsettings():
    global settings
    settingschanged = 0
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            settingschanged = 1
    if settingschanged == 1:
        writesettings()


settings = initialise()
loadsettings()
