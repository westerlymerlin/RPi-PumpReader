# Pump Reader

### Python project to read the Pfeiffer Vacuum gauges and is controlled via an HTTP API

It uses CH-340 USB to RS232 adapters for Serial comms and a MCP2221 usb analog to digital convertor to read froma pressure transducer.



`app.py`			    Flask application that manages the API 

----------------------------------------------------

`pumpclass.py`		reads the pumps connected to CH-340 USB to RS232 adapters

`README.pdf`		software description and details how to setup on a Raspberry Pi

### JSON Commands
 
`{'getpressures', 1}` Return the vaccum and gas pressures

 

