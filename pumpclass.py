import serial
from RPi import GPIO
from time import sleep
from settings import version, settings
from logmanager import *
from threading import Timer





class PumpClass:
    def __init__(self, config):
        self.port = serial.Serial()
        self.port.port = config['port']
        self.port.baudrate = config['speed']
        self.start = config['start']
        self.length = config['length']
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.bytesize = serial.EIGHTBITS
        # self.port.set_buffer_size(4096, 4096)
        self.port.timeout = 1
        self.value = 0
        self.portready = 0
        self.string1 = config['string1']
        if len(config) > 5:
            self.string2 = config['string2']
        else:
            self.string2 = None
        print('Initialising pump on port %s' % self.port.port)
        try:
            self.port.close()
            self.port.open()
            print("port %s ok" % self.port.port)
            self.portready = 1
            self.readtimer()
        except serial.serialutil.SerialException:
            print("pumpClass error opening port %s" % self.port.port)

    def readtimer(self):
        if self.portready == 1:
            timerthread = Timer(5, self.readtimer)
            timerthread.start()
            self.port.write(self.string1)
            sleep(0.5)
            if self.string2:
                self.port.write(self.string2)
            databack = self.port.read(size=100)
            self.value = str(databack, 'utf-8')[self.start:self.length]
            #print('Pump Return "%s" from %s' % (self.value, self.port.port))
        else:
            self.value = 0

    def read(self):
        if self.value == '':
            return 0
        else:
            try:
                return float(self.value)
            except:
                return 0

class PyroClass:
    def __init__(self, config):
        self.port = serial.Serial()
        self.port.port = config['port']
        self.port.baudrate = config['speed']
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.bytesize = serial.EIGHTBITS
        # self.port.set_buffer_size(4096, 4096)
        self.port.timeout = 1
        self.value = 0
        self.laser = 0
        self.portready = 0
        self.readtemp = config['readtemp']
        self.readlaser = config['readlaser']
        self.laser_on = config['laseron']
        self.laser_off = config['laserof' \
                              'f']
        print('Initialising pump on port %s' % self.port.port)
        try:
            self.port.close()
            self.port.open()
            print("port %s ok" % self.port.port)
            self.portready = 1
            self.readtimer()
        except serial.serialutil.SerialException:
            print("pumpClass error opening port %s" % self.port.port)

    def readtimer(self):
        if self.portready == 1:
            timerthread = Timer(5, self.readtimer)
            timerthread.start()
            self.port.write(self.readtemp)
            databack = self.port.read(size=100)
            print('Databack=*%s*' % databack)
            if databack == b'':
                self.value = 0
                self.laser = 0
            else:
                self.value = ((databack[0] * 256 + databack[1])-1000)/10
                self.port.write(self.readlaser)
                databack = self.port.read(size=100)
                self.laser = databack[0]
            #print('Pump Return "%s" from %s' % (self.value, self.port.port))
        else:
            self.value = 0

    def laseron(self):
        if self.portready == 1:
            self.port.write(self.laser_on)
            databack = self.port.read(size=100)
            self.laser = 1
            laserthread = Timer(60, self.laseroff)
            laserthread.start()

    def laseroff(self):
        if self.portready == 1:
            self.port.write(self.laser_off)
            databack = self.port.read(size=100)
            self.laser = 0


    def read(self):
        if self.value == 385.0:
            return 0.1
        else:
            return self.value


def pressures():
    pressure = [{'pump': 'turbo', 'pressure': turbopump.read()}, {'pump': 'tank', 'pressure': tankpump.read()},
                {'pump': 'ion', 'pressure': ionpump.read()}]
    return pressure


def temperature():
    return {'temperature': pyrometer.read(),'laser':pyrometer.laser}


def httpstatus():
    if turbopump.portready == 0:
        turbovalue = 'Port not available'
    elif turbopump.value == '':
        turbovalue = 'Pump not connected'
    else:
        turbovalue = turbopump.value
    if tankpump.portready == 0:
        tankvalue = 'Port not available'
    elif tankpump.value == '':
        tankvalue = 'Pump not connected'
    else:
        tankvalue = tankpump.value
    if ionpump.portready == 0:
        ionvalue = 'Port not available'
    elif ionpump.value == '':
        ionvalue = 'Pump not connected'
    else:
        ionvalue = ionpump.value
    if pyrometer.portready == 0:
        pyrovalue = 'Port not available'
        pyrolaser = 'Port not available'
    elif pyrometer.value == 0:
        pyrovalue = 'Pyrometer not connected'
        pyrolaser = 'Pyrometer not connected'
    else:
        pyrovalue = pyrometer.value
        pyrolaser = pyrometer.laser
    return {'turbo': turbovalue, 'tank': tankvalue, 'ion': ionvalue, 'temperature': pyrovalue, 'pyrolaser':pyrolaser}


print("pump reader started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, 0)
turbopump = PumpClass(settings['turbo'])
tankpump = PumpClass(settings['tank'])
ionpump = PumpClass(settings['ion'])
pyrometer = PyroClass(settings['pyro'])
print('Running version %s' % version)
print("pump reader ready")
GPIO.output(12, 1)  # Set ready LED
