#include <WiFi.h>
#include <IPGWClient.h>

static const String sta_ssid = "Wireless PKU";
static const String sta_password = "";

static const String username = "1111111111"; // Change it to your own Student/Faculty ID.
static const String password = "aiguojinbuminzhukexue"; // Change it to your own password.

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Arduino has opened serial connection at 115200 baud rate.");

  // Connecting to Wireless PKU
  WiFi.begin(sta_ssid.c_str(), sta_password.c_str());
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Trying to connect. Status is " + String(WiFi.status()));
    delay(500);
  }
  Serial.println("Connected to Wireless PKU!");

  
  String mac = WiFi.macAddress(); 
  // Example value may be 5C:CF:7F:08:11:17
  // Needed because the logging protocol requires the device's MAC. (Quite stupid actually. Who appends the MAC on their User-Agent?)
  // Note that if you are using a different network interfance, for example ethernet or serial, then your must aquire your MAC address in a different way.
  // For example, if you are using ethernet, the only way to get the MAC maybe is to look at a sticker on your board.  
  
  IPGWClient clt(username, password, mac);
  while (clt.connect() != IPGW_SUCC) {
    delay(2000);
  }
  // Finer logic may be implemented to deal with all the other edge cases. 
  
  Serial.println("Now we are able to access the outside Internet! Check your ITS account!"); 
}

void loop() {

}
