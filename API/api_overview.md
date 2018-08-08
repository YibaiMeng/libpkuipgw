# API Overview
All users of Peking University's Internet service need to authenticate when attempting to access out of campus resources. The steps are as follows:

1. The user connects to the school network, either wirelessly, by connecting to the WiFi network "Wireless PKU", or by ethernet.
2. Now, the user can access resources within campus, for example the school library, or other local servers.
3. The user authenticates him/herself if he wishes to access the Internet. The user can either visit the website `its.pku.edu.cn`, or use a variaty of clients.
4. The user can authenticate, close access, see the online clients for their accounts, check their balances and take other actions.

Technically, the auth processes simply send a HTTP PUT/GET request. So the APIs are pretty straight forward to reimplement. I have implemented:
- connect: Authenticate and gain Internet access.
- close & close_all: Close access to the Internet.
- get_connections: Get connection information under the same account.
The other functionallties are not frequently used and are better left to the Web interface
