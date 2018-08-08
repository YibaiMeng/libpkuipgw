# libpkuipgw

A library for accessing the Internet through Peking University's Internet service. It only supports ESP32 and ESP8266 boards, due to the need for HTTPS. 

## Installing

Follow Arduino's instructions for installing libraries. 

## Usage

Initalize the client object. `mac` is the network interface's MAC address, formatted like "5C:CF:7F:08:11:17".
```
#include<IPGWClient.h>
IPGWClient clt(username, password, mac);
```
Call connect when connecting to the Internet.
```
clt.connect()
```
It will return `IPGW_SUCC` when successful.


