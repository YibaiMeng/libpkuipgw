import requests

import time
import json
import os

class IPGWError(Exception):
    pass
class IPGWClient():
    def __init__(self, _username, _password, _mac=None):
        if not isinstance(_username, str) or not isinstance(_password, str):
            raise IPGWError("Wrong type for username and password!");
        self.username = _username
        self.password = _password
        self.url = 'https://its.pku.edu.cn/cas/ITSClient'
        self.is_connected = None
        self.ip = None
        self.balance = None
        self.last_check = None
        def get_mac():
            try:
                dirs = os.listdir("/sys/class/net/")
            except FileNotFoundError:
                raise IPGWError("Can't aquire your MAC address. Please input your MAC manually.")
            for path_ in dirs:
                if path_ == "lo":
                    continue
                is_up = open("/sys/class/net/"+path_+"/operstate").read()
                if is_up == "up\n": 
                    return open("/sys/class/net/"+path_+"/address").read()
                else:
                    continue
            raise IPGWError("Can't aquire your MAC address due to no useable network inteface. Please input your MAC manually.")
        if _mac is None:
            my_mac = get_mac().replace(":", "-").replace("\n", "")
        else:
            my_mac = _mac.replace(":", "-").replace("\n", "")
        self.headers = {'User-Agent': 'IPGWLinux1.1_Linux_' + my_mac, 'Host': 'its.pku.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding' : 'gzip'}
    def connect(self):
        payload = { 'cmd' : 'open', 'username': self.username, 'password': self.password, 'iprange' : 'free', 'ip': '', 'lang' : 'en', 'app': '1.0'}    
        r = requests.post(self.url, headers=self.headers, params=payload)
        ans = json.loads(r.text)
        if ans["succ"] == "":
            self.balance = ans["BALANCE_CN"]
            self.ip =  ans["IP"]
            self.is_connected = True
            self.last_check = time.time()
        else:
            self.is_connected = False
            raise IPGWError("Can't connect to Internet!")
    def disconnect(self, ip_=None):
        if ip_ is None:
            payload = { 'cmd' : 'close', 'lang' : 'en'} 
        else:
            payload = { 'cmd' : 'close', 'lang' : 'en', 'ip' : ip_}
        r = requests.post(self.url, headers=self.headers, params=payload)
        ans = json.loads(r.text)
        if ans["succ"] == "close_OK":
            self.ip =  None
            self.is_connected = False
            self.last_check = None
        else:
            if ip_ is None:
                raise IPGWError("Can't disconnect self!")
            else:
                raise IPGWError("Can't disconnect this IP address: ", ip_)
    def disconnect_all(self):
        payload = { 'cmd' : 'closeall', 'username': self.username, 'password': self.password, 'lang' : 'en'}
        r = requests.post(self.url, headers=self.headers, params=payload)
        ans = json.loads(r.text)
        if ans["succ"] == "close_OK":
            self.ip =  None
            self.is_connected = False
            self.last_check = None
        else:
            raise IPGWError("Can't disconnect all!")
    def get_connections(self):
        payload = { 'cmd' : 'getconnections', 'username': self.username, 'password': self.password, 'lang' : 'en'}
        r = requests.post(self.url, headers=self.headers, params=payload)
        ans = json.loads(r.text)    
        try:
            if ans["succ"] != "":
                tmp = ans["succ"].split(";")
                self.connections = list()
                for i in range(len(tmp)//4):
                    connection = dict()
                    connection["ip"] = tmp[4*i]
                    connection["location"] = tmp[4*i+2]
                    connection["login_time"] = tmp[4*i +3]
                    connection["login_time"] ="T".join(connection["login_time"].split(" "))+"+08" # Make the time ISO_8601 compliant. Needs further check to make sure it adheres to the corner cases.
                    self.connections.append(connection)
                    self.last_check = time.time
        except KeyError:
            raise IPGWError("Can't get connection info!")
        return self.connections
