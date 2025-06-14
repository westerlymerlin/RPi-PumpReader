# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[app](./app.md)  
Pump Reader Web Application

This Flask application serves as a web interface for monitoring and controlling
a pump system. It provides:

- A web dashboard showing real-time pump pressure readings and system status
- REST API endpoints for programmatic access to pump data and control functions
- System monitoring capabilities including CPU temperature and log viewing
- Remote system control functions (restart)

The application is designed to run on a Raspberry Pi using Gunicorn as the WSGI server.

Usage:
    - Run directly: python app.py (development)
    - Run with Gunicorn: gunicorn app:app (production)

Configuration is loaded from app_control.settings

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.

[pumpclass](./pumpclass.md)  
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


---


  
-------
#### Copyright (C) 2025 Gary Twinn  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.  
  
  ##### Author: Gary Twinn  
  
 -------------
  
