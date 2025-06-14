# RPi Pump Reader

## Overview
A Python application for monitoring Pfeiffer Vacuum gauges through an HTTP API interface. The system collects data from vacuum equipment using both CH-340 USB to RS232 adapters for serial communication and an MCP2221 USB analog-to-digital converter to read from pressure transducers.

## Features
- Real-time monitoring of vacuum and gas pressures
- HTTP API for remote access and control
- Support for CH-340 USB to RS232 serial communication
- Integration with MCP2221 for analog pressure transducer readings
- JSON-based command interface

## Hardware Requirements
- Pfeiffer Vacuum gauges
- CH-340 USB to RS232 adapters
- MCP2221 USB analog-to-digital converter
- Pressure transducer(s)
- Raspberry Pi 4b

## Documentation
- Detailed application documentation: [README.pdf](./README.pdf)
- Python module documentation: [Module Docs](./docs/readme.md)
- Change log: [changelog.txt](./changelog.txt)


### JSON Commands
 
`{'getpressures', 1}` Return the vacuum and gas pressures


&nbsp;   
&nbsp;    
&nbsp;  
&nbsp;   
&nbsp;   
&nbsp;   
--------------

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


Author:  Gary Twinn  
Repository:  [github.com/westerlymerlin](https://github)

-------------
