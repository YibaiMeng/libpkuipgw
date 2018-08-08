# Half finished experiment for Web API. 
import requests
import time
import json
import account

class Web(account.Account):
    def __init__(self):
        account.Account.__init__(self)
        self.url = 'https://its.pku.edu.cn/cas/webLogin'
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", 'Host': 'its.pku.edu.cn', 'Origin': 'https://its.pku.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding' : 'gzip, deflate, br'}
    def connect(self):
        payload = { 'cmd' : 'select', 'username': self.username, 'password': self.password, 'iprange' : 'no'}
        r = requests.post(self.url, headers=self.headers, params=payload, allow_redirects=False)
        ans = r.text
        self.cookies =  r.cookies
        #print(r.cookies["authUser"])
        print(self.cookies.items())
        new_header = self.headers
        new_header["Referer"] = "https://its.pku.edu.cn/netportal/myits.jsp"
        import random
        pld = {"cmd":"getconnections", "sid": random.randint(200,300)}
        r = requests.post("https://its.pku.edu.cn/netportal/ipgwConns.jsp", headers=new_header, params=pld, cookies=self.cookies)
        print(r.text)

        '''
        if ans["succ"] == "":
            self.balance = ans["BALANCE_CN"]
            self.ip =  ans["IP"]
            self.is_connected = True
            self.last_check = time.time()
        else:
            self.is_connected = False
        print(self.ip, self.balance)
        '''
