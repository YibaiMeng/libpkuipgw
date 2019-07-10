import json
import os
import time
import logging
import random
import collections

import requests
import netifaces # Check available interface. Do not want to throw cryptic errors when the WiFi is not on.

class IPGWError(Exception):
    pass

# A class for indicating the result of each operation.
IPGWStatus = collections.namedtuple('IPGWStatus', ['operation', 'status', 'description','data'])
IPGWStatus.__new__.__defaults__ = (None, None, None, None) # For Python 3.6 compatibility https://stackoverflow.com/questions/11351032/namedtuple-and-default-values-for-optional-keyword-arguments
IPGWStatus.__bool__ = lambda x : x.status == "success"

class IPGWClient():
    def __init__(self, _username, _password, _mac=None):
        print("Shit")
        if not isinstance(_username, str) or not isinstance(_password, str):
            raise IPGWError("Wrong type for username and password!");
        self.username = _username
        self.password = _password
        self.url = 'https://its.pku.edu.cn/cas/ITSClient'
        self.is_connected = None
        self.ip = None
        self.balance = None
        self.last_check = None
        self.headers = {'User-Agent': 'IPGWLinux1.1_Linux_', 'Host': 'its.pku.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding' : 'gzip'} # User-Agent is NOT complete! need appending MAC!
    def check_interface(self):
        gateways = netifaces.gateways()    
        if not netifaces.AF_INET in gateways:
            logging.info("No available gateways for IPv4.") 
            return IPGWStatus(operation="Check interface", status="error", description="No available gateways for IPv4.")
        inet_if = gateways[netifaces.AF_INET]
        mac = None
        for i in inet_if:
            if i[2]:
                logging.debug("Gateway %s is available for IPv4 connections." % (str(i),))
                for link_if in  netifaces.ifaddresses(i[1])[netifaces.AF_LINK]: # Should only have one for most reasonable setups……     
                    logging.debug("Checking link layer information for interface %s." % (i[1],)) 
                    if "addr" in link_if:
                        mac = link_if["addr"]   
                        logging.debug("MAC addr %s found for interface %s." % (mac, i[1])) 
                        break
            if not mac:
                logging.info("Interfaces exist for IPv4, but none serves as the default gateway, or none has mac address. Check your routing setup.")
            self.mac = mac 
            if self.mac: 
                self.headers["User-Agent"] +=  mac.replace(":", "-").replace("\n", "")
            return IPGWStatus(operation="Check interface", status="success" if self.mac else "error", description="Interfaces exist for IPv4, but none serves as the default gateway, or none has mac address. Check your routing setup.", data=self.mac)
            
    def connect(self):
        payload = { 'cmd' : 'open', 'username': self.username, 'password': self.password, 'iprange' : 'free', 'ip': '', 'lang' : 'en', 'app': '1.0'}
        try:    
            r = requests.post(self.url, headers=self.headers, params=payload,timeout=5)
            ans = json.loads(r.text)
        except requests.exceptions.RequestException as e:
            return IPGWStatus(operation="connect", status="error", description="PKU ITS server error")
        except json.decoder.JSONDecodeError:
            return IPGWStatus(operation="connect", status="error", description="PKU ITS server error")
        if "succ" in ans and ans["succ"] == "":
            self.balance = ans["BALANCE_CN"]
            self.ip =  ans["IP"]
            self.is_connected = True
            self.last_check = time.time()
            return IPGWStatus(operation="connect", status="success")
        else:
            self.is_connected = False
            if "error" in ans:
                return IPGWStatus(operation="connect", status="error", description=ans["error"])
            return IPGWStatus(operation="connect", status="error", description="unknown")
    def disconnect(self, ip_=None):
        if ip_ is None:
            payload = { 'cmd' : 'close', 'lang' : 'en'} 
        else:
            payload = { 'cmd' : 'close', 'lang' : 'en', 'ip' : ip_}
        try:
            r = requests.post(self.url, headers=self.headers, params=payload)
            ans = json.loads(r.text)
        except requests.exceptions.RequestException as e:
            return IPGWStatus(operation="disconnect", status="error", description="PKU ITS server error")
        except json.decoder.JSONDecodeError:
            return IPGWStatus(operation="disconnect", status="error", description="PKU ITS server error")
        if "succ" in ans and ans["succ"] == "close_OK":
            self.ip =  None
            self.is_connected = False
            self.last_check = None
            return IPGWStatus(operation="disconnect", status="success")
        else:
            if "error" in ans:
                return IPGWStatus(operation="disconnect", status="error", description=ans["error"])
            return IPGWStatus(operation="disconnect", status="error", description="unknown")
    def disconnect_all(self):
        payload = { 'cmd' : 'closeall', 'username': self.username, 'password': self.password, 'lang' : 'en'}
        try:
            r = requests.post(self.url, headers=self.headers, params=payload)
            ans = json.loads(r.text)
        except requests.exceptions.RequestException as e:
            return IPGWStatus(operation="disconnect_all", status="error", description="PKU ITS server error")
        except json.decoder.JSONDecodeError:
            return IPGWStatus(operation="disconnect_all", status="error", description="PKU ITS server error")
        if "succ" in ans and ans["succ"] == "close_OK":
            self.ip =  None
            self.is_connected = False
            self.last_check = None
            return IPGWStatus(operation="disconnect_all ", status="success")
        else:
            if "error" in ans:
                return IPGWStatus(operation="disconnect_all", status="error", description=ans["error"])
            return IPGWStatus(operation="disconnect_all", status="error", description="unknown")
    def get_connections(self):
        payload = { 'cmd' : 'getconnections', 'username': self.username, 'password': self.password, 'lang' : 'en'}
        try:
            r = requests.post(self.url, headers=self.headers, params=payload)
            ans = json.loads(r.text)    
        except requests.exceptions.RequestException as e:
            return IPGWStatus(operation="get_connections", status="error", description="PKU ITS server error")
        except json.decoder.JSONDecodeError:
            return IPGWStatus(operation="get_connections", status="error", description="PKU ITS server error")
        if "succ" in ans and ans["succ"] != "":
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
                return IPGWStatus(operation="get_connections", status="success", data=self.connections)
        else:   
            if "error" in ans:
                return IPGWStatus(operation="get_connections", status="error", description=ans["error"])
            return IPGWStatus(operation="get_connections", status="error", description="unknown")
        
    def check_connectivity(self):   
        captive_portal_servers = ["https://http204.sinaapp.com/generate_204", "https://captive.v2ex.co/generate_204", "https://connect.rom.miui.com/generate_204", "https://noisyfox.cn/generate_204", "https://www.qualcomm.cn/generate_204"]
        random.shuffle(captive_portal_servers)
        try:
            r = requests.get(captive_portal_servers[0], timeout=5, headers={"User-Agent" : "libpkuipgw"})
            if r.status_code == 204:
                return IPGWStatus(operation="check_connectivity", status="success")
            else:
                logging.info("Request to %s returned with status code %i and headers %s." % (captive_portal_servers[0], r.status_code, str(r.headers))) 
        except requests.exceptions.RequestException as e:
            logging.info("Request error %s", e)
            pass
        try:
            r = requests.get(captive_portal_servers[1], timeout=5, headers={"User-Agent" : "libpkuipgw"})
            if r.status_code == 204:
                return IPGWStatus(operation="check_connectivity", status="success")
            else:
                logging.info("Request to %s returned with status code %i and headers %s." % (captive_portal_servers[0], r.status_code, str(r.headers))) 
        except requests.exceptions.RequestException as e:
            logging.info("Request error %s", e)
            pass
        return IPGWStatus(operation="check_connectivity", status="error", description="Can't connect to the Internet after two tries")
