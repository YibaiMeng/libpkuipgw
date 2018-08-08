/*
    A small library for accessing the Internet through Peking University's Interent service.
    If you don't know what that is, then you probably won't need it.
    Only support ESP32 and ESP8266 at the moment.
*/
#ifndef IPGWClient_H
#define IPGWClient_H

//If in need of the debug outputs, uncomment the following line:
//#define IPGW_DEBUG_ENABLE   

//TODO: Problems with this, DON't uncomment!
//If you want to check the certificate of its.pku.edu.cn, uncomment the following line.
//#define IPGW_CHECK_CERT

#if defined(ESP8266) || defined(ESP32)
    #include <WiFiClientSecure.h>
#else
    #error “Currently this library only supports ESP32 and ESP8266 boards, due to the need for SSL/TLS communication.”
#endif

#ifdef IPGW_DEBUG_ENABLE
 #define IPGW_DEBUG(x)  Serial.println(x)
#else
 #define IPGW_DEBUG(x)
#endif

enum IPGWStatus {
        IPGW_SUCC, IPGW_NO_CONN, IPGW_CERT_ERR, IPGW_PWD_ERR, IPGW_GENERAL_ERR
};

class IPGWClient {
  public:
    IPGWClient(const String username, const String password, const String mac);
    IPGWStatus connect();
  private:
    WiFiClientSecure client;
    String host = "its.pku.edu.cn";
    // Fingerprint for https://its.pku.edu.cn as of 2018-08-06. Will expire on December 2018.
    //TODO: Fingerprint doesn't match. Trying to understand why.
    String fingerprint = "81 75 82 19 12 64 72 39 24 0E 29 E7 8B F9 6A BB 5A D2 5B 1C";
    String endpoint = "/cas/ITSClient";
    String mac;
    String UserAgent_prefix = "User-Agent: IPGWLinux1.1_Linux_";
    String header = "Host: its.pku.edu.cn\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept-Encoding: gzip\r\n";
    String username;
    String password;
};
#endif
