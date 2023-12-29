import serial
from time import sleep
from threading import Timer
from RPi import GPIO
from settings import version, settings
from logmanager import logger



class PumpClass:
    def __init__(self, name, port, speed, start, length, string1, string2=None):
        self.name = name
        self.port = serial.Serial()
        self.port.port = port
        self.port.baudrate = speed
        self.start = start
        self.length = length
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.bytesize = serial.EIGHTBITS
        # self.port.set_buffer_size(4096, 4096)
        self.port.timeout = 1
        self.value = 0

        self.portready = 0
        self.string1 = string1
        self.string2 = string2
        logger.info('Initialising %s pump on port %s' % (self.name, self.port.port))
        try:
            self.port.close()
            self.port.open()
            logger.info("%s port %s ok" % (self.name, self.port.port))
            self.portready = 1
            self.readtimer()
        except serial.serialutil.SerialException:
            logger.error("pumpClass error %s opening port %s" % (self.name, self.port.port))

    def readtimer(self):
        try:
            if self.portready == 1:
                timerthread = Timer(5, self.readtimer)
                timerthread.start()
                self.port.write(self.string1)
                sleep(0.5)
                if self.string2:
                    self.port.write(self.string2)
                databack = self.port.read(size=100)
                self.value = str(databack, 'utf-8')[self.start:self.length]
                logger.info('Pump Return "%s" from %s' % (self.value, self.name))
            else:
                self.value = 0
        except:
            logger.error('Pump Error on %s: %s' % (self.name, Exception ))
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
    def __init__(self, port, speed, readtemp, readlaser, laseron, laseroff):
        self.port = serial.Serial()
        self.port.port = port
        self.port.baudrate = speed
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.bytesize = serial.EIGHTBITS
        # self.port.set_buffer_size(4096, 4096)
        self.port.timeout = 1
        self.value = 0
        self.laser = 0
        self.maxtemp = 0
        self.portready = 0
        self.readtemp = readtemp
        self.readlaser = readlaser
        self.laser_on = laseron
        self.laser_off = laseroff
        logger.info('Initialising pyrometer on port %s' % self.port.port)
        try:
            self.port.close()
            self.port.open()
            logger.info("pyrometer port %s ok" % self.port.port)
            self.portready = 1
            self.readtimer()
        except serial.serialutil.SerialException:
            logger.error("PyroClass error opening port %s" % self.port.port)

    def readtimer(self):
        if self.portready == 1:
            timerthread = Timer(5, self.readtimer)
            timerthread.start()
            self.port.write(self.readtemp)
            databack = self.port.read(size=100)
            if databack == b'':
                self.value = 0
                self.laser = 0
            else:
                self.value = ((databack[0] * 256 + databack[1])-1000)/10
                logger.info('Pyrometer value = %s' % self.value)
                if self.maxtemp < self.value:
                    self.maxtemp = self.value
                self.port.write(self.readlaser)
                databack = self.port.read(size=100)
                self.laser = databack[0]
        else:
            self.value = 0

    def resetmax(self):
        self.maxtemp = 0

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

    def readmax(self):
        return self.maxtemp

    def read(self):
        return self.value


def pressures():
    pressure = [{'pump': 'turbo', 'pressure': turbopump.read()}, {'pump': 'tank', 'pressure': tankpump.read()},
                {'pump': 'ion', 'pressure': ionpump.read()}]
    return pressure


def temperature():
    return {'temperature': pyrometer.read(), 'laser': pyrometer.laser, 'maxtemp': pyrometer.readmax()}


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
        pyromax = 'Port not available'
    elif pyrometer.value == 0:
        pyrovalue = 'Pyrometer not connected'
        pyrolaser = 'Pyrometer not connected'
        pyromax = 'Pyrometer not connected'
    else:
        pyrovalue = pyrometer.value
        pyrolaser = pyrometer.laser
        pyromax = pyrometer.maxtemp
    return {'turbo': turbovalue, 'tank': tankvalue, 'ion': ionvalue,
            'temperature': pyrovalue, 'pyrolaser': pyrolaser, 'maxtemperature': pyromax}


logger.info("pump reader started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, 0)
turbopump = PumpClass('Turbo Pump', settings['turbo-port'], settings['turbo-speed'], settings['turbo-start'],
                      settings['turbo-length'], settings['turbo-string1'], settings['turbo-string2'])
tankpump = PumpClass('Tank Pump', settings['tank-port'], settings['tank-speed'], settings['tank-start'],
                      settings['tank-length'], settings['tank-string1'], settings['tank-string2'])
ionpump = PumpClass('Ion Pump', settings['ion-port'], settings['ion-speed'], settings['ion-start'],
                      settings['ion-length'], settings['ion-string1'])
pyrometer = PyroClass(settings['pyro-port'], settings['pyro-speed'],settings['pyro-readtemp'],
                      settings['pyro-readlaser'],settings['pyro-laseron'], settings['pyro-laseroff'])
logger.info('Running version %s' % version)
logger.info("Pump reader ready")
GPIO.output(12, 1)  # Set ready LED
