# Stupid Python's package system...
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
import sys
sys.path.append("..")

import libpkuipgw

import json

# Logging facilities
import logging
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

with open("ipgw.cfg") as fp:
    account_data = json.load(fp)
cli = libpkuipgw.IPGWClient(account_data['username'], account_data["password"])
print("Trying to connect!")
cli.connect()
print("Connected!")
# To connect, call cli.connect()
# To disconnect this device, call cli.disconnect()
# To disconnect device with specific IP, make the call like cli.disconnect("10.2.111.111")
# To disconnect all devices, call cli.disconnect_all()
# To get all the connections available:
print(cli.get_connections())

