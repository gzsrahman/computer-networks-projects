Web Proxy Guide
===
The relevant files for this document are:
>web_proxy.py
>web_client.py

Run them by typing the following into separate terminal consoles, with the proxy first followed by the client:
python3 web_proxy.py
python3 web_client.py
web_proxy.py initiates a connection, waiting for web_client.py to connect to it. The latter then parses a pre-specified website url, creates a request to get the HTTP info from the site, and sends over the request line to web_proxy.py. The proxy then contacts the host referenced in the website url, requests the info, waits to receive the data, closes the connection with the web host, and then sends the data to the client. web_client.py then prints the received data and closes its connection to web_proxy.py

