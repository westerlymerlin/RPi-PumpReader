# Pump Reader

### Python project to read the Pfeiffer Vacuum gauges and is controlled via an HTTP API

It uses CH-340 USB to RS232 adapters for Serial comms and a MCP2221 usb analog to digital convertor to read froma pressure transducer.



Application dcumentaton can be found in [readme.pdf](./README.pdf)

Python module documentation can be found in the folder: [docs](./docs/readme.md)

Change log can be found in the file [changelog.txt](./changelog.txt)


### JSON Commands
 
`{'getpressures', 1}` Return the vaccum and gas pressures

 

