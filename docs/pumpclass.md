# Contents for: pumpclass

* [pumpclass](#pumpclass)
  * [sleep](#pumpclass.sleep)
  * [os](#pumpclass.os)
  * [Timer](#pumpclass.Timer)
  * [b64decode](#pumpclass.b64decode)
  * [serial](#pumpclass.serial)
  * [hid](#pumpclass.hid)
  * [GPIO](#pumpclass.GPIO)
  * [settings](#pumpclass.settings)
  * [logger](#pumpclass.logger)
  * [PumpClass](#pumpclass.PumpClass)
    * [\_\_init\_\_](#pumpclass.PumpClass.__init__)
    * [serialreader](#pumpclass.PumpClass.serialreader)
    * [read](#pumpclass.PumpClass.read)
  * [PressureClass](#pumpclass.PressureClass)
    * [\_\_init\_\_](#pumpclass.PressureClass.__init__)
    * [read\_adc](#pumpclass.PressureClass.read_adc)
    * [read](#pumpclass.PressureClass.read)
  * [pressures](#pumpclass.pressures)
  * [httpstatus](#pumpclass.httpstatus)
  * [device](#pumpclass.device)
  * [turbopump](#pumpclass.turbopump)
  * [tankpump](#pumpclass.tankpump)
  * [ionpump](#pumpclass.ionpump)
  * [gaspressure](#pumpclass.gaspressure)

<a id="pumpclass"></a>

# pumpclass

Pump reader class, uses pyserial to read pressure gauges and pyrometer

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

PumpClass: reads pressures from gauges via RS232 ports

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

Reads the serial port

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

PressureClass: reads pressures from pressure transducer

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

regular reader, reads the gauge every 5 seconds

<a id="pumpclass.PressureClass.read"></a>

#### read

```python
def read()
```

Return the pressure from the MCP2221 chip

<a id="pumpclass.pressures"></a>

#### pressures

```python
def pressures()
```

API call: return all guage pressures as a json message

<a id="pumpclass.httpstatus"></a>

#### httpstatus

```python
def httpstatus()
```

Web page info

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

