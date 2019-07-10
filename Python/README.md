# libpkuipgw

A library for accessing the Internet through Peking University's Internet service.

## Installing

The recommended way is to use pip to install
```bash
pip3 install --user libpkuipgw
```

## Usage
First, initialize an `IPGWClient`object:
```
import libpkuipgw
cli = libpkuipgw.IPGWClient(username, password)
```

To connect to the Internet, call `cli.connect()`

To check connectivity to the Internet, call `cli.check_connectivity()`

To disconnect this device, call `cli.disconnect()`

To disconnect device with specific IP, make the call like `cli.disconnect("10.2.111.111")`

To disconnect all devices, call `cli.disconnect_all()`

To get all the connections available: `cli.get_connections()`

All operations returns `IPGWStatus` objects. For example, for `get_connections`:
```python
$ res = cli.get_connections()
$ res
libpkuipgw.IPGWStatus(operation="list", status="success", description="", data=[{'ip': '10.2.111.111', 'location': '22楼', 'login_time': '2018-08-08T22:22:22+08'}, {'ip': '10.2.222.222', 'location': '33楼', 'login_time': '2018-08-08T11:11:11+08'}])
```
The time format is ISO8601 compliant.

If something goes wrong, returns a status of "error".
