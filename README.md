# Pump Reader

### Python project to read the Pfeiffer Vacuum gauges and a micro-epsilon infrared pyrometer. and is controlled via an HTTP API

It uses CH-340 USB to RS232 adapters for comms. 


`app.py`			    Flask application that manages the API 

----------------------------------------------------

`pumpclass.py`		reads the pumps connected to CH-340 USB to RS232 adapters

`README.pdf`		software description and details how to setup on a Raspberry Pi

### JSON Commands
 
`{'getpressures', 1}` Return the pump pressures

`{'gettemperature', 1}` Return the pyrometer temperature and maximum attained temperature

`{'resetmax', 1}` Reset the maximum pyrometer temperature reading

`{'laser', 'off'}` Switch off the rangefinder laser    

`{'laser', 'on'}` Switch on the rangefinder laser   
