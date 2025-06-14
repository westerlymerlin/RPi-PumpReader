"""
    A class to communicate with and read pressure data from gauges via RS232 serial connections.

    This class establishes a serial connection to pressure measurement devices, sends
    command strings to request data, and processes the responses to extract pressure values.
    It manages the continuous reading of pressure data in a separate thread.

    Parameters
    ----------
    name : str
        Identifier for the pump/gauge, used in logging.
    port : str
        Serial port identifier (e.g., '/dev/ttyUSB0', 'COM1').
    speed : int
        Baud rate for the serial connection.
    start : int
        Starting position for extracting pressure value from response string.
    length : int
        Ending position for extracting pressure value from response string.
    string1 : str
        Base64-encoded primary command string to send to the device.
    string2 : str, optional
        Base64-encoded secondary command string to send to the device (default: None).

    Attributes
    ----------
    value : float or int
        The most recently read pressure value.
    portready : int
        Status of port connection (1 = ready, 0 = not connected).
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
    """
    Represents a pump device with serial communication capabilities.

    This class handles the initialization, communication, and data reading
    from a pump using a serial port. It manages the configuration of the
    serial port, starts a timer for periodic serial data reads, and
    processes the data returned by the pump. It is primarily used for
    monitoring and retrieving pressure data from the pump.

    Attributes:
        name (str): The name of the pump.
        port (serial.Serial): The serial port object configured for pump communication.
        start (int): The starting index for slicing the serial data received.
        length (int): The length of the substring to extract from the received data.
        value (str): The last read value from the pump's serial port.
        portready (int): Status indicator whether the port has been initialized and opened.
        string1 (bytes): The primary string to be sent to the pump.
        string2 (Optional[bytes]): The secondary string to be sent to the pump if provided.

    """
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
            timerthread = Timer(1, self.serialreader)
            timerthread.name = self.name
            timerthread.start()
        except serial.serialutil.SerialException:
            logger.error("pumpClass error %s opening port %s", self.name, self.port.port)

    def serialreader(self):
        """
        A method to manage serial communication with a hardware pump. This method handles
        writing to the port, reading responses, and processing the response data. It also logs
        errors if exceptions are encountered during the communication process.

        Yields no explicit return but continuously updates the attribute `self.value` with the
        processed response from the serial port or sets it to 0 in case of an error or
        unavailability of the port.

        Raises
        ------
        Exception
            Logs and handles any exceptions that occur during the serial port communication,
            ensuring that the method continues operation without halting unexpectedly.
        """
        while True:
            try:
                if self.portready == 1:
                    self.port.write(self.string1)
                    sleep(0.5)
                    if self.string2:
                        self.port.write(self.string2)
                    databack = self.port.read(size=100)
                    self.value = str(databack, 'utf-8')[self.start:self.length]
                    logger.debug('Pump Return "%s" from %s', self.value, self.name)
                else:
                    self.value = 0
            except:
                logger.exception('Pump Error on %s: %s', self.name, Exception)
                self.value = 0
            sleep(5)

    def read(self):
        """Return the gauge pressure"""
        if self.value == '':
            return 0
        try:
            return float(self.value)
        except:
            return 0


class PressureClass:
    """
    Represents a pressure monitoring system utilizing analog-to-digital conversion.

    This class is designed to measure and manage pressure readings using an ADC input from a
    specified analog pin. A periodic reading mechanism is implemented to automatically update
    pressure values. The pressure values are scaled based on configurable voltage and pressure
    limits. It handles scenarios where the controller is not provided by assigning default
    values.

    Attributes:
        conroller: str
            The name or identifier of the associated controller.
        value: float
            The current pressure value calculated from the analog input.
        adc: AnalogIn or None
            The analog input channel instance from which pressure readings are derived.
    """
    def __init__(self, name):
        self.conroller = name
        self.value = 0
        if self.conroller is not None:
            self.adc = AnalogIn(board.G1)
        else:
            self.adc = None
        timerthread = Timer(1, self.read_adc)
        timerthread.name = 'N2 Reader'
        timerthread.start()


    def read_adc(self):
        """
        Reads data from the ADC (Analog-to-Digital Converter) and calculates the corresponding
        pressure value in specified units. Continuously loops to fetch and process ADC readings.
        Adjusts pressure value based on configured minimum and maximum voltage-to-pressure
        mappings. Introduces a delay in each iteration to ensure periodicity in reading.

        Raises:
            None

        Args:
            None

        Returns:
            None
        """
        while True:
            if self.conroller is not None:
                raw = self.adc.value
                volts = (raw * 5.174) / 65536
                logger.debug('voltage is %s', volts)
                if volts <= settings['pressure-min-volt']:
                    self.value = settings['pressure-min-units']
                if volts >= settings['pressure-max-volt']:
                    self.value = settings['pressure-max-units']
                presurescaler = ((settings['pressure-max-units'] - settings['pressure-min-units']) /
                                 (settings['pressure-max-volt'] - settings['pressure-min-volt']))
                self.value = ((volts - settings['pressure-min-volt']) * presurescaler) + settings['pressure-min-units']
                self.value = round(self.value * 4, 0) / 4
            else:
                self.value = 1000
            sleep(5)

    def read(self):
        """
        Represents a method to read and return the value of a specific object attribute.

        This method is used to access the `value` attribute of an object and return
        its current state. It is intended to provide a simple interface for retrieving
        an attribute value without directly accessing it.

        Returns:
            Any: The current value of the `value` attribute of the object.
        """
        return self.value


def pressures():
    """
    Reads and returns the current pressure readings for multiple pumps in a standardized
    format. Each pump is associated with its pressure value and measurement units
    as defined in the settings. This function aggregates the readings from all the
    pumps and prepares them for further usage or monitoring.

    Return:
        list of dict: A list of dictionaries where each dictionary contains the
        following keys:
            - pump (str): The name of the pump ('turbo', 'tank', 'ion', or 'gas').
            - pressure: The current pressure reading from the pump. Type depends on
              implementation of the corresponding pump's read method.
            - units (str): The measurement units for the corresponding pump pressure.

    Raises:
        KeyError: If the required settings keys ('turbo-units', 'tank-units',
        'ion-units', 'pressure-units') are not present in the settings dictionary.
    """
    pressure = [{'pump': 'turbo', 'pressure': turbopump.read(), 'units': settings['turbo-units']},
                {'pump': 'tank', 'pressure': tankpump.read(), 'units': settings['tank-units']},
                {'pump': 'ion', 'pressure': ionpump.read(), 'units': settings['ion-units']},
                {'pump': 'gas', 'pressure': gaspressure.read(), 'units': settings['pressure-units']}]
    return pressure


def httpstatus():
    """
    Determines the operational status of various pumps and a gas pressure reader,
    and returns their statuses along with associated measurement units.

    The function checks the states of three pumps: turbopump, tankpump, and ionpump,
    as well as a gas pressure measurement reader. Each pump's status is determined
    based on its port's readiness and current value. The gas pressure reader's
    status is evaluated based on its reading. The output is a dictionary containing
    the status of each component along with their respective measurement units,
    as retrieved from the settings.

    Returns:
        dict: A dictionary containing the following keys:
            - turbo: The status of the turbopump.
            - turbounits: The measurement units for the turbopump status.
            - tank: The status of the tank pump.
            - tankunits: The measurement units for the tank pump status.
            - ion: The status of the ion pump.
            - ionunits: The measurement units for the ion pump status.
            - gas: The gas pressure read by the reader.
            - gasunits: The measurement units for the gas pressure.

    Raises:
        None
    """
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
    if gaspressure.read() == 1000:
        gasvalue = 'Reader not connected'
    else:
        gasvalue = '%.2f' % gaspressure.read()
    return {'turbo': turbovalue, 'turbounits': settings['turbo-units'], 'tank': tankvalue,
            'tankunits': settings['tank-units'], 'ion': ionvalue, 'ionunits': settings['ion-units'],
            'gas': gasvalue, 'gasunits': settings['pressure-units']}


logger.info("pump reader started")
os.environ[settings['pressure-env']] = "1"  # set an environment variable for the board we are using
device = hid.enumerate(settings['pressure-vendorid'], settings['pressure-productid'])
if not device:
    logger.error('Gas Pressure Reader not connected')
    CONTROLLER = None
else:
    os.environ["BLINKA_MCP2221"] = "1"  # set an environment variable for the board we are using
    import board
    from analogio import AnalogIn
    CONTROLLER = board.board_id
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
