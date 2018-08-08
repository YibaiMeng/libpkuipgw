# libpkuipgw

A library for accessing the Internet through Peking University's Internet service.

## Installing

The recommanded way is to use pip to install
```bash
pip3 install --user libpkuipgw
```

## Usage
First initialize an `IPGWClient`object:
```
import libpkuipgw
cli = libpkuipgw.IPGWClient(username, password)
```
If you are on Windows or macOS, you'll need to manually provide your MAC address:
```
import libpkuipgw
cli = libpkuipgw.IPGWClient(username, password, MAC) # MAC is a string, formatted like 5C:CF:7F:08:11:17
```
This is because I haven't found a way of portablely getting the device's MAC address.

To connect to the Internet, call `cli.connect()`

To disconnect this device, call `cli.disconnect()`

To disconnect device with specific IP, make the call like `cli.disconnect("10.2.111.111")`

To disconnect all devices, call `cli.disconnect_all()`

To get all the connections available: `cli.get_connections()`. Returns a list:
```python
[{'ip': '10.2.111.111', 'location': '22楼', 'login_time': '2018-08-08T22:22:22+08'}, {'ip': '10.2.222.222', 'location': '33楼', 'login_time': '2018-08-08T11:11:11+08'}]
```
The time format is ISO8601 complient.

# Error Handling

Apart from `get_connections`, returns nothing when everything is allright. If error occurs, an `IPGWError` would be raised. 

