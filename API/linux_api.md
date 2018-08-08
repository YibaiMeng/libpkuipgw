# API of Linux Client

The reverse engineered API is based on Version 1.1 of the official client, released on 2017-03-23. The process of reverse engineering is recorded in [this file](miti.md).

The Linux API is simple and straight-forward, so my reimplementations are all based on it. However, the corner cases may still need some work, so don't use it for important stuff.

## Overview

The Linux Client uses HTTP POST requests. The hostname is `https://its.pku.edu.cn`, with endpoint being `/cas/ITSClient`.

The header fields are as follows:

- Host: `its.pku.edu.cn` 
- User-Agent: `IPGWLinux1.1_Linux_27-e2-a6-b1-b9-12` 
- Content-Type: `application/x-www-form-urlencoded`
- Accept-Encoding: `gzip`

For the User-Agent, the literal at the end is the network interface's MAC address. Note the formatting. All parameters are required.

## List of commands

### Connect to the Internet

Parameters are
- cmd: `open`.
- username: A string for the username of the account. For example, 1700012301 
- password: The account's password, in plain text.
- iprange: `free`. Exists for historical reasons.
- ip: Leave it empty. I don't know what it does.
- lang: `en`
- app: `1.0`

When successfully authenticated, an example JSON response is:
```
{
    "succ":"",
    "ver":"1.1",
    "FIXRATE":"YES",
    "FR_TYPE":"",
    "FR_DESC_CN":"不限时间",
    "FR_DESC_EN":"unlimited",
    "SCOPE":"international",
    "DEFICIT":"",
    "FR_TIME_CN":"",
    "FR_TIME_EN":"Unlimited",
    "CONNECTIONS":"1",
    "BALANCE_CN":"1000.0",
    "BALANCE_EN":"1000.0",
    "IP":"10.2.111.111"
}
```

Most terms exist for historical reasons and are now obsolete. The remaining used parameters are explained:
- CONNECTIONS: The number of connections the account has at the moment.
- BALANCE_CN: The remaining credit of the account, in CNY. `BALANCE_EN` is identical.
- IP: The assigned LAN IP for this connection. 

When the username doesn't exist, it returns:
```
{
    "error":"user not found"
}
```

When the user exists, but the password is wrong, returns:
```
{
    "error": "Password error"
}
```

## Close the current connection.

Parameters are:
- cmd: `close`.
- lang: `en`

Response when successfully closed is:
```
{
    "succ": "close_OK"
}
```

I don't know what the error responses are.

# Close all the connections under the user's account

Parameters are:
- cmd: `closeall`.
- lang: `en`
- username: A string for the username of the account. For example, 1700012301 
- password: The account's password, in plain text.

Note that this function may be called, even if NOT connected to the school's network! That's why authentication is needed.

Response is:
```
{
    "succ": "close_OK"
}
```
