"""
Pump reader class, uses pyserial to read pressure gauges and pyrometer
"""
from time import sleep
import os
from threading import Timer
from base64 import b64decode
import serial  # from pyserial
import hid
from RPi import GPIO
from app_control import settings
from logmanager import logger



class PumpClass:
    """PumpClass: reads pressures from gauges via RS232 ports"""
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
        self.string1 = b64decode(string1)
        if string2 is None:
            self.string2 = None
        else:
            self.string2 = b64decode(string2)
        logger.info('Initialising %s pump on port %s', self.name, self.port.port)
        try:
            self.port.close()
            self.port.open()
            logger.info("%s port %s ok", self.name, self.port.port)
            self.portready = 1
            self.readtimer()
        except serial.serialutil.SerialException:
            logger.error("pumpClass error %s opening port %s", self.name, self.port.port)

    def readtimer(self):
        """regular timer, reads the gauges every 5 seconds"""
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
                logger.info('Pump Return "%s" from %s', self.value, self.name)
            else:
                self.value = 0
        except:
            logger.error('Pump Error on %s: %s' ,self.name, Exception )
            self.value = 0

    def read(self):
        """Return the gauge pressure"""
        if self.value == '':
            return 0
        try:
            return float(self.value)
        except:
            return 0


class PressureClass:
    """PressureClass: reads pressures from pressure transducer"""
    def __init__(self, name):
        self.conroller = name
        if self.conroller is not None:
            self.adc = AnalogIn(board.G1)
        else:

            self.adc = None

    def read(self):
        """Read the pressure from the MCP2221 chip"""
        if self.conroller is not None:
            raw= self.adc.value
            volts = (raw * 5.174) / 65536
            if volts <= settings['pressure-min-volt']:
                return settings['pressure-min-units']
            if volts >= settings['pressure-max-volt']:
                return settings['pressure-max-units']
            presurescaler = ((settings['pressure-max-units'] - settings['pressure-min-units']) /
                             (settings['pressure-max-volt'] - settings['pressure-min-volt']))
            return (volts - settings['pressure-min-volt']) * presurescaler
        return -1



def pressures():
    """API call: return all guage pressures as a json message"""
    pressure = [{'pump': 'turbo', 'pressure': turbopump.read()}, {'pump': 'tank', 'pressure': tankpump.read()},
                {'pump': 'ion', 'pressure': ionpump.read()}, {'pump': 'gas', 'pressure': gaspressure.read()},]
    return pressure


def httpstatus():
    """Web page info"""
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
    if gaspressure.read() == -1:
        gasvalue = 'Reader not connected'
    else:
        gasvalue = '%.2f' % gaspressure.read()
    return {'turbo': turbovalue, 'tank': tankvalue, 'ion': ionvalue, 'gas': gasvalue, 'gasunits': settings['pressure-units']}






logger.info("pump reader started")
os.environ[settings['pressure-env']] = "1"  # set an environment variable for the board we are using
device = hid.enumerate(settings['pressure-vendorid'], settings['pressure-productid'])
if device == []:
    logger.error('Gas Pressure Reader not connected')
    CONTROLLER = None
else:
    os.environ["BLINKA_MCP2221"] = "1"  # set an environment variable for the board we are using
    import board
    from analogio import AnalogIn
    CONTROLLER= board.board_id
    logger.info('Pressure reader device is %s', CONTROLLER)

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
gaspressure = PressureClass(CONTROLLER)
logger.info("Pump reader ready")
GPIO.output(12, 1)  # Set ready LED
