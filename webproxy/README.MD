Web Proxy Guide
===
Okay! This system of files creates a web proxy that listens for a web client. The client will seek the HTTP info of a website, which the proxy will process, create the request for, send the request, and then forward the results to the server. This is a build up to my proxyandcache project also in this repository.

The client in this case automatically requests example.com. You can change this by manually going into the file and asking for a different URL. Note, though, that right now this code only works for HTTP requests, not HTTPS.

To run this system of files, run the proxy in one terminal window by typing:
>python3 web_proxy.py

Afterwards, run the client in either the terminal of another device or another terminal window by typing:
>python3 web_client.py

The results should look like this:
<img width="1440" alt="proxy" src="https://user-images.githubusercontent.com/124002750/222594440-368a0f8c-cf82-4646-a65f-7a83580add08.png">
