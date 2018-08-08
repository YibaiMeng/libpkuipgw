# libpkuipgw
A library for accessing the Internet through Peking University's Internet service.

## Overview
All users of Peking University's Internet service need to authenticate when attempting to access out of campus resources. The user can either visit the website `its.pku.edu.cn` or use a variety of official clients.

However, there's no official API to automate these activities, making it very difficult to connect a Raspberry Pi or an ESP32 to the school's network. Furthermore, the standard APIs are large and cumbersome and have potential security problems (the Windows client require Administrator privileges!). It would be great if there were a library for such actions. 

Thankfully, the APIs are pretty straightforward to reimplement. So I have implemented:
- `connect`: Authenticate and gain Internet access.
- `close` & `close_all`: Close access to the Internet.
- `get_connections`: Get connection information under the same account.
The other functionalities are not frequently used and are better left to the Web interface

Now I can connect my ESP32 or Raspberry Pi to Wireless PKU, or have my Ubuntu automatically connect to school network upon startup. How wonderful!

## Languages Implemented
The different implementations are listed here. Perhaps I'll expand this library to more languages and platforms if I have time:
- [Python](Python/README.md)
- [Arduino ESP32](arduino-esp32/README.md)
- ESP32: TODO. Developing ESP32 using ESP-IDF is really frustrating.
- Shell: TODO
- Java or Kotlin if I'm really bored

## Usage
To be continued...
