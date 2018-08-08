#include "IPGWClient.h"

IPGWClient::IPGWClient(const String _username, const String _password, const String _mac) {
  IPGW_DEBUG("Initializing IPGWClient object.");
  IPGW_DEBUG("Username is: " + _username + "; Password is: " + _password);
  username = _username;
  password = _password;
  IPGW_DEBUG("MAC address for NodeMCU board STA mode is: " + _mac);
  mac = _mac;
  mac.replace(":", "-");
  mac.toLowerCase();
  IPGW_DEBUG("MAC address reformatted: " + mac);
  IPGW_DEBUG("Initialization complete.");
}

IPGWStatus IPGWClient::connect() {
  if (!client.connect(host.c_str(), 443)) {
    IPGW_DEBUG("Connection failed");
    return IPGW_NO_CONN;
  }
  #ifdef IPGW_CHECK_CERT
  if (client.verify(fingerprint.c_str(), host.c_str())) {
    IPGW_DEBUG("Certificate matches.");
  } else {
    IPGW_DEBUG("Certificate doesn't match");
    return IPGW_CERT_ERR;
  }
  #else
    IPGW_DEBUG("Certificate check skipped.");
  #endif
  String payload = "cmd=open&username=" + username + "&password=" + password + "&iprange=free&ip=&lang=en&app=1.0";
  int content_length =  payload.length();
  String POST_payload = String("POST ") + endpoint + " HTTP/1.0\r\n" +
                    UserAgent_prefix + mac + "\r\n" + header + "Content-Length: " +
                    String(content_length) + "\r\n\r\n" + payload;
  IPGW_DEBUG("The POSTed message is: " + POST_payload);
  client.print(POST_payload.c_str());
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      IPGW_DEBUG("Headers received from PKU ITS.");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  IPGW_DEBUG("Received response body is: " + line);
  if (line.startsWith("{\"succ\":\"\"")) {
    IPGW_DEBUG("Successfully authenticated PKU ITS.");
    return IPGW_SUCC;
  }
  else if (line.startsWith("{\"error\":\"Password error\"")) {
    IPGW_DEBUG("Wrong password!");
    return IPGW_PWD_ERR;
  }
  else {
    IPGW_DEBUG("Something Wrong! Unable to authenticated PKU ITS.");
    return IPGW_GENERAL_ERR;
  }
}
