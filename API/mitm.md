# PKU IPGW script

## Method of Getting the API

I did a mitm(man in the middle attack) to aquire the https request API. I used the tool mitmproxy(https://mitmproxy.org/) to generate the bogus SSL certificate and intercept the traffic. The steps are as follows.

1. Install `mitmproxy` tools according to the instructions on its website.
2. Acquire the CA certificate. They are already in the folder `~/.mitmproxy`. 

In order to make the operating system trust the bogus CA certificate as a root certificate, do the following steps.
3. Make sure the program `ca-certificates` is installed. Use `apt` to check. 
4. Go to directory '/usr/share/ca-certificates/`. Make a new directory, call it anything you wish, for example `example.com`.
5. Copy the `mitmproxy-ca-cert.pem` in `~/.mitmproxy` to the new directory. Change the extension to `.crt`.
6. Add a line to the file `/etc/ca-certificates.conf`: `example.com/mitmproxy-ca-cert.crt`.
7. Run `update-ca-certificate` command. The `/etc/ssl/certs` directory will now be regenerated, and the bogus certificate will now be trusted. Most of the operations require root privildge.

When all is set up, it's time to intercept the traffic. Start an instance of `mitmproxy`, which is a http/https proxy server listening at 127.0.0.1:8080. Open a separate shell instance. Change the proxy setting in that shell, using `export https_proxy=127.0.0.1:8080`. The http traffic could be redirected as well. Note the configuration lasts only for this shell session.

Run the PKU Internet Service's Linux client from that shell. You should see the intercepted traffic in mitmproxy's window. Congratulations! You've just accomplished an MITM attack!
