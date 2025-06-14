# None

<a id="pumpclass"></a>

# pumpclass

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

<a id="pumpclass.sleep"></a>

## sleep

<a id="pumpclass.os"></a>

## os

<a id="pumpclass.Timer"></a>

## Timer

<a id="pumpclass.b64decode"></a>

## b64decode

<a id="pumpclass.serial"></a>

## serial

<a id="pumpclass.hid"></a>

## hid

<a id="pumpclass.GPIO"></a>

## GPIO

<a id="pumpclass.settings"></a>

## settings

<a id="pumpclass.logger"></a>

## logger

<a id="pumpclass.PumpClass"></a>

## PumpClass Objects

```python
class PumpClass()
```

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

<a id="pumpclass.PumpClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name, port, speed, start, length, string1, string2=None)
```

<a id="pumpclass.PumpClass.serialreader"></a>

#### serialreader

```python
def serialreader()
```

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

<a id="pumpclass.PumpClass.read"></a>

#### read

```python
def read()
```

Return the gauge pressure

<a id="pumpclass.PressureClass"></a>

## PressureClass Objects

```python
class PressureClass()
```

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

<a id="pumpclass.PressureClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name)
```

<a id="pumpclass.PressureClass.read_adc"></a>

#### read\_adc

```python
def read_adc()
```

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

<a id="pumpclass.PressureClass.read"></a>

#### read

```python
def read()
```

Represents a method to read and return the value of a specific object attribute.

This method is used to access the `value` attribute of an object and return
its current state. It is intended to provide a simple interface for retrieving
an attribute value without directly accessing it.

Returns:
    Any: The current value of the `value` attribute of the object.

<a id="pumpclass.pressures"></a>

#### pressures

```python
def pressures()
```

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

<a id="pumpclass.httpstatus"></a>

#### httpstatus

```python
def httpstatus()
```

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

<a id="pumpclass.device"></a>

#### device

<a id="pumpclass.turbopump"></a>

#### turbopump

<a id="pumpclass.tankpump"></a>

#### tankpump

<a id="pumpclass.ionpump"></a>

#### ionpump

<a id="pumpclass.gaspressure"></a>

#### gaspressure

